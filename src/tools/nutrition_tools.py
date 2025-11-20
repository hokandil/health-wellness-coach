"""
Nutrition-related tools for meal planning and macro calculations

These tools are used by the Nutrition Agent via Google ADK.
"""
from typing import Dict, List, Any
import json
import os
from src.utils.observability import trace_tool


@trace_tool
def calculate_daily_calories(
    age: int,
    weight_kg: float,
    height_cm: float,
    gender: str,
    activity_level: str,
    goal: str = "maintain"
) -> Dict[str, Any]:
    """
    Calculate TDEE (Total Daily Energy Expenditure) and calorie targets
    
    Args:
        age: User's age in years
        weight_kg: Current weight in kilograms
        height_cm: Height in centimeters
        gender: "male" or "female"
        activity_level: "sedentary", "light", "moderate", "active", "very_active"
        goal: "lose_weight", "maintain", "gain_weight"
    
    Returns:
        Dictionary with BMR, TDEE, and goal-specific calorie targets
    """
    # Mifflin-St Jeor Equation for BMR
    if gender.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    
    # Activity multipliers
    activity_multipliers = {
        "sedentary": 1.2,       # Little or no exercise
        "light": 1.375,         # Light exercise 1-3 days/week
        "moderate": 1.55,       # Moderate exercise 3-5 days/week
        "active": 1.725,        # Heavy exercise 6-7 days/week
        "very_active": 1.9      # Very heavy exercise, physical job
    }
    
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)
    
    # Goal adjustments
    if goal == "lose_weight":
        target = tdee - 500  # 500 cal deficit = ~1 lb/week loss
        min_cal = max(target, 1200 if gender == "female" else 1500)  # Safety floor
        target = max(target, min_cal)
    elif goal == "gain_weight":
        target = tdee + 300  # 300 cal surplus = ~0.5 lb/week gain
    else:
        target = tdee
    
    return {
        "bmr": round(bmr),
        "tdee": round(tdee),
        "target_calories": round(target),
        "weight_loss_target": round(tdee - 500),
        "maintenance_target": round(tdee),
        "weight_gain_target": round(tdee + 300),
        "activity_level": activity_level,
        "goal": goal
    }


@trace_tool
def calculate_macro_targets(
    target_calories: int,
    weight_kg: float,
    goal: str = "lose_weight",
    activity_level: str = "moderate"
) -> Dict[str, Any]:
    """
    Calculate macronutrient targets (protein, carbs, fats)
    
    Args:
        target_calories: Daily calorie target
        weight_kg: Current weight in kg
        goal: "lose_weight", "maintain", "gain_muscle"
        activity_level: Training intensity level
    
    Returns:
        Dictionary with macro targets in grams and percentages
    """
    # ... (rest of function logic remains same, just decorating)
    # Protein: Higher for weight loss and muscle gain
    if goal in ["lose_weight", "gain_muscle"]:
        protein_g_per_kg = 2.0  # 2g per kg for muscle preservation/growth
    else:
        protein_g_per_kg = 1.6
    
    protein_grams = weight_kg * protein_g_per_kg
    protein_calories = protein_grams * 4  # 4 cal per gram
    
    # Fat: 25-30% of calories
    fat_percentage = 0.28
    fat_calories = target_calories * fat_percentage
    fat_grams = fat_calories / 9  # 9 cal per gram
    
    # Carbs: Remaining calories
    carb_calories = target_calories - protein_calories - fat_calories
    carb_grams = max(carb_calories / 4, 0)  # 4 cal per gram, minimum 0
    
    return {
        "target_calories": target_calories,
        "protein": {
            "grams": round(protein_grams),
            "calories": round(protein_calories),
            "percentage": round((protein_calories / target_calories) * 100)
        },
        "carbs": {
            "grams": round(carb_grams),
            "calories": round(carb_calories),
            "percentage": round((carb_calories / target_calories) * 100)
        },
        "fats": {
            "grams": round(fat_grams),
            "calories": round(fat_calories),
            "percentage": round((fat_calories / target_calories) * 100)
        }
    }


