"""
Health Coordinator Agent - Main orchestrator using ADK AgentTool for LLM-based routing.

This coordinator uses AgentTool to wrap specialized agents and lets the LLM
decide which agent to route queries to, eliminating manual routing logic.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from google.adk.tools import AgentTool
from src.agents.base_agent import create_health_agent
from config.prompts import COORDINATOR_PROMPT

# Import specialized agents
from src.agents.nutrition_agent import nutrition_agent
from src.agents.fitness_agent import fitness_agent
from src.agents.sleep_agent import sleep_agent
from src.agents.mental_wellness_agent import mental_wellness_agent


def create_coordinator_agent():
    """
    Create the Health Coordinator with LLM-based routing using AgentTool.
    
    The coordinator uses AgentTool to wrap specialized agents, allowing the LLM
    to intelligently route queries to the appropriate specialist based on the
    user's request.
    
    Returns:
        Configured ADK Agent for health coordination
    """
    
    # Wrap specialized agents with AgentTool
    # AgentTool allows the LLM to invoke sub-agents as tools
    tools = [
        AgentTool(agent=nutrition_agent),
        AgentTool(agent=fitness_agent),
        AgentTool(agent=sleep_agent),
        AgentTool(agent=mental_wellness_agent)
    ]
    
    # Enhanced coordinator instruction for LLM-based routing
    enhanced_instruction = f"""{COORDINATOR_PROMPT}

## Agent Routing Guidelines

You have access to four specialized agents via tools:
1. **nutrition_specialist**: For all nutrition, diet, meal planning, and calorie-related queries
2. **fitness_specialist**: For all exercise, workout, and fitness-related queries
3. **sleep_specialist**: For all sleep quality, schedule, and rest-related queries
4. **wellness_specialist**: For all mental health, stress, and mindfulness-related queries

**Routing Strategy:**
- Analyze the user's query to determine which specialist(s) can best help
- Use the appropriate specialist tool to get expert advice
- For multi-domain queries (e.g., "help me lose weight"), coordinate between specialists
- For general greetings or simple questions, respond directly without invoking specialists
- Always provide a cohesive, personalized response that integrates specialist advice

**Important:**
- Let the specialists handle domain-specific calculations and recommendations
- Synthesize specialist responses into a coherent, actionable plan for the user
- Maintain conversation context and user preferences across interactions
"""
    
    agent = create_health_agent(
        name="health_coordinator",
        instruction=enhanced_instruction,
        description="Main health coaching coordinator that routes queries to specialized agents "
                   "for nutrition, fitness, sleep, and mental wellness guidance. Provides "
                   "comprehensive, personalized health coaching by coordinating specialist advice.",
        tools=tools,
        temperature=0.7
    )
    
    return agent


# Singleton instance
coordinator_agent = create_coordinator_agent()
