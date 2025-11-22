"""
Base agent factory for creating ADK agents with consistent configuration.

Provides `create_health_agent` to instantiate agents using Google Gemini models.
"""

import os
import logging
from typing import List, Optional, Callable

from google.adk.agents import Agent
from google.adk.models import LLMRegistry, Gemini

logger = logging.getLogger(__name__)

def _resolve_model_name(model_name: Optional[str]) -> str:
    """Return a model identifier compatible with the ADK registry.

    - If the name starts with ``google/`` we strip that prefix.
    - If it starts with ``models/`` we strip that prefix.
    - Otherwise we assume the caller supplied a valid registry name.
    """
    default = "gemini-2.5-flash"
    model = model_name or os.getenv("MODEL_NAME", default)
    if model.startswith("google/"):
        return model.replace("google/", "")
    if model.startswith("models/"):
        return model.replace("models/", "")
    return model

def create_health_agent(
    name: str,
    instruction: str,
    description: str,
    tools: Optional[List[Callable]] = None,
    output_key: Optional[str] = None,
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 8192,
) -> Agent:
    """Factory function to create ADK agents with consistent configuration.

    Args:
        name: Human‑readable agent name.
        instruction: System prompt for the agent.
        description: Brief description of the agent's role.
        tools: List of tool callables to expose to the agent.
        output_key: Session key for the agent's output.
        model_name: Optional override for the model identifier.
        temperature: Model temperature (0.0‑1.0).
        max_tokens: Maximum tokens for the response.

    Returns:
        Configured ADK ``Agent`` instance.
    """
    # ADK requires the agent name to be a valid Python identifier
    valid_name = name.lower().replace(" ", "_").replace("-", "_")

    actual_model = _resolve_model_name(model_name)
    logger.info("Creating ADK agent: %s with model %s", valid_name, actual_model)

    agent = Agent(
        name=valid_name,
        model=actual_model,
        instruction=instruction,
        tools=tools or [],
        output_key=output_key,
        description=description,
    )

    logger.info("%s initialized with %d tools, output_key=%s", valid_name, len(tools or []), output_key)
    return agent
