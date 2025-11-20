"""
Base agent class with common functionality
"""
import google.generativeai as genai
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import Settings
import logging


class BaseAgent:
    """Base class for all specialized agents"""
    
    def __init__(
        self,
        name: str,
        system_prompt: str,
        tools: List[Dict] = None,
        model_config: Dict = None
    ):
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.logger = logging.getLogger(name)
        
        # Model configuration
        config = model_config or Settings.AGENT_CONFIG.get(
            name.lower().replace(" ", "_").replace("agent", "").strip("_"),
            Settings.AGENT_CONFIG["coordinator"]
        )
        
        # Initialize Gemini model
        if Settings.GOOGLE_API_KEY:
            genai.configure(api_key=Settings.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(
                model_name=config["model"],
                generation_config={
                    "temperature": config["temperature"],
                    "max_output_tokens": config["max_tokens"]
                },
                system_instruction=system_prompt
            )
        else:
            self.model = None
            self.logger.warning(f"{self.name}: No API key configured")
        
        self.logger.info(f"{self.name} initialized with {len(self.tools)} tools")
    
    def process(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process user input and return response
        
        Args:
            user_input: User's message or query
            context: Additional context (user profile, history, etc.)
        
        Returns:
            Agent's response with metadata
        """
        if not self.model:
            return {
                "agent": self.name,
                "response": "Agent not configured. Please set GOOGLE_API_KEY in .env file.",
                "success": False,
                "error": "No API key"
            }
        
        try:
            # Build prompt with context
            full_prompt = self._build_prompt(user_input, context)
            
            self.logger.debug(f"Processing: {user_input[:100]}...")
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            return {
                "agent": self.name,
                "response": response.text,
                "success": True,
                "metadata": {
                    "model": self.model.model_name,
                    "prompt_length": len(full_prompt)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error processing request: {str(e)}")
            return {
                "agent": self.name,
                "response": f"I encountered an error: {str(e)}",
                "success": False,
                "error": str(e)
            }
    
    def _build_prompt(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build complete prompt with context"""
        prompt_parts = []
        
        if context:
            prompt_parts.append("CONTEXT:")
            
            if "user_profile" in context:
                profile = context["user_profile"]
                prompt_parts.append(f"""
User Profile:
- Age: {profile.get('age', 'N/A')}
- Gender: {profile.get('gender', 'N/A')}
- Current Weight: {profile.get('current_weight_kg', 'N/A')}kg
- Goals: {', '.join(profile.get('goals', []))}
- Restrictions: {', '.join(profile.get('restrictions', []))}
""")
            
            if "recent_history" in context:
                prompt_parts.append(f"\nRecent History:\n{context['recent_history']}")
            
            prompt_parts.append("\n---\n")
        
        prompt_parts.append(f"USER REQUEST:\n{user_input}")
        
        return "\n".join(prompt_parts)
    
    def call_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool by name"""
        for tool in self.tools:
            if tool["name"] == tool_name:
                self.logger.info(f"Calling tool: {tool_name}")
                return tool["function"](**kwargs)
        
        raise ValueError(f"Tool '{tool_name}' not found in {self.name}")
