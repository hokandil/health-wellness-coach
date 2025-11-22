"""
RunnerManager: Central orchestration for ADK agents, sessions, and plugins.

This module provides the RunnerManager class which manages:
- ADK Runner configuration
- Session persistence (DatabaseSessionService or InMemorySessionService)
- Memory management (InMemoryMemoryService)
- Plugin integration (LoggingPlugin, HealthMetricsPlugin)
- Agent execution and query routing
"""

import os
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService, InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.plugins import LoggingPlugin
from google.genai import types
from google.genai.errors import ClientError

from src.config import config

logger = logging.getLogger(__name__)


class RunnerManager:
    """
    Manages ADK Runner, session services, memory services, and plugins.
    
    This class provides a centralized interface for executing agent queries
    with proper session management, memory persistence, and observability.
    """
    
    def __init__(self):
        """Initialize the RunnerManager with session and memory services."""
        self._runner: Optional[Runner] = None
        self._session_service = None
        self._memory_service = None
        self._plugins = []
        
        # Initialize services
        self._initialize_services()
        
    def _initialize_services(self):
        """Initialize session service, memory service, and plugins."""
        # Initialize session service based on configuration
        use_persistent = os.getenv('USE_PERSISTENT_SESSIONS', 'true').lower() == 'true'
        
        if use_persistent:
            try:
                # Create data directory if it doesn't exist
                db_url = os.getenv('SESSION_DB_URL', 'sqlite:///data/sessions.db')
                db_path = db_url.replace('sqlite:///', '')
                Path(db_path).parent.mkdir(parents=True, exist_ok=True)
                
                self._session_service = DatabaseSessionService(db_url=db_url)
                logger.info(f"Initialized DatabaseSessionService with URL: {db_url}")
            except Exception as e:
                logger.warning(f"Failed to initialize DatabaseSessionService: {e}. Falling back to InMemorySessionService.")
                self._session_service = InMemorySessionService()
        else:
            self._session_service = InMemorySessionService()
            logger.info("Initialized InMemorySessionService")
        
        # Initialize memory service
        self._memory_service = InMemoryMemoryService()
        logger.info("Initialized InMemoryMemoryService")
        
        # Initialize plugins
        self._initialize_plugins()
        
    def _initialize_plugins(self):
        """Initialize observability plugins."""
        # Add LoggingPlugin (no parameters needed)
        logging_plugin = LoggingPlugin()
        self._plugins.append(logging_plugin)
        logger.info("Added LoggingPlugin")
        
        # Add HealthMetricsPlugin if enabled
        enable_health_metrics = os.getenv('ENABLE_HEALTH_METRICS', 'true').lower() == 'true'
        if enable_health_metrics:
            try:
                from src.plugins.health_metrics_plugin import HealthMetricsPlugin
                health_metrics_plugin = HealthMetricsPlugin()
                self._plugins.append(health_metrics_plugin)
                logger.info("Added HealthMetricsPlugin")
            except ImportError:
                logger.warning("HealthMetricsPlugin not found. Skipping health metrics.")
    
    def _get_runner(self, agent: Agent) -> Runner:
        """
        Get or create a Runner instance for the given agent.
        
        Args:
            agent: The ADK Agent to run
            
        Returns:
            Configured Runner instance
        """
        return Runner(
            app_name="health_wellness_coach",
            agent=agent,
            session_service=self._session_service,
            memory_service=self._memory_service,
            plugins=self._plugins
        )
    
    async def run_query(
        self,
        agent: Agent,
        query: str,
        user_id: str,
        session_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Execute a query using the specified agent with session management.
        
        Args:
            agent: The ADK Agent to use for processing the query
            query: The user's query string
            user_id: Unique identifier for the user
            session_id: Optional session ID for conversation continuity
            context: Optional additional context for the query
            
        Returns:
            The agent's response as a string
            
        Raises:
            Exception: If query execution fails
        """
        try:
            # Get runner for this agent
            runner = self._get_runner(agent)
            
            # Use session_id or fallback to user_id
            actual_session_id = session_id or user_id
            
            # Ensure session exists
            try:
                session = await self._session_service.get_session(
                    app_name="health_wellness_coach",
                    user_id=user_id,
                    session_id=actual_session_id
                )
                if not session:
                    await self._session_service.create_session(
                        app_name="health_wellness_coach",
                        user_id=user_id,
                        session_id=actual_session_id
                    )
            except Exception as e:
                logger.warning(f"Session management warning: {e}")
            
            # Prepare additional context (don't include session_id here)
            session_context = {
                'user_id': user_id,
                **(context or {})
            }
            
            logger.info(f"Running query for user {user_id}, session {actual_session_id}")
            logger.debug(f"Query: {query}")
            
            # Execute the query using ADK Runner API
            # Runner.run() expects: user_id, session_id, new_message (types.Content)
            # It returns a Generator of Events (not async)
            
            # Create Content object from query string
            content = types.Content(
                role="user",
                parts=[types.Part(text=query)]
            )
            
            events = []
            try:
                for event in runner.run(
                    user_id=user_id,
                    session_id=actual_session_id,
                    new_message=content
                ):
                    events.append(event)
            except ClientError as e:
                logger.error(f"API Error: {e}")
                return f"I encountered an issue connecting to the AI service. Please check your API configuration. Error: {e}"
            except Exception as e:
                logger.error(f"Runtime Error: {e}")
                return f"I encountered an unexpected error. Please try again later. Error: {e}"
            
            # Extract the final response from events
            # The last event should contain the agent's response
            if events:
                last_event = events[-1]
                # Try to get the response text from the event
                if hasattr(last_event, 'content'):
                    response = str(last_event.content)
                elif hasattr(last_event, 'text'):
                    response = last_event.text
                else:
                    response = str(last_event)
            else:
                response = "No response generated"
            
            if not response or response == "No response generated":
                logger.warning("No response generated from runner events")
                return "I apologize, but I encountered an issue connecting to the AI service (likely an API configuration error). Please check your .env file and console logs for details."

            logger.info("Query executed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error executing query: {e}", exc_info=True)
            raise
    
    async def get_session_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversation history for a session.
        
        Args:
            session_id: The session ID to retrieve history for
            limit: Optional maximum number of messages to retrieve
            
        Returns:
            List of message dictionaries with role and content
        """
        try:
            if hasattr(self._session_service, 'get_session'):
                session = await self._session_service.get_session(session_id)
                if session and hasattr(session, 'messages'):
                    messages = session.messages
                    if limit:
                        messages = messages[-limit:]
                    return [
                        {'role': msg.role, 'content': msg.content}
                        for msg in messages
                    ]
            return []
        except Exception as e:
            logger.error(f"Error retrieving session history: {e}", exc_info=True)
            return []
    
    async def clear_session(self, session_id: str) -> bool:
        """
        Clear/delete a session and its history.
        
        Args:
            session_id: The session ID to clear
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if hasattr(self._session_service, 'delete_session'):
                await self._session_service.delete_session(session_id)
                logger.info(f"Cleared session: {session_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error clearing session: {e}", exc_info=True)
            return False
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get metrics from all plugins.
        
        Returns:
            Dictionary containing metrics from all plugins
        """
        metrics = {}
        for plugin in self._plugins:
            if hasattr(plugin, 'get_metrics'):
                plugin_name = plugin.__class__.__name__
                metrics[plugin_name] = plugin.get_metrics()
        return metrics


# Singleton instance
runner_manager = RunnerManager()