@trace_tool
def analyze_meal_macros(meal_description: str, api_key: str = None) -> Dict[str, Any]:
    """
    Analyze macronutrients in a meal description using Gemini
    
    Args:
        meal_description: Natural language description of food
        api_key: Google API key (optional if already configured)
    
    Returns:
        Estimated macros for the meal
    """
    # Use ADK-compatible model initialization
    from google.genai import Client
    
    api_key = api_key or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {
            "error": "No API key configured",
            "total_calories": 0,
            "protein_grams": 0,
            "carbs_grams": 0,
            "fat_grams": 0
        }
    
    client = Client(api_key=api_key)
    
    prompt = f"""Analyze the following meal and provide nutritional breakdown:

Meal: {meal_description}

Provide a JSON response with:
- total_calories (number)
- protein_grams (number)
- carbs_grams (number)
- fat_grams (number)
- fiber_grams (number)
- meal_components (array of objects with: food, portion, calories, protein, carbs, fats)

Be realistic with portion sizes. If not specified, assume standard portions.
Return ONLY the JSON, no other text."""

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )
        
        # Extract JSON from response
        result_text = response.text.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:-3]
        elif result_text.startswith("```"):
            result_text = result_text[3:-3]
        
        result = json.loads(result_text)
        return result
    except Exception as e:
        return {
            "error": f"Could not parse nutrition data: {str(e)}",
            "total_calories": 0,
            "protein_grams": 0,
            "carbs_grams": 0,
            "fat_grams": 0
        }


@trace_tool
def generate_meal_plan(
    target_calories: int,
    macro_targets: Dict[str, Any],
    dietary_restrictions: List[str] = None,
    liked_foods: List[str] = None,
    disliked_foods: List[str] = None,
    num_days: int = 7,
    api_key: str = None
) -> Dict[str, Any]:
    """
    Generate a personalized meal plan
    
    Args:
        target_calories: Daily calorie target
        macro_targets: From calculate_macro_targets()
        dietary_restrictions: List like ["gluten-free", "lactose-intolerant"]
        liked_foods: Foods user enjoys
        disliked_foods: Foods to avoid
        num_days: Number of days to plan (default 7)
        api_key: Google API key (optional)
    
    Returns:
        Complete meal plan with recipes
    """
    from google.genai import Client
    
    api_key = api_key or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {
            "error": "No API key configured",
            "days": []
        }

    
    client = Client(api_key=api_key)
    
    dietary_restrictions = dietary_restrictions or []
    liked_foods = liked_foods or []
    disliked_foods = disliked_foods or []
    
    restrictions_str = ", ".join(dietary_restrictions) if dietary_restrictions else "none"
    likes_str = ", ".join(liked_foods[:5]) if liked_foods else "flexible"
    dislikes_str = ", ".join(disliked_foods[:5]) if disliked_foods else "none"
    
    prompt = f"""Create a {num_days}-day meal plan with these requirements:

TARGET NUTRITION (per day):
- Calories: {target_calories}
- Protein: {macro_targets['protein']['grams']}g
- Carbs: {macro_targets['carbs']['grams']}g
- Fats: {macro_targets['fats']['grams']}g

DIETARY RESTRICTIONS: {restrictions_str}
PREFERRED FOODS: {likes_str}
FOODS TO AVOID: {dislikes_str}

Requirements:
- 3 meals + 1 snack per day
- Hit macro targets within ±5%
- Variety: No meal repeated within 3 days
- Practical recipes (≤30 min prep)
- Include portion sizes

Return JSON with this structure:
{{
  "days": [
    {{
      "day": 1,
      "total_calories": number,
      "total_protein": number,
      "total_carbs": number,
      "total_fats": number,
      "meals": [
        {{
          "type": "breakfast|lunch|dinner|snack",
          "name": "Meal name",
          "ingredients": ["ingredient with portion"],
          "calories": number,
          "protein": number,
          "carbs": number,
          "fats": number,
          "prep_time_minutes": number,
          "instructions": "Brief cooking instructions"
        }}
      ]
    }}
  ],
  "shopping_list": {{
    "proteins": ["item"],
    "vegetables": ["item"],
    "grains": ["item"],
    "other": ["item"]
  }}
}}

Return ONLY valid JSON."""

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )
        
        result_text = response.text.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:-3]
        elif result_text.startswith("```"):
            result_text = result_text[3:-3]
        
        return json.loads(result_text)
    except Exception as e:
        return {
            "error": f"Could not generate meal plan: {str(e)}",
            "days": []
        }
