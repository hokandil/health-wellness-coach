import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "health_coach.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Observability")

# OpenTelemetry is configured in src/observability/telemetry.py
# and initialized in main.py
tracer = trace.get_tracer(__name__)

class Tracer:
    """OpenTelemetry wrapper for easy tracing"""
    
    def __init__(self, name: str):
        self.name = name
        self.span = None
        self.ctx_manager = None
        
    def __enter__(self):
        self.ctx_manager = tracer.start_as_current_span(self.name)
        self.span = self.ctx_manager.__enter__()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.span:
            if exc_type:
                self.span.record_exception(exc_val)
                self.span.set_status(trace.Status(trace.StatusCode.ERROR))
            else:
                self.span.set_status(trace.Status(trace.StatusCode.OK))
        # Exit the context manager properly
        if self.ctx_manager:
            self.ctx_manager.__exit__(exc_type, exc_val, exc_tb)
        
    def log_event(self, event_name: str, data: Dict[str, Any] = None):
        """Add event to the current span"""
        if self.span:
            self.span.add_event(event_name, attributes=data or {})

def log_api_call(provider: str, model: str, prompt_tokens: int = 0, completion_tokens: int = 0):
    """Log API usage metrics and add to current span"""
    logger.info(f"API Call - Provider: {provider} - Model: {model} - Input Tokens: {prompt_tokens} - Output Tokens: {completion_tokens}")
    
    current_span = trace.get_current_span()
    if current_span:
        current_span.set_attribute("llm.provider", provider)
        current_span.set_attribute("llm.model", model)
        current_span.set_attribute("llm.prompt_tokens", prompt_tokens)
        current_span.set_attribute("llm.completion_tokens", completion_tokens)

import functools

import functools
import inspect
import asyncio

def trace_tool(func):
    """Decorator to trace tool execution (sync and async)"""
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            with Tracer(f"Tool: {func.__name__}") as tracer:
                tracer.log_event("tool_start", {"args": str(args), "kwargs": str(kwargs)})
                try:
                    result = await func(*args, **kwargs)
                    tracer.log_event("tool_end", {"result": str(result)[:100] + "..." if len(str(result)) > 100 else str(result)})
                    return result
                except Exception as e:
                    tracer.log_event("tool_error", {"error": str(e)})
                    raise e
        return wrapper
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with Tracer(f"Tool: {func.__name__}") as tracer:
                tracer.log_event("tool_start", {"args": str(args), "kwargs": str(kwargs)})
                try:
                    result = func(*args, **kwargs)
                    tracer.log_event("tool_end", {"result": str(result)[:100] + "..." if len(str(result)) > 100 else str(result)})
                    return result
                except Exception as e:
                    tracer.log_event("tool_error", {"error": str(e)})
                    raise e
        return wrapper
