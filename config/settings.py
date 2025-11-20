"""
Global configuration settings for the Health & Wellness Coach
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # Project paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Google AI Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    PROJECT_ID = os.getenv("PROJECT_ID", "")
    LOCATION = os.getenv("LOCATION", "us-central1")
    
    # Model Configuration
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash-exp")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8192"))
    
    # Agent Configuration
    AGENT_CONFIG = {
        "coordinator": {
            "model": MODEL_NAME,
            "temperature": 0.7,
            "max_tokens": MAX_TOKENS
        },
        "nutrition": {
            "model": MODEL_NAME,
            "temperature": 0.5,  # More deterministic for calculations
            "max_tokens": MAX_TOKENS
        },
        "fitness": {
            "model": MODEL_NAME,
            "temperature": 0.6,
            "max_tokens": MAX_TOKENS
        },
        "sleep": {
            "model": MODEL_NAME,
            "temperature": 0.6,
            "max_tokens": MAX_TOKENS
        },
        "mental_wellness": {
            "model": MODEL_NAME,
            "temperature": 0.8,  # More creative for motivation
            "max_tokens": MAX_TOKENS
        }
    }
    
    # Observability
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENABLE_TRACING = os.getenv("ENABLE_TRACING", "true").lower() == "true"
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    
    # Health Parameters
    HEALTH_DEFAULTS = {
        "min_sleep_hours": 7.5,
        "max_sleep_hours": 9.0,
        "min_daily_calories": 1200,
        "max_daily_calories": 3500,
        "protein_per_kg": 1.6,  # grams per kg bodyweight
        "carb_per_kg": 3.0,
        "fat_per_kg": 0.8,
    }
    
    @classmethod
    def validate(cls):
        """Validate required settings"""
        # Create necessary directories
        cls.LOGS_DIR.mkdir(exist_ok=True, parents=True)
        cls.DATA_DIR.mkdir(exist_ok=True, parents=True)
        
        if not cls.GOOGLE_API_KEY:
            print("WARNING: GOOGLE_API_KEY not set. Please configure .env file.")

# Validate on import
Settings.validate()
