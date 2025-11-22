"""Configuration module for Health & Wellness Coach."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    # Project paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    # API Configuration
    BYTEZ_API_KEY = os.getenv("BYTEZ_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # Model Configuration
    MODEL_NAME = os.getenv("MODEL_NAME", "bytez/google/gemini-2.5-flash")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8192"))
    
    # ADK Session Management
    USE_PERSISTENT_SESSIONS = os.getenv("USE_PERSISTENT_SESSIONS", "true").lower() == "true"
    SESSION_DB_URL = os.getenv("SESSION_DB_URL", "sqlite:///data/sessions.db")
    
    # Observability
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENABLE_TRACING = os.getenv("ENABLE_TRACING", "true").lower() == "true"
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    ENABLE_HEALTH_METRICS = os.getenv("ENABLE_HEALTH_METRICS", "true").lower() == "true"
    
    # Jaeger Configuration
    JAEGER_ENDPOINT = os.getenv("JAEGER_ENDPOINT", "http://localhost:4317")
    
    # ADK Web UI
    ADK_WEB_PORT = int(os.getenv("ADK_WEB_PORT", "8080"))
    ADK_WEB_HOST = os.getenv("ADK_WEB_HOST", "localhost")
    
    # Deployment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    @classmethod
    def validate(cls):
        """Validate required settings and create necessary directories."""
        cls.LOGS_DIR.mkdir(exist_ok=True, parents=True)
        cls.DATA_DIR.mkdir(exist_ok=True, parents=True)
        
        if not cls.BYTEZ_API_KEY and not cls.GOOGLE_API_KEY:
            print("WARNING: Neither BYTEZ_API_KEY nor GOOGLE_API_KEY is set. Please configure .env file.")


# Singleton instance
config = Config()

# Validate on import
config.validate()
