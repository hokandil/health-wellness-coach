"""
Fitness Agent - Specialized in workout programming and exercise guidance
"""
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.base_agent import create_adk_agent
from config.prompts import FITNESS_AGENT_PROMPT
from src.tools import fitness_tools


def create_fitness_agent():
    """Create and configure the Fitness Agent using Google ADK"""
    
    # Get all fitness tool functions
    tools = [
        fitness_tools.assess_fitness_level,
        fitness_tools.generate_workout_plan,
        fitness_tools.calculate_exercise_calories
    ]
    
    agent = create_adk_agent(
        name="Fitness Agent",
        instruction=FITNESS_AGENT_PROMPT,
        description="Specialist in workout programming, exercise guidance, and fitness assessment",
        tools=tools
    )
    
    return agent


def create_workout_program_workflow(
    agent,
    user_profile: Dict[str, Any],
    num_weeks: int = 4
) -> Dict[str, Any]:
    """
    Execute complete workout program creation workflow
    
    Args:
        agent: Fitness agent instance
        user_profile: User profile data
        num_weeks: Number of weeks to program
    
    Returns:
        Complete workout program
    """
    prompt = f"""Create a personalized {num_weeks}-week workout program for this user:

User Profile:
- Fitness Level: {user_profile.get('fitness_level', 'beginner')}
- Goals: {', '.join(user_profile.get('fitness_goals', ['general fitness']))}
- Training Days/Week: {user_profile.get('training_days_per_week', 3)}
- Available Equipment: {', '.join(user_profile.get('available_equipment', ['bodyweight']))}
- Workout Duration: {user_profile.get('workout_duration', 45)} minutes
- Exercise History: {user_profile.get('exercise_history', 'beginner')}

Please:
1. Assess their fitness level if needed
2. Generate a {num_weeks}-week progressive workout plan
3. Include exercise descriptions and form cues
4. Provide progression guidelines

Use the available tools to assess fitness and generate the workout plan."""

    response = agent.run(prompt)
    
    return {
        "response": response,
        "success": True
    }
