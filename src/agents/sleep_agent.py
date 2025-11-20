"""
Sleep Agent - Specialized in sleep quality and recovery
"""
from typing import Dict, Any, List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.base_agent import BaseAgent
from config.prompts import SLEEP_AGENT_PROMPT
from src.tools.sleep_tools import SLEEP_TOOLS


class SleepAgent(BaseAgent):
    """Sleep specialist agent"""
    
    def __init__(self):
        super().__init__(
            name="Sleep Agent",
            system_prompt=SLEEP_AGENT_PROMPT,
            tools=SLEEP_TOOLS
        )
    
    def analyze_sleep(
        self,
        hours_slept: float,
        quality_factors: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze sleep quality"""
        assessment = self.call_tool(
            "assess_sleep_quality",
            hours_slept=hours_slept,
            times_woke_up=quality_factors.get("times_woke_up", 0),
            time_to_fall_asleep_minutes=quality_factors.get("sleep_latency", 15),
            felt_rested=quality_factors.get("felt_rested", True),
            caffeine_after_2pm=quality_factors.get("caffeine_after_2pm", False),
            screen_time_before_bed=quality_factors.get("screen_before_bed", False)
        )
        
        return assessment
