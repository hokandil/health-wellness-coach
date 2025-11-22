"""
Mental wellness tools for stress management and mindfulness guidance.

These tools are used by the Mental Wellness Agent via Google ADK.
"""
from typing import Dict, List, Any, Optional
from src.utils.observability import trace_tool


@trace_tool
def assess_stress_level(
    stress_rating: int,
    sleep_quality: str = "average",
    work_hours_per_day: int = 8,
    exercise_frequency: int = 0,
    social_connections: str = "moderate"
) -> Dict[str, Any]:
    """
    Assess user's current stress level and contributing factors.
    
    Args:
        stress_rating: Self-reported stress level (1-10)
        sleep_quality: "poor", "average", "good"
        work_hours_per_day: Hours worked per day
        exercise_frequency: Days per week exercising
        social_connections: "low", "moderate", "high"
    
    Returns:
        Stress assessment with recommendations
    """
    stress_factors = []
    recommendations = []
    
    # Analyze stress rating
    if stress_rating >= 8:
        stress_level = "high"
        stress_factors.append("High self-reported stress")
        recommendations.append("Consider professional support if stress persists")
    elif stress_rating >= 5:
        stress_level = "moderate"
        stress_factors.append("Moderate stress levels")
    else:
        stress_level = "low"
    
    # Sleep quality impact
    if sleep_quality == "poor":
        stress_factors.append("Poor sleep quality contributing to stress")
        recommendations.append("Prioritize sleep hygiene and aim for 7-8 hours")
    
    # Work-life balance
    if work_hours_per_day > 10:
        stress_factors.append("Long work hours")
        recommendations.append("Set boundaries and take regular breaks")
    
    # Exercise
    if exercise_frequency < 2:
        stress_factors.append("Insufficient physical activity")
        recommendations.append("Aim for 3-4 days of exercise per week")
    
    # Social connections
    if social_connections == "low":
        stress_factors.append("Limited social support")
        recommendations.append("Nurture relationships and seek social connections")
    
    return {
        "stress_level": stress_level,
        "stress_rating": stress_rating,
        "contributing_factors": stress_factors,
        "recommendations": recommendations,
        "immediate_actions": [
            "Take 5 deep breaths",
            "Step outside for fresh air",
            "Drink water and stretch"
        ]
    }


@trace_tool
def recommend_mindfulness_practice(
    available_time_minutes: int = 10,
    experience_level: str = "beginner",
    preferred_style: str = "breathing"
) -> Dict[str, Any]:
    """
    Recommend appropriate mindfulness practice based on user preferences.
    
    Args:
        available_time_minutes: Time available for practice
        experience_level: "beginner", "intermediate", "advanced"
        preferred_style: "breathing", "meditation", "body_scan", "movement"
    
    Returns:
        Personalized mindfulness practice recommendation
    """
    practices = {
        "breathing": {
            "beginner": {
                "name": "Box Breathing",
                "duration": 5,
                "steps": [
                    "Inhale through nose for 4 counts",
                    "Hold breath for 4 counts",
                    "Exhale through mouth for 4 counts",
                    "Hold empty for 4 counts",
                    "Repeat 4-5 times"
                ]
            },
            "intermediate": {
                "name": "4-7-8 Breathing",
                "duration": 10,
                "steps": [
                    "Inhale through nose for 4 counts",
                    "Hold breath for 7 counts",
                    "Exhale completely through mouth for 8 counts",
                    "Repeat 8-10 times"
                ]
            },
            "advanced": {
                "name": "Alternate Nostril Breathing",
                "duration": 15,
                "steps": [
                    "Close right nostril, inhale left for 4 counts",
                    "Hold both closed for 4 counts",
                    "Close left nostril, exhale right for 4 counts",
                    "Inhale right for 4 counts",
                    "Hold both for 4 counts",
                    "Exhale left for 4 counts",
                    "Repeat 10-15 cycles"
                ]
            }
        },
        "meditation": {
            "beginner": {
                "name": "Guided Mindfulness Meditation",
                "duration": 10,
                "steps": [
                    "Sit comfortably with eyes closed",
                    "Focus on your breath naturally flowing",
                    "When mind wanders, gently return to breath",
                    "Continue for 10 minutes"
                ]
            },
            "intermediate": {
                "name": "Loving-Kindness Meditation",
                "duration": 15,
                "steps": [
                    "Sit comfortably and close eyes",
                    "Think of someone you love, send them well-wishes",
                    "Extend wishes to yourself",
                    "Extend to neutral person, then difficult person",
                    "Extend to all beings",
                    "Continue for 15 minutes"
                ]
            },
            "advanced": {
                "name": "Vipassana Meditation",
                "duration": 30,
                "steps": [
                    "Sit in meditation posture",
                    "Observe sensations throughout body",
                    "Note arising and passing of sensations",
                    "Maintain equanimity",
                    "Continue for 30 minutes"
                ]
            }
        },
        "body_scan": {
            "beginner": {
                "name": "Progressive Muscle Relaxation",
                "duration": 10,
                "steps": [
                    "Lie down comfortably",
                    "Tense and relax each muscle group",
                    "Start with feet, move up to head",
                    "Hold tension 5 seconds, release 10 seconds"
                ]
            },
            "intermediate": {
                "name": "Full Body Scan",
                "duration": 20,
                "steps": [
                    "Lie down and close eyes",
                    "Bring awareness to each body part",
                    "Start at toes, slowly move to head",
                    "Notice sensations without judgment",
                    "Spend 20 minutes scanning entire body"
                ]
            },
            "advanced": {
                "name": "Yoga Nidra",
                "duration": 30,
                "steps": [
                    "Lie in savasana",
                    "Set intention (sankalpa)",
                    "Rotate consciousness through body parts",
                    "Visualize images and sensations",
                    "Return to intention",
                    "Slowly return to awareness"
                ]
            }
        },
        "movement": {
            "beginner": {
                "name": "Mindful Walking",
                "duration": 10,
                "steps": [
                    "Walk slowly and deliberately",
                    "Notice each foot lifting and placing",
                    "Feel connection with ground",
                    "Observe surroundings without judgment",
                    "Continue for 10 minutes"
                ]
            },
            "intermediate": {
                "name": "Gentle Yoga Flow",
                "duration": 20,
                "steps": [
                    "Start with mountain pose",
                    "Flow through sun salutations",
                    "Hold each pose for 5 breaths",
                    "Focus on breath-movement connection",
                    "End with savasana"
                ]
            },
            "advanced": {
                "name": "Qigong Practice",
                "duration": 30,
                "steps": [
                    "Begin with standing meditation",
                    "Perform flowing movements",
                    "Coordinate breath with movement",
                    "Cultivate qi energy",
                    "End with meditation"
                ]
            }
        }
    }
    
    practice = practices.get(preferred_style, practices["breathing"]).get(
        experience_level, 
        practices["breathing"]["beginner"]
    )
    
    return {
        "practice_name": practice["name"],
        "duration_minutes": practice["duration"],
        "steps": practice["steps"],
        "experience_level": experience_level,
        "style": preferred_style,
        "benefits": [
            "Reduces stress and anxiety",
            "Improves focus and clarity",
            "Enhances emotional regulation",
            "Promotes relaxation"
        ],
        "tips": [
            "Find a quiet space",
            "Set a timer",
            "Be patient with yourself",
            "Practice regularly for best results"
        ]
    }


