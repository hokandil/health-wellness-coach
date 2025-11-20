"""
Base agent utilities for Google ADK
"""
from google.adk.agents import LlmAgent
from typing import Dict, List, Any, Optional, Callable
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import Settings
import logging


def create_adk_agent(
    name: str,
    instruction: str,
    description: str,
    tools: List[Callable] = None,
    sub_agents: List[LlmAgent] = None,
    model_name: str = None
) -> LlmAgent:
    """
    Factory function to create ADK agents with consistent configuration
    
    Args:
        name: Agent name (will be converted to valid identifier)
        instruction: System instruction/prompt for the agent
        description: Brief description of agent's role
        tools: List of tool functions to equip the agent with
        sub_agents: List of sub-agents for multi-agent coordination
        model_name: Gemini model name (defaults to settings)
    
    Returns:
        Configured LlmAgent instance
    """
    # Convert name to valid Python identifier (ADK requirement)
    valid_name = name.lower().replace(" ", "_").replace("-", "_")
    
    logger = logging.getLogger(name)
    
    # Get model configuration
    agent_key = valid_name.replace("agent", "").strip("_")
    config = Settings.AGENT_CONFIG.get(
        agent_key,
        Settings.AGENT_CONFIG.get("coordinator", {})
    )
    
    model = model_name or config.get("model", "gemini-2.0-flash-exp")
    
    logger.info(f"Creating ADK agent: {valid_name} with model {model}")
    
    # Create ADK agent with valid identifier name
    agent = LlmAgent(
        name=valid_name,
        model=model,
        instruction=instruction,
        description=description,
        tools=tools or [],
        sub_agents=sub_agents or []
    )
    
    logger.info(f"{valid_name} initialized with {len(tools or [])} tools and {len(sub_agents or [])} sub-agents")
    
    return agent


class AgentResponse:
    """Wrapper for agent responses to maintain compatibility with existing code"""
    
    def __init__(self, agent_name: str, response_text: str, success: bool = True, metadata: Dict = None):
        self.agent = agent_name
        self.response = response_text
        self.success = success
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "agent": self.agent,
            "response": self.response,
            "success": self.success,
            "metadata": self.metadata
        }
