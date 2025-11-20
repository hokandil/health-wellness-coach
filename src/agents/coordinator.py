"""
Health Coordinator Agent - Main orchestrator using Google ADK (Simplified)
"""
from typing import Dict, Any, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.base_agent import create_adk_agent
from src.agents.nutrition_agent import create_nutrition_agent
from src.agents.fitness_agent import create_fitness_agent
from src.agents.sleep_agent import create_sleep_agent
from src.agents.mental_wellness_agent import create_mental_wellness_agent
from config.prompts import COORDINATOR_PROMPT
import logging


def create_health_coordinator():
    """
    Create the Health Coordinator with all specialized sub-agents
    
    Returns:
        Configured coordinator agent with all sub-agents
    """
    logger = logging.getLogger("HealthCoordinator")
    
    # Create all specialized agents
    nutrition_agent = create_nutrition_agent()
    fitness_agent = create_fitness_agent()
    sleep_agent = create_sleep_agent()
    mental_wellness_agent = create_mental_wellness_agent()
    
    # Create coordinator with sub-agents
    coordinator = create_adk_agent(
        name="Health Coordinator",
        instruction=COORDINATOR_PROMPT,
        description="Main health coach coordinator that orchestrates specialized agents for nutrition, fitness, sleep, and mental wellness",
        tools=[],
        sub_agents=[
            nutrition_agent,
            fitness_agent,
            sleep_agent,
            mental_wellness_agent
        ]
    )
    
    logger.info(f"Health Coordinator initialized with 4 specialized sub-agents")
    
    return coordinator


def execute_health_workflow(
    coordinator,
    user_input: str,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Execute a health coaching workflow (Simplified - using direct Gemini API)
    
    Note: Full ADK Runner integration is complex. This uses a simplified approach
    that leverages ADK agent structure but uses direct Gemini API for execution.
    
    Args:
        coordinator: Health coordinator agent
        user_input: User's message or query
        context: Optional user context (profile, history, etc.)
    
    Returns:
        Complete response
    """
    from google.genai import Client
    import os
    
    # Build context-aware prompt
    if context:
        full_prompt = _build_prompt_with_context(user_input, context)
    else:
        full_prompt = user_input
    
    # Use direct Gemini API (simplified approach)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {
            "user_input": user_input,
            "final_response": "No API key configured. Please set GOOGLE_API_KEY in .env file.",
            "success": False
        }
    
    try:
        client = Client(api_key=api_key)
        
        # Generate response using Gemini with coordinator's instruction
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=f"{COORDINATOR_PROMPT}\n\n{full_prompt}"
        )
        
        return {
            "user_input": user_input,
            "final_response": response.text,
            "success": True
        }
    except Exception as e:
        logging.error(f"Error executing workflow: {e}")
        return {
            "user_input": user_input,
            "final_response": f"Error: {str(e)}",
            "success": False
        }


def _build_prompt_with_context(
    user_input: str,
    context: Optional[Dict[str, Any]] = None
) -> str:
    """Build complete prompt with user context"""
    prompt_parts = []
    
    if context:
        prompt_parts.append("CONTEXT:")
        
        if "user_profile" in context:
            profile = context["user_profile"]
            prompt_parts.append(f"""
User Profile:
- Age: {profile.get('age', 'N/A')}
- Gender: {profile.get('gender', 'N/A')}
- Current Weight: {profile.get('current_weight_kg', 'N/A')}kg
- Goals: {', '.join(profile.get('goals', []))}
- Restrictions: {', '.join(profile.get('restrictions', []))}
""")
        
        if "recent_history" in context:
            prompt_parts.append(f"\nRecent History:\n{context['recent_history']}")
        
        prompt_parts.append("\n---\n")
    
    prompt_parts.append(f"USER REQUEST:\n{user_input}")
    
    return "\n".join(prompt_parts)
