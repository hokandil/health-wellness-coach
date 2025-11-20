"""
Health Coordinator Agent - Main orchestrator using Bytez API
"""
from typing import Dict, Any, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from config.prompts import COORDINATOR_PROMPT
import logging


def create_health_coordinator():
    """
    Create the Health Coordinator (simplified for Bytez API)
    
    Returns:
        Coordinator configuration
    """
    logger = logging.getLogger("HealthCoordinator")
    logger.info("Health Coordinator initialized for Bytez API")
    
    return {
        "name": "health_coordinator",
        "model": "google/gemini-2.5-flash",
        "instruction": COORDINATOR_PROMPT
    }


def execute_health_workflow(
    coordinator,
    user_input: str,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Execute a health coaching workflow using Bytez or Google API
    
    Automatically detects which API to use based on MODEL_NAME prefix:
    - "bytez/" prefix -> Use Bytez API
    - "google/" prefix -> Use Google API directly
    
    Args:
        coordinator: Health coordinator agent
        user_input: User's message or query
        context: Optional user context (profile, history, etc.)
    
    Returns:
        Complete response
    """
    import os
    
    # Build context-aware prompt
    if context:
        full_prompt = _build_prompt_with_context(user_input, context)
    else:
        full_prompt = user_input
    
    # Get model name from environment
    model_name = os.getenv("MODEL_NAME", "bytez/google/gemini-2.5-flash")
    
    from src.utils.observability import Tracer, log_api_call
    
    with Tracer("HealthWorkflow") as tracer:
        tracer.log_event("input_received", {"length": len(user_input)})
        
        try:
            # Detect API type from model prefix
            if model_name.startswith("bytez/"):
                # Use Bytez API
                result = _execute_with_bytez(model_name, full_prompt, user_input)
            elif model_name.startswith("google/"):
                # Use Google API directly
                result = _execute_with_google(model_name, full_prompt, user_input)
            else:
                # Default to Bytez if no prefix
                result = _execute_with_bytez(f"bytez/{model_name}", full_prompt, user_input)
            
            tracer.log_event("execution_complete", {"success": result.get("success", False)})
            return result
                
        except Exception as e:
            logging.error(f"Error executing workflow: {e}")
            tracer.log_event("execution_error", {"error": str(e)})
            return {
                "user_input": user_input,
                "final_response": f"I apologize, but I encountered an error. Please try again.",
                "success": False
            }


def _execute_with_bytez(model_name: str, full_prompt: str, user_input: str) -> Dict[str, Any]:
    """Execute using Bytez API"""
    from bytez import Bytez
    import os
    from src.utils.observability import log_api_call
    
    # Remove "bytez/" prefix for actual model name
    actual_model = model_name.replace("bytez/", "")
    
    # Get API key
    api_key = os.getenv("BYTEZ_API_KEY")
    if not api_key:
        return {
            "user_input": user_input,
            "final_response": "No BYTEZ_API_KEY configured. Please set it in your .env file.",
            "success": False
        }
    
    # Initialize Bytez SDK
    sdk = Bytez(api_key)
    model = sdk.model(actual_model)
    
    # Prepare messages
    messages = [
        {"role": "system", "content": COORDINATOR_PROMPT},
        {"role": "user", "content": full_prompt}
    ]
    
    # Send to model
    response = model.run(messages)
    
    # Log API call (estimated tokens for now)
    log_api_call("Bytez", actual_model, len(full_prompt)//4, 0)
    
    # Check for error in response object
    if hasattr(response, 'error') and response.error:
        logging.error(f"Bytez API error: {response.error}")
        return {
            "user_input": user_input,
            "final_response": f"I apologize, but I encountered an error: {response.error}",
            "success": False
        }
    
    # Extract content from response
    output_text = ""
    if hasattr(response, 'output'):
        if isinstance(response.output, dict) and 'content' in response.output:
            output_text = response.output['content']
        else:
            output_text = str(response.output)
    else:
        # Fallback for tuple unpacking if behavior changes
        try:
            output, error = response
            if error:
                return {
                    "user_input": user_input,
                    "final_response": f"Error: {error}",
                    "success": False
                }
            output_text = output
        except:
            output_text = str(response)
            
    return {
        "user_input": user_input,
        "final_response": output_text,
        "success": True
    }


def _execute_with_google(model_name: str, full_prompt: str, user_input: str) -> Dict[str, Any]:
    """Execute using Google API directly"""
    from google import genai
    import os
    from src.utils.observability import log_api_call
    
    # Remove "google/" prefix for actual model name
    actual_model = model_name.replace("google/", "")
    
    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {
            "user_input": user_input,
            "final_response": "No GOOGLE_API_KEY configured. Please set it in your .env file.",
            "success": False
        }
    
    # Initialize Google client
    client = genai.Client(api_key=api_key)
    
    # Generate response
    response = client.models.generate_content(
        model=actual_model,
        contents=f"{COORDINATOR_PROMPT}\n\n{full_prompt}"
    )
    
    # Log API call
    log_api_call("Google", actual_model, len(full_prompt)//4, len(response.text)//4)
    
    return {
        "user_input": user_input,
        "final_response": response.text,
        "success": True
    }


def _build_prompt_with_context(
    user_input: str,
    context: Optional[Dict[str, Any]] = None
) -> str:
    """Build complete prompt with user context"""
    prompt_parts = []
    
    if context:
        prompt_parts.append("CONTEXT:")
        
        if "user_profile" in context and context["user_profile"] is not None:
            profile = context["user_profile"]
            prompt_parts.append(f"""
User Profile:
- Age: {profile.get('age', 'N/A')}
- Gender: {profile.get('gender', 'N/A')}
- Current Weight: {profile.get('current_weight_kg', 'N/A')}kg
- Goals: {', '.join(profile.get('goals', []))}
- Restrictions: {', '.join(profile.get('restrictions', []))}
""")
        
        if "conversation_history" in context and context["conversation_history"]:
            history = context["conversation_history"]
            prompt_parts.append("\nRecent Conversation:")
            for exchange in history[-3:]:  # Last 3 exchanges
                role = exchange.get("role", "unknown")
                content = exchange.get("content", "")
                prompt_parts.append(f"{role.title()}: {content[:100]}...")
        
        prompt_parts.append("\n---\n")
    
    prompt_parts.append(f"USER REQUEST:\n{user_input}")
    
    return "\n".join(prompt_parts)
