"""
Health Coordinator Agent - Main orchestrator using Google ADK
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
    
    ADK automatically handles:
    - Intelligent routing to appropriate sub-agents
    - Multi-agent coordination (parallel/sequential)
    - Response synthesis
    
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
    # ADK will automatically route requests to appropriate agents
    coordinator = create_adk_agent(
        name="Health Coordinator",
        instruction=COORDINATOR_PROMPT,
        description="Main health coach coordinator that orchestrates specialized agents for nutrition, fitness, sleep, and mental wellness",
        tools=[],  # Coordinator uses sub-agents, not tools directly
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
    Execute a health coaching workflow
    
    ADK automatically:
    - Analyzes the request
    - Routes to appropriate agent(s)
    - Coordinates multi-agent responses
    - Synthesizes final answer
    
    Args:
        coordinator: Health coordinator agent
        user_input: User's message or query
        context: Optional user context (profile, history, etc.)
    
    Returns:
        Complete response with routing and agent outputs
    """
    # Build context-aware prompt if context provided
    if context:
        full_prompt = _build_prompt_with_context(user_input, context)
    else:
        full_prompt = user_input
    
    # ADK handles all orchestration automatically
    response = coordinator.run(full_prompt)
    
    return {
        "user_input": user_input,
        "final_response": response,
        "success": True
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
