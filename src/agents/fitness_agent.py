"""
Fitness Agent - Specialized in workout programming and exercise guidance.

This agent uses ADK patterns with FunctionTool wrappers and output_key
for state management.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from google.adk.tools import FunctionTool
from src.agents.base_agent import create_health_agent
from config.prompts import FITNESS_AGENT_PROMPT
from src.tools import fitness_tools


def create_fitness_agent():
    """
    Create and configure the Fitness Agent using Google ADK.
    
    Returns:
        Configured ADK Agent for fitness guidance
    """
    
    # Wrap fitness tools with FunctionTool
    tools = [
        FunctionTool(fitness_tools.assess_fitness_level),
        FunctionTool(fitness_tools.generate_workout_plan),
        FunctionTool(fitness_tools.calculate_calories_burned)
    ]
    
    agent = create_health_agent(
        name="fitness_agent",
        instruction=FITNESS_AGENT_PROMPT,
        description="Specialist in workout programming, exercise guidance, and fitness assessment. "
                   "Provides personalized workout plans, assesses fitness levels, and calculates "
                   "calories burned during exercise.",
        tools=tools,
        output_key="fitness_plan",
        temperature=0.6
    )
    
    return agent


# Singleton instance
fitness_agent = create_fitness_agent()
