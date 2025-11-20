"""
Fitness Agent - Specialized in workout programming and exercise guidance
"""
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.base_agent import BaseAgent
from config.prompts import FITNESS_AGENT_PROMPT
from src.tools.fitness_tools import FITNESS_TOOLS


class FitnessAgent(BaseAgent):
    """Fitness specialist agent"""
    
    def __init__(self):
        super().__init__(
            name="Fitness Agent",
            system_prompt=FITNESS_AGENT_PROMPT,
            tools=FITNESS_TOOLS
        )
    
    def create_workout_program(
        self,
        user_profile: Dict[str, Any],
        num_weeks: int = 4
    ) -> Dict[str, Any]:
        """Create personalized workout program"""
        # Assess fitness level if not already done
        if "fitness_level" not in user_profile:
            assessment = self.call_tool(
                "assess_fitness_level",
                can_do_pushups=user_profile.get("can_do_pushups", 5),
                can_do_squats=user_profile.get("can_do_squats", 10),
                can_run_minutes=user_profile.get("can_run_minutes", 10),
                exercise_history=user_profile.get("exercise_history", "beginner")
            )
            fitness_level = assessment["fitness_level"]
        else:
            fitness_level = user_profile["fitness_level"]
        
        # Generate workout plan
        workout_plan = self.call_tool(
            "generate_workout_plan",
            fitness_level=fitness_level,
            goals=user_profile.get("fitness_goals", ["lose_weight"]),
            days_per_week=user_profile.get("training_days_per_week", 3),
            equipment=user_profile.get("available_equipment", ["bodyweight"]),
            workout_duration_minutes=user_profile.get("workout_duration", 45),
            num_weeks=num_weeks
        )
        
        return {
            "fitness_level": fitness_level,
            "workout_plan": workout_plan,
            "success": True
        }
