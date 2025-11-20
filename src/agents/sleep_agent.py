"""
Sleep Agent - Specialized in sleep quality and recovery
"""
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.base_agent import create_adk_agent
from config.prompts import SLEEP_AGENT_PROMPT
from src.tools import sleep_tools


def create_sleep_agent():
    """Create and configure the Sleep Agent using Google ADK"""
    
    # Get all sleep tool functions
    tools = [
        sleep_tools.assess_sleep_quality,
        sleep_tools.recommend_sleep_schedule,
        sleep_tools.analyze_sleep_patterns
    ]
    
    agent = create_adk_agent(
        name="Sleep Agent",
        instruction=SLEEP_AGENT_PROMPT,
        description="Specialist in sleep quality, recovery, and sleep schedule optimization",
        tools=tools
    )
    
    return agent


def analyze_sleep_workflow(
    agent,
    hours_slept: float,
    quality_factors: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute sleep quality analysis workflow
    
    Args:
        agent: Sleep agent instance
        hours_slept: Hours of sleep
        quality_factors: Dictionary with sleep quality factors
    
    Returns:
        Sleep analysis and recommendations
    """
    prompt = f"""Analyze this sleep data and provide recommendations:

Sleep Data:
- Hours Slept: {hours_slept}
- Times Woke Up: {quality_factors.get('times_woke_up', 0)}
- Time to Fall Asleep: {quality_factors.get('sleep_latency', 15)} minutes
- Felt Rested: {quality_factors.get('felt_rested', True)}
- Caffeine After 2pm: {quality_factors.get('caffeine_after_2pm', False)}
- Screen Time Before Bed: {quality_factors.get('screen_before_bed', False)}

Please:
1. Assess the overall sleep quality
2. Identify issues affecting sleep
3. Provide specific recommendations
4. Suggest an optimal sleep schedule

Use the available tools to assess sleep quality and recommend schedules."""

    response = agent.run(prompt)
    
    return {
        "response": response,
        "success": True
    }
