"""
Sleep-related tools for sleep quality analysis and recommendations

These tools are used by the Sleep Agent via Google ADK.
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta


def assess_sleep_quality(
    hours_slept: float,
    times_woke_up: int = 0,
    time_to_fall_asleep_minutes: int = 15,
    felt_rested: bool = True,
    caffeine_after_2pm: bool = False,
    screen_time_before_bed: bool = False
) -> Dict[str, Any]:
    """
    Assess sleep quality based on various factors
    
    Args:
        hours_slept: Total hours of sleep
        times_woke_up: Number of times woke during night
        time_to_fall_asleep_minutes: Sleep latency
        felt_rested: Did user feel rested upon waking
        caffeine_after_2pm: Had caffeine after 2 PM
        screen_time_before_bed: Used screens within 1 hour of bed
    
    Returns:
        Sleep quality assessment and recommendations
    """
    score = 10.0  # Start with perfect score
    issues = []
    recommendations = []
    
    # Sleep duration
    if hours_slept < 6:
        score -= 3.0
        issues.append("Severely insufficient sleep duration")
        recommendations.append("Aim for at least 7.5 hours. Set earlier bedtime.")
    elif hours_slept < 7:
        score -= 1.5
        issues.append("Below recommended sleep duration")
        recommendations.append("Try to get 7.5-8 hours for optimal recovery.")
    elif hours_slept > 9.5:
        score -= 0.5
        issues.append("Possibly oversleeping")
        recommendations.append("Consistent wake time helps regulate circadian rhythm.")
    
    # Sleep continuity
    if times_woke_up > 3:
        score -= 2.0
        issues.append("Frequent nighttime awakenings")
        recommendations.append("Avoid fluids 2 hours before bed. Check room temperature (65-68°F optimal).")
    elif times_woke_up > 1:
        score -= 1.0
        issues.append("Some sleep disruption")
    
    # Sleep latency
    if time_to_fall_asleep_minutes > 30:
        score -= 1.5
        issues.append("Difficulty falling asleep")
        recommendations.append("Try 10-minute wind-down routine: dim lights, no screens, light stretching.")
    
    # Subjective quality
    if not felt_rested:
        score -= 2.0
        issues.append("Poor subjective sleep quality")
        recommendations.append("Consider sleep study if this persists. May indicate sleep disorder.")
    
    # Sleep hygiene violations
    if caffeine_after_2pm:
        score -= 1.0
        issues.append("Late caffeine consumption")
        recommendations.append("Cut off caffeine by 2 PM. Half-life is 5-6 hours.")
    
    if screen_time_before_bed:
        score -= 1.0
        issues.append("Blue light exposure before bed")
        recommendations.append("Use blue light filters or avoid screens 1 hour before bed.")
    
    # Determine rating
    if score >= 9:
        rating = "Excellent"
    elif score >= 7:
        rating = "Good"
    elif score >= 5:
        rating = "Fair"
    else:
        rating = "Poor"
    
    return {
        "sleep_quality_score": max(score, 0),
        "rating": rating,
        "hours_slept": hours_slept,
        "target_hours": "7.5-8.5",
        "issues_identified": issues if issues else ["None - great sleep!"],
        "recommendations": recommendations if recommendations else ["Keep up the good sleep habits!"],
        "recovery_status": "Good" if score >= 7 else "Moderate" if score >= 5 else "Poor"
    }


def recommend_sleep_schedule(
    desired_wake_time: str,
    sleep_cycles_needed: int = 5
) -> Dict[str, Any]:
    """
    Recommend optimal bedtime based on sleep cycles
    
    Args:
        desired_wake_time: Target wake time (e.g., "06:30")
        sleep_cycles_needed: Number of 90-minute sleep cycles (default 5 = 7.5 hours)
    
    Returns:
        Recommended bedtime and schedule
    """
    # Parse wake time
    wake_hour, wake_minute = map(int, desired_wake_time.split(":"))
    wake_time = datetime.now().replace(hour=wake_hour, minute=wake_minute, second=0)
    
    # Each sleep cycle is ~90 minutes
    cycle_duration = timedelta(minutes=90)
    # Add 15 minutes to fall asleep
    sleep_latency = timedelta(minutes=15)
    
    # Calculate bedtime
    sleep_duration = cycle_duration * sleep_cycles_needed
    bedtime = wake_time - sleep_duration - sleep_latency
    
    # Alternative options (4 or 6 cycles)
    bedtime_6_cycles = wake_time - (cycle_duration * 6) - sleep_latency
    bedtime_4_cycles = wake_time - (cycle_duration * 4) - sleep_latency
    
    return {
        "wake_time": desired_wake_time,
        "recommended_bedtime": bedtime.strftime("%H:%M"),
        "total_sleep_hours": sleep_cycles_needed * 1.5,
        "sleep_cycles": sleep_cycles_needed,
        "alternatives": {
            "if_need_more_sleep": {
                "bedtime": bedtime_6_cycles.strftime("%H:%M"),
                "hours": 9.0,
                "cycles": 6
            },
            "if_time_limited": {
                "bedtime": bedtime_4_cycles.strftime("%H:%M"),
                "hours": 6.0,
                "cycles": 4,
                "warning": "Less than recommended minimum"
            }
        },
        "wind_down_start": (bedtime - timedelta(minutes=30)).strftime("%H:%M"),
        "notes": "Start winding down 30 min before bedtime. Dim lights, no screens, light stretching or reading."
    }


def analyze_sleep_patterns(
    sleep_log: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Analyze sleep patterns over time to identify trends
    
    Args:
        sleep_log: List of sleep records
            [{"date": "2024-11-10", "hours": 7.5, "quality": 8}, ...]
    
    Returns:
        Pattern analysis and insights
    """
    if not sleep_log:
        return {"error": "No sleep data provided"}
    
    # Calculate averages
    total_hours = sum(log.get("hours", 0) for log in sleep_log)
    avg_hours = total_hours / len(sleep_log)
    
    total_quality = sum(log.get("quality", 0) for log in sleep_log)
    avg_quality = total_quality / len(sleep_log) if total_quality > 0 else 0
    
    # Identify patterns
    days_under_7hrs = sum(1 for log in sleep_log if log.get("hours", 0) < 7)
    days_over_8hrs = sum(1 for log in sleep_log if log.get("hours", 0) > 8)
    
    # Trends
    if len(sleep_log) >= 7:
        recent_avg = sum(log.get("hours", 0) for log in sleep_log[-7:]) / 7
        older_avg = sum(log.get("hours", 0) for log in sleep_log[:7]) / 7
        trend = "improving" if recent_avg > older_avg + 0.3 else "declining" if recent_avg < older_avg - 0.3 else "stable"
    else:
        trend = "insufficient data"
    
    insights = []
    recommendations = []
    
    if avg_hours < 7:
        insights.append("Chronic sleep deprivation detected")
        recommendations.append("Prioritize sleep - aim for 7.5+ hours consistently")
    
    if days_under_7hrs > len(sleep_log) * 0.5:
        insights.append(f"Insufficient sleep on {days_under_7hrs}/{len(sleep_log)} days")
        recommendations.append("Set earlier bedtime alarm to build consistency")
    
    if trend == "declining":
        insights.append("Sleep duration declining over time")
        recommendations.append("Review recent life changes. What's disrupting your sleep routine?")
    
    return {
        "period_analyzed": f"{len(sleep_log)} days",
        "average_hours_per_night": round(avg_hours, 1),
        "average_quality_score": round(avg_quality, 1),
        "days_under_7hrs": days_under_7hrs,
        "days_over_8hrs": days_over_8hrs,
        "trend": trend,
        "insights": insights if insights else ["Sleep patterns look healthy!"],
        "recommendations": recommendations if recommendations else ["Maintain current sleep habits"]
    }