@trace_tool
def generate_relaxation_routine(
    daily_schedule: str = "morning",
    stress_triggers: Optional[List[str]] = None,
    time_available: int = 15
) -> Dict[str, Any]:
    """
    Generate a personalized daily relaxation routine.
    
    Args:
        daily_schedule: "morning", "midday", "evening", "bedtime"
        stress_triggers: List of known stress triggers
        time_available: Minutes available for routine
    
    Returns:
        Complete relaxation routine with timing
    """
    stress_triggers = stress_triggers or ["work", "deadlines"]
    
    routines = {
        "morning": {
            "name": "Morning Mindfulness Routine",
            "activities": [
                {"activity": "Gentle stretching", "duration": 5, "description": "Wake up body gently"},
                {"activity": "Breathing exercise", "duration": 5, "description": "Box breathing or 4-7-8"},
                {"activity": "Gratitude practice", "duration": 3, "description": "List 3 things you're grateful for"},
                {"activity": "Intention setting", "duration": 2, "description": "Set positive intention for the day"}
            ],
            "benefits": "Starts day with calm, focused energy"
        },
        "midday": {
            "name": "Midday Reset Routine",
            "activities": [
                {"activity": "Step outside", "duration": 3, "description": "Get fresh air and sunlight"},
                {"activity": "Mindful breathing", "duration": 5, "description": "Deep belly breathing"},
                {"activity": "Body scan", "duration": 5, "description": "Release tension in shoulders, neck, jaw"},
                {"activity": "Hydration break", "duration": 2, "description": "Drink water mindfully"}
            ],
            "benefits": "Recharges energy and reduces afternoon stress"
        },
        "evening": {
            "name": "Evening Wind-Down Routine",
            "activities": [
                {"activity": "Gentle movement", "duration": 5, "description": "Light yoga or stretching"},
                {"activity": "Journaling", "duration": 5, "description": "Reflect on the day"},
                {"activity": "Meditation", "duration": 10, "description": "Loving-kindness or gratitude meditation"},
                {"activity": "Digital detox", "duration": 0, "description": "Turn off screens 1 hour before bed"}
            ],
            "benefits": "Transitions from day to restful evening"
        },
        "bedtime": {
            "name": "Bedtime Relaxation Routine",
            "activities": [
                {"activity": "Progressive muscle relaxation", "duration": 10, "description": "Tense and release each muscle group"},
                {"activity": "Breathing exercise", "duration": 5, "description": "4-7-8 breathing for sleep"},
                {"activity": "Visualization", "duration": 5, "description": "Imagine peaceful scene"},
                {"activity": "Body scan", "duration": 5, "description": "Full body relaxation scan"}
            ],
            "benefits": "Prepares body and mind for deep sleep"
        }
    }
    
    routine = routines.get(daily_schedule, routines["morning"])
    
    # Adjust activities to fit available time
    total_duration = sum(act["duration"] for act in routine["activities"])
    if total_duration > time_available:
        # Scale down durations proportionally
        scale_factor = time_available / total_duration
        for activity in routine["activities"]:
            activity["duration"] = max(1, int(activity["duration"] * scale_factor))
    
    return {
        "routine_name": routine["name"],
        "schedule": daily_schedule,
        "total_duration_minutes": sum(act["duration"] for act in routine["activities"]),
        "activities": routine["activities"],
        "benefits": routine["benefits"],
        "stress_management_tips": [
            f"When facing {trigger}, take 3 deep breaths before responding" 
            for trigger in stress_triggers[:3]
        ],
        "consistency_tips": [
            "Set a daily reminder",
            "Start small and build gradually",
            "Track your practice",
            "Be compassionate with yourself"
        ]
    }
