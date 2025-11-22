"""
Comprehensive test script for Health & Wellness Coach ADK application.
Tests all major functionality to identify and fix errors.
"""

import os
# Fix for SSL PermissionError
os.environ['SSLKEYLOGFILE'] = ''

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

async def test_nutrition_query():
    """Test nutrition-specific query."""
    print("\n=== Testing Nutrition Query ===")
    try:
        from src.core.runner_manager import runner_manager
        from src.agents.coordinator import coordinator_agent
        
        response = await runner_manager.run_query(
            agent=coordinator_agent,
            query="I want to lose weight. I'm 30 years old, 80kg, 180cm tall.",
            user_id="test_user",
            session_id="test_session_nutrition"
        )
        
        print(f"✓ Nutrition query executed")
        print(f"Response preview: {response[:150]}...")
        return True
    except Exception as e:
        print(f"✗ Nutrition query error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_nutrition_query())
