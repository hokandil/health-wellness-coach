"""
Mental Wellness Agent - Specialized in motivation and emotional support
"""
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.base_agent import create_adk_agent
from config.prompts import MENTAL_WELLNESS_AGENT_PROMPT


def create_mental_wellness_agent():
    """Create and configure the Mental Wellness Agent using Google ADK"""
    
    # Mental wellness agent is primarily conversational, no specific tools
    agent = create_adk_agent(
        name="Mental Wellness Agent",
        instruction=MENTAL_WELLNESS_AGENT_PROMPT,
        description="Specialist in motivation, emotional support, and mental health guidance",
        tools=[]  # Primarily conversational
    )
    
    return agent


def provide_motivation_workflow(
    agent,
    user_context: Dict[str, Any],
    situation: str = "general"
) -> Dict[str, Any]:
    """
    Provide personalized motivation and support
    
    Args:
        agent: Mental wellness agent instance
        user_context: User's current context and progress
        situation: Specific situation requiring motivation
    
    Returns:
        Motivational message and support
    """
    prompt = f"""Provide encouraging, personalized motivation for this user.

SITUATION: {situation}

USER CONTEXT:
- Current streak: {user_context.get('current_streak', 0)} days
- Recent challenges: {user_context.get('recent_challenges', 'None')}
- Recent wins: {user_context.get('recent_wins', 'None')}
- Progress: {user_context.get('progress_summary', 'Just starting')}

Create a warm, genuine message that:
1. Acknowledges their effort and progress
2. Provides perspective on challenges
3. Offers concrete next steps
4. Ends with encouragement"""

    response = agent.run(prompt)
    
    return {
        "response": response,
        "success": True
    }
