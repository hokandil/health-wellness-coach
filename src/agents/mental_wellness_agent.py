"""
Mental Wellness Agent - Specialized in motivation and emotional support
"""
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.base_agent import BaseAgent
from config.prompts import MENTAL_WELLNESS_AGENT_PROMPT


class MentalWellnessAgent(BaseAgent):
    """Mental wellness specialist agent"""
    
    def __init__(self):
        super().__init__(
            name="Mental Wellness Agent",
            system_prompt=MENTAL_WELLNESS_AGENT_PROMPT,
            tools=[]  # Primarily conversational
        )
    
    def provide_motivation(
        self,
        user_context: Dict[str, Any],
        situation: str = "general"
    ) -> str:
        """Provide personalized motivation"""
        prompt = f"""Provide encouraging, personalized motivation for this user.

SITUATION: {situation}

USER CONTEXT:
- Current streak: {user_context.get('current_streak', 0)} days
- Recent challenges: {user_context.get('recent_challenges', 'None')}
- Recent wins: {user_context.get('recent_wins', 'None')}
- Progress: {user_context.get('progress_summary', 'Just starting')}

Create a warm, genuine message that acknowledges their effort, provides perspective, offers concrete next steps, and ends with encouragement."""

        if self.model:
            response = self.model.generate_content(prompt)
            return response.text
        return "Keep up the great work!"
