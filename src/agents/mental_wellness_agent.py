"""
Mental Wellness Agent - Specialized in stress management and mindfulness guidance.

This agent uses ADK patterns with FunctionTool wrappers and output_key
for state management.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from google.adk.tools import FunctionTool
from src.agents.base_agent import create_health_agent
from config.prompts import MENTAL_WELLNESS_AGENT_PROMPT
from src.tools import mental_wellness_tools


def create_mental_wellness_agent():
    """
    Create and configure the Mental Wellness Agent using Google ADK.
    
    Returns:
        Configured ADK Agent for mental wellness guidance
    """
    
    # Wrap mental wellness tools with FunctionTool
    tools = [
        FunctionTool(mental_wellness_tools.assess_stress_level),
        FunctionTool(mental_wellness_tools.recommend_mindfulness_practice),
        FunctionTool(mental_wellness_tools.generate_relaxation_routine)
    ]
    
    agent = create_health_agent(
        name="mental_wellness_agent",
        instruction=MENTAL_WELLNESS_AGENT_PROMPT,
        description="Specialist in stress management, mindfulness practices, and mental wellness. "
                   "Assesses stress levels, recommends evidence-based mindfulness techniques, "
                   "and creates personalized relaxation routines.",
        tools=tools,
        output_key="wellness_assessment",
        temperature=0.8  # More creative for motivation and empathy
    )
    
    return agent


# Singleton instance
mental_wellness_agent = create_mental_wellness_agent()
