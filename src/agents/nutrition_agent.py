"""
Nutrition Agent - Specialized in meal planning and nutrition guidance
"""
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.base_agent import create_adk_agent
from config.prompts import NUTRITION_AGENT_PROMPT
from src.tools import nutrition_tools


def create_nutrition_agent():
    """Create and configure the Nutrition Agent using Google ADK"""
    
    # Get all nutrition tool functions
    tools = [
        nutrition_tools.calculate_daily_calories,
        nutrition_tools.calculate_macro_targets,
        nutrition_tools.analyze_meal_macros,
        nutrition_tools.generate_meal_plan
    ]
    
    agent = create_adk_agent(
        name="Nutrition Agent",
        instruction=NUTRITION_AGENT_PROMPT,
        description="Specialist in meal planning, nutrition guidance, and macro calculations",
        tools=tools
    )
    
    return agent


# Helper functions for common nutrition workflows
def create_meal_plan_workflow(
    agent,
    user_profile: Dict[str, Any],
    num_days: int = 7
) -> Dict[str, Any]:
    """
    Execute complete meal planning workflow
    
    Args:
        agent: Nutrition agent instance
        user_profile: User profile data
        num_days: Number of days to plan
    
    Returns:
        Complete meal plan with calorie and macro data
    """
    # Build context-aware prompt
    prompt = f"""Create a personalized {num_days}-day meal plan for this user:

User Profile:
- Age: {user_profile.get('age')}
- Gender: {user_profile.get('gender')}
- Weight: {user_profile.get('current_weight_kg')}kg
- Height: {user_profile.get('height_cm')}cm
- Activity Level: {user_profile.get('activity_level', 'moderate')}
- Goal: {user_profile.get('primary_goal', 'lose_weight')}
- Dietary Restrictions: {', '.join(user_profile.get('dietary_restrictions', []))}
- Liked Foods: {', '.join(user_profile.get('preferences', {}).get('liked_foods', []))}
- Disliked Foods: {', '.join(user_profile.get('preferences', {}).get('disliked_foods', []))}

Please:
1. Calculate appropriate daily calorie target
2. Determine optimal macro distribution
3. Generate a {num_days}-day meal plan with recipes
4. Provide a shopping list

Use the available tools to calculate calories, macros, and generate the meal plan."""

    # ADK agent will automatically use tools as needed
    response = agent.run(prompt)
    
    return {
        "response": response,
        "success": True
    }
