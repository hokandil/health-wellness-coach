"""
Personal Health & Wellness Coach - Interactive Mode (Google ADK)

Continuous conversation with your AI health coach using ADK architecture.
"""

# Fix for SSL permission error with antivirus software
import os
os.environ['SSLKEYLOGFILE'] = ''

import sys
import asyncio
import uuid
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.core.runner_manager import runner_manager
from src.agents.coordinator import coordinator_agent
from src.config import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def interactive_chat():
    """Interactive Health Coach - Continuous Conversation Mode"""
    print("\n" + "=" * 60)
    print("   🏥 PERSONAL HEALTH & WELLNESS COACH")
    print("   AI Multi-Agent System (Powered by Google ADK)")
    print("=" * 60)
    
    print("\n🏥 Initializing your AI Health Coach...")
    print("-" * 60)
    
    # Generate user and session IDs
    user_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    
    print("✅ Health Coach ready!")
    print(f"   - AI Model: {config.MODEL_NAME}")
    print(f"   - Session Management: {'Persistent' if config.USE_PERSISTENT_SESSIONS else 'In-Memory'}")
    print(f"   - Session ID: {session_id[:8]}...")
    print("=" * 60)
    
    print("\n💬 Welcome to your Personal Health & Wellness Coach!")
    print("\nI'm here to help you with:")
    print("  • Nutrition planning and meal guidance")
    print("  • Fitness programs and workout advice")
    print("  • Sleep quality and recovery optimization")
    print("  • Mental wellness and motivation")
    print("\nType 'quit' to exit, 'history' to see conversation history, 'clear' to start fresh.")
    print("Let's get started!\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == 'quit':
                print("\n👋 Thank you for using Health Coach! Stay healthy!")
                break
            
            if user_input.lower() == 'history':
                history = await runner_manager.get_session_history(session_id, limit=10)
                if history:
                    print("\n📜 Recent Conversation History:")
                    for msg in history[-10:]:
                        role = msg.get('role', 'unknown')
                        content = msg.get('content', '')
                        print(f"   {role.upper()}: {content[:100]}...")
                else:
                    print("\n⚠️  No conversation history yet.")
                print()
                continue
            
            if user_input.lower() == 'clear':
                await runner_manager.clear_session(session_id)
                session_id = str(uuid.uuid4())  # New session
                print(f"\n🔄 Conversation cleared. New session started: {session_id[:8]}...\n")
                continue
            
            if user_input.lower() == 'help':
                print("\n📚 Available Commands:")
                print("   quit - Exit the program")
                print("   history - View recent conversation history")
                print("   clear - Clear conversation history and start fresh")
                print("   metrics - Show health metrics (if enabled)")
                print("   help - Show this help message")
                print("   Or just chat naturally with your health coach!\n")
                continue
            
            if user_input.lower() == 'metrics':
                metrics = runner_manager.get_metrics()
                if metrics:
                    print("\n📊 Health Metrics:")
                    for plugin_name, plugin_metrics in metrics.items():
                        print(f"\n   {plugin_name}:")
                        for key, value in plugin_metrics.items():
                            print(f"      {key}: {value}")
                else:
                    print("\n⚠️  No metrics available.")
                print()
                continue
            
            # Process query through coordinator agent
            print("\n🤔 Coach: ", end="", flush=True)
            
            try:
                response = await runner_manager.run_query(
                    agent=coordinator_agent,
                    query=user_input,
                    user_id=user_id,
                    session_id=session_id
                )
                
                print(response)
                print()
                
            except Exception as e:
                logger.error(f"Error processing query: {e}", exc_info=True)
                print(f"\n❌ Sorry, I encountered an error: {str(e)}")
                print("Please try rephrasing your question or type 'help' for assistance.\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Thank you for using Health Coach!")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            print(f"\n❌ An unexpected error occurred: {str(e)}\n")


def main():
    """Main entry point"""
    try:
        asyncio.run(interactive_chat())
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
