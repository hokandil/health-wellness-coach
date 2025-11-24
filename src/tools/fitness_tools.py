"""
Fitness-related tools for workout planning and exercise recommendations

These tools are used by the Fitness Agent via Google ADK.
"""
from typing import Dict, List, Any, Optional
import json
import os
from src.utils.observability import trace_tool


@trace_tool
def assess_fitness_level(
    can_do_pushups: int,
    can_do_squats: int,
    can_run_minutes: int,
    exercise_history: str = "beginner"
) -> Dict[str, str]:
    """
    Assess user's current fitness level
    
    Args:
        can_do_pushups: Number of pushups in one set
        can_do_squats: Number of bodyweight squats in one set
        can_run_minutes: Minutes of continuous running
        exercise_history: "beginner", "intermediate", "advanced"
    
    Returns:
        Fitness assessment with recommendations
    """
    # Simple assessment rubric
    if can_do_pushups >= 20 and can_do_squats >= 30 and can_run_minutes >= 30:
        level = "advanced"
    elif can_do_pushups >= 10 and can_do_squats >= 15 and can_run_minutes >= 15:
        level = "intermediate"
    else:
        level = "beginner"
    
    recommendations = {
        "beginner": "Start with bodyweight exercises, 2-3x/week, focus on form",
        "intermediate": "Mix of bodyweight and weighted exercises, 3-4x/week, progressive overload",
        "advanced": "Complex movements, 4-5x/week, periodization and specialization"
    }
    
    return {
        "fitness_level": level,
        "pushup_rating": "excellent" if can_do_pushups >= 20 else "good" if can_do_pushups >= 10 else "needs_work",
        "squat_rating": "excellent" if can_do_squats >= 30 else "good" if can_do_squats >= 15 else "needs_work",
        "cardio_rating": "excellent" if can_run_minutes >= 30 else "good" if can_run_minutes >= 15 else "needs_work",
        "recommendation": recommendations[level],
        "starting_frequency": "2-3x/week" if level == "beginner" else "3-4x/week" if level == "intermediate" else "4-5x/week"
    }


@trace_tool
async def generate_workout_plan(
    fitness_level: str,
    goals: List[str],
    days_per_week: int,
    equipment: List[str],
    workout_duration_minutes: int = 45,
    num_weeks: int = 4,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate personalized workout program
    
    Args:
        fitness_level: "beginner", "intermediate", "advanced"
        goals: List like ["lose_weight", "build_muscle", "improve_endurance"]
        days_per_week: 2-6 training days
        equipment: ["bodyweight", "dumbbells", "barbell", "resistance_bands", "gym"]
        workout_duration_minutes: Session length
        num_weeks: Program duration
        api_key: Google API key (optional)
    
    Returns:
        Complete workout program with progressive overload
    """
    from google.adk.models import Gemini, LlmRequest
    from google.genai.types import Content, Part
    
    api_key = api_key or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {
            "error": "No API key configured",
            "weeks": []
        }
        
    llm = Gemini(model="gemini-2.5-flash", api_key=api_key)
    
    goals_str = ", ".join(goals)
    equipment_str = ", ".join(equipment)
    
    prompt = f"""Create a {num_weeks}-week workout program:

USER PROFILE:
- Fitness Level: {fitness_level}
- Goals: {goals_str}
- Training Frequency: {days_per_week} days/week
- Session Duration: {workout_duration_minutes} minutes
- Available Equipment: {equipment_str}

Requirements:
- Progressive overload week-to-week
- Balanced muscle group coverage
- Include warm-up and cool-down
- Specific sets, reps, rest periods

Return JSON with structure showing weeks, workouts per week, exercises with sets/reps/rest, and exercise library.
Return ONLY valid JSON."""

    try:
        request = LlmRequest(
            model="gemini-2.5-flash",
            contents=[Content(parts=[Part(text=prompt)])]
        )
        full_response_text = ""
        chunk_count = 0
        async for chunk in llm.generate_content_async(request):
            chunk_count += 1
            # LlmResponse has .content.parts[].text structure
            if hasattr(chunk, 'content') and chunk.content:
                if hasattr(chunk.content, 'parts') and chunk.content.parts:
                    for part in chunk.content.parts:
                        if hasattr(part, 'text') and part.text:
                            full_response_text += part.text
        
        if not full_response_text:
            return {
                "error": f"No text received from API (received {chunk_count} chunks)",
                "weeks": []
            }
        
        result_text = full_response_text.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:-3]
        elif result_text.startswith("```"):
            result_text = result_text[3:-3]
        
        result_text = result_text.strip()
        
        if not result_text:
            return {
                "error": "Empty response after processing",
                "weeks": []
            }
        
        return json.loads(result_text)
    except json.JSONDecodeError as e:
        return {
            "error": f"JSON parsing error: {str(e)}. Response preview: {full_response_text[:200] if full_response_text else 'empty'}",
            "weeks": []
        }
    except Exception as e:
        return {
            "error": f"Could not generate workout plan: {str(e)}",
            "weeks": []
        }


@trace_tool
def calculate_calories_burned(
    activity: str,
    duration_minutes: int,
    weight_kg: float,
    intensity: str = "moderate"
) -> Dict[str, Any]:
    """
    Estimate calories burned during exercise
    
    Args:
        activity: Type of exercise (e.g., "running", "weightlifting", "yoga")
        duration_minutes: Duration of activity
        weight_kg: User's weight in kg
        intensity: "light", "moderate", "vigorous"
    
    Returns:
        Estimated calories burned
    """
    # MET (Metabolic Equivalent of Task) values
    met_values = {
        "running": {"light": 6.0, "moderate": 8.0, "vigorous": 11.0},
        "walking": {"light": 3.0, "moderate": 3.5, "vigorous": 4.5},
        "cycling": {"light": 4.0, "moderate": 6.8, "vigorous": 10.0},
        "swimming": {"light": 4.5, "moderate": 6.0, "vigorous": 9.0},
        "weightlifting": {"light": 3.0, "moderate": 5.0, "vigorous": 6.0},
        "hiit": {"light": 8.0, "moderate": 10.0, "vigorous": 12.0},
        "yoga": {"light": 2.5, "moderate": 3.0, "vigorous": 4.0},
        "dancing": {"light": 3.0, "moderate": 4.5, "vigorous": 6.5},
    }
    
    # Default MET if activity not found
    met = met_values.get(activity.lower(), {}).get(intensity, 5.0)
    
    # Calories = MET × weight(kg) × time(hours)
    calories = met * weight_kg * (duration_minutes / 60)
    
    return {
        "activity": activity,
        "duration_minutes": duration_minutes,
        "intensity": intensity,
        "met_value": met,
        "calories_burned": round(calories),
        "calories_per_minute": round(calories / duration_minutes, 1)
    }
