"""
Nutrition Agent - Specialized in meal planning and nutrition guidance.

This agent uses ADK patterns with FunctionTool wrappers and output_key
for state management.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from google.adk.tools import FunctionTool
from src.agents.base_agent import create_health_agent
from config.prompts import NUTRITION_AGENT_PROMPT
from src.tools import nutrition_tools


def create_nutrition_agent():
    """
    Create and configure the Nutrition Agent using Google ADK.
    
    Returns:
        Configured ADK Agent for nutrition guidance
    """
    
    # Wrap nutrition tools with FunctionTool
    tools = [
        FunctionTool(nutrition_tools.calculate_daily_calories),
        FunctionTool(nutrition_tools.calculate_macro_targets),
        FunctionTool(nutrition_tools.analyze_meal_macros),
        FunctionTool(nutrition_tools.generate_meal_plan)
    ]
    
    agent = create_health_agent(
        name="nutrition_agent",
        instruction=NUTRITION_AGENT_PROMPT,
        description="Specialist in meal planning, nutrition guidance, and macro calculations. "
                   "Provides personalized nutrition advice, calculates daily calorie needs, "
                   "determines optimal macro distribution, and creates customized meal plans.",
        tools=tools,
        output_key="nutrition_analysis",
        temperature=0.5  # More deterministic for calculations
    )
    
    return agent


# Singleton instance
nutrition_agent = create_nutrition_agent()
