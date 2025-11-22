"""
Sleep Agent - Specialized in sleep optimization and circadian rhythm guidance.

This agent uses ADK patterns with FunctionTool wrappers and output_key
for state management.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from google.adk.tools import FunctionTool
from src.agents.base_agent import create_health_agent
from config.prompts import SLEEP_AGENT_PROMPT
from src.tools import sleep_tools


def create_sleep_agent():
    """
    Create and configure the Sleep Agent using Google ADK.
    
    Returns:
        Configured ADK Agent for sleep optimization
    """
    
    # Wrap sleep tools with FunctionTool
    tools = [
        FunctionTool(sleep_tools.assess_sleep_quality),
        FunctionTool(sleep_tools.recommend_sleep_schedule),
        FunctionTool(sleep_tools.analyze_sleep_patterns)
    ]
    
    agent = create_health_agent(
        name="sleep_agent",
        instruction=SLEEP_AGENT_PROMPT,
        description="Specialist in sleep optimization, circadian rhythm guidance, and sleep hygiene. "
                   "Analyzes sleep patterns, creates personalized sleep schedules, and provides "
                   "evidence-based sleep improvement recommendations.",
        tools=tools,
        output_key="sleep_analysis",
        temperature=0.6
    )
    
    return agent


# Singleton instance
sleep_agent = create_sleep_agent()
