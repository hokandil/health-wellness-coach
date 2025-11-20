"""
Nutrition Agent - Specialized in meal planning and nutrition guidance
"""
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.base_agent import BaseAgent
from config.prompts import NUTRITION_AGENT_PROMPT
from src.tools.nutrition_tools import NUTRITION_TOOLS


class NutritionAgent(BaseAgent):
    """Nutrition specialist agent"""
    
    def __init__(self):
        super().__init__(
            name="Nutrition Agent",
            system_prompt=NUTRITION_AGENT_PROMPT,
            tools=NUTRITION_TOOLS
        )
    
    def create_meal_plan(
        self,
        user_profile: Dict[str, Any],
        num_days: int = 7
    ) -> Dict[str, Any]:
        """Create personalized meal plan for user"""
        # Calculate calorie and macro targets
        calories_data = self.call_tool(
            "calculate_daily_calories",
            age=user_profile["age"],
            weight_kg=user_profile["current_weight_kg"],
            height_cm=user_profile["height_cm"],
            gender=user_profile["gender"],
            activity_level=user_profile.get("activity_level", "moderate"),
            goal=user_profile.get("primary_goal", "lose_weight")
        )
        
        target_calories = calories_data["target_calories"]
        
        macro_targets = self.call_tool(
            "calculate_macro_targets",
            target_calories=target_calories,
            weight_kg=user_profile["current_weight_kg"],
            goal=user_profile.get("primary_goal", "lose_weight")
        )
        
        # Generate meal plan
        meal_plan = self.call_tool(
            "generate_meal_plan",
            target_calories=target_calories,
            macro_targets=macro_targets,
            dietary_restrictions=user_profile.get("dietary_restrictions", []),
            liked_foods=user_profile.get("preferences", {}).get("liked_foods", []),
            disliked_foods=user_profile.get("preferences", {}).get("disliked_foods", []),
            num_days=num_days
        )
        
        return {
            "calories_data": calories_data,
            "macro_targets": macro_targets,
            "meal_plan": meal_plan,
            "success": True
        }
