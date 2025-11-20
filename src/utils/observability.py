import logging
from pathlib import Path
from typing import Any, Dict, Optional
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.sdk.resources import Resource

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

# Configure OpenTelemetry
resource = Resource.create({"service.name": "health-wellness-coach"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# For development, export traces to console
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

class Tracer:
    """OpenTelemetry wrapper for easy tracing"""
    
    def __init__(self, name: str):
        self.name = name
        self.span = None
        
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
