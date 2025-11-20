"""
Health Coordinator Agent - Main orchestrator
"""
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.base_agent import BaseAgent
from config.prompts import COORDINATOR_PROMPT
import logging


class HealthCoordinator(BaseAgent):
    """
    Main health coordinator that orchestrates specialized agents
    """
    
    def __init__(self, sub_agents: Dict[str, BaseAgent] = None):
        super().__init__(
            name="Health Coordinator",
            system_prompt=COORDINATOR_PROMPT,
            tools=[]
        )
        
        self.sub_agents = sub_agents or {}
        self.logger = logging.getLogger("HealthCoordinator")
        
        self.logger.info(f"Coordinator initialized with {len(self.sub_agents)} sub-agents")
    
    def route_request(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze request and route to appropriate agent(s)
        
        Args:
            user_input: User's message
            context: User context and history
        
        Returns:
            Routing decision with agent assignments
        """
        routing_prompt = f"""Analyze this user request and determine which specialist agents should handle it:

USER REQUEST: {user_input}

AVAILABLE AGENTS:
- nutrition_agent: Meal planning, macros, food recommendations
- fitness_agent: Workout programs, exercise guidance
- sleep_agent: Sleep quality, schedules, recovery
- mental_wellness_agent: Motivation, stress management, emotional support

Respond with JSON:
{{
  "primary_agent": "agent_name",
  "secondary_agents": ["agent_name"],
  "execution_mode": "sequential|parallel|single",
  "reasoning": "Why this routing"
}}

Return ONLY valid JSON."""

        try:
            if not self.model:
                return {
                    "primary_agent": "coordinator",
                    "secondary_agents": [],
                    "execution_mode": "single",
                    "reasoning": "No model configured"
                }
            
            response = self.model.generate_content(routing_prompt)
            result_text = response.text.strip()
            
            if result_text.startswith("```json"):
                result_text = result_text[7:-3]
            elif result_text.startswith("```"):
                result_text = result_text[3:-3]
            
            routing = json.loads(result_text)
            
            self.logger.info(f"Routing: {routing['primary_agent']} (mode: {routing['execution_mode']})")
            
            return routing
            
        except Exception as e:
            self.logger.error(f"Routing error: {e}")
            # Fallback to coordinator handling
            return {
                "primary_agent": "coordinator",
                "secondary_agents": [],
                "execution_mode": "single",
                "reasoning": "Routing failed, coordinator will handle directly"
            }
    
    def execute_workflow(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None,
        mode: str = "auto"
    ) -> Dict[str, Any]:
        """
        Execute complete workflow: routing → agent execution → synthesis
        
        Args:
            user_input: User's message
            context: User context
            mode: "auto" (intelligent routing) or specific mode
        
        Returns:
            Complete response with all agent outputs
        """
        # Step 1: Route request
        if mode == "auto":
            routing = self.route_request(user_input, context)
        else:
            routing = {
                "primary_agent": mode,
                "secondary_agents": [],
                "execution_mode": "single"
            }
        
        # Step 2: Execute agents
        agent_responses = {}
        
        execution_mode = routing.get("execution_mode", "single")
        
        if execution_mode == "single":
            # Single agent handles request
            agent_name = routing["primary_agent"]
            if agent_name in self.sub_agents:
                response = self.sub_agents[agent_name].process(user_input, context)
                agent_responses[agent_name] = response
            else:
                # Coordinator handles directly
                response = self.process(user_input, context)
                agent_responses["coordinator"] = response
        
        elif execution_mode == "parallel":
            # Multiple agents process simultaneously
            agents_to_call = [routing["primary_agent"]] + routing.get("secondary_agents", [])
            
            for agent_name in agents_to_call:
                if agent_name in self.sub_agents:
                    response = self.sub_agents[agent_name].process(user_input, context)
                    agent_responses[agent_name] = response
        
        elif execution_mode == "sequential":
            # Agents process in sequence, each building on previous
            agents_to_call = [routing["primary_agent"]] + routing.get("secondary_agents", [])
            
            accumulated_context = context.copy() if context else {}
            
            for agent_name in agents_to_call:
                if agent_name in self.sub_agents:
                    response = self.sub_agents[agent_name].process(user_input, accumulated_context)
                    agent_responses[agent_name] = response
                    
                    # Add response to context for next agent
                    accumulated_context[f"{agent_name}_response"] = response["response"]
        
        # Step 3: Synthesize responses
        final_response = self._synthesize_responses(
            user_input,
            agent_responses,
            context
        )
        
        return {
            "user_input": user_input,
            "routing": routing,
            "agent_responses": agent_responses,
            "final_response": final_response,
            "success": True
        }
    
    def _synthesize_responses(
        self,
        user_input: str,
        agent_responses: Dict[str, Dict],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Synthesize multiple agent responses into cohesive answer
        """
        if len(agent_responses) == 1:
            # Single agent - return response directly
            return list(agent_responses.values())[0]["response"]
        
        # Multiple agents - synthesize
        synthesis_prompt = f"""Synthesize these specialist responses into a cohesive answer for the user.

USER QUESTION: {user_input}

SPECIALIST RESPONSES:
"""
        
        for agent_name, response_data in agent_responses.items():
            synthesis_prompt += f"\n{agent_name.upper()}:\n{response_data['response']}\n"
        
        synthesis_prompt += """
Create a unified response that:
1. Addresses the user's question completely
2. Integrates insights from all specialists
3. Resolves any conflicts or contradictions
4. Provides clear, actionable guidance
5. Maintains a warm, supportive tone

Do not mention "the nutrition agent said" or reference agents. Present as unified guidance."""

        try:
            if self.model:
                response = self.model.generate_content(synthesis_prompt)
                return response.text
            else:
                return "\n\n".join([r["response"] for r in agent_responses.values()])
        except Exception as e:
            self.logger.error(f"Synthesis error: {e}")
            # Fallback: concatenate responses
            return "\n\n".join([r["response"] for r in agent_responses.values()])
