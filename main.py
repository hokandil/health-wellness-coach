"""
Personal Health & Wellness Coach - Interactive Mode (Google ADK)

Continuous conversation with your AI health coach.
"""

import sys
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.agents.coordinator import create_health_coordinator, execute_health_workflow
from src.memory.memory_bank import MemoryBank
from config.settings import Settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Interactive Health Coach - Continuous Conversation Mode"""
    print("\n" + "=" * 60)
    print("   🏥 PERSONAL HEALTH & WELLNESS COACH")
    print("   AI Multi-Agent System (Powered by Google ADK)")
    print("=" * 60)
    
    # Check API key
    if not Settings.GOOGLE_API_KEY:
        print("\n⚠️  WARNING: GOOGLE_API_KEY not set!")
        print("Please create a .env file with your Gemini API key.")
        print("Copy .env.example to .env and add your key.\n")
        return
    
    print("\n🏥 Initializing your AI Health Coach...")
    print("-" * 60)
    
    # Initialize coordinator with all sub-agents
    coordinator = create_health_coordinator()
    
    # Initialize memory bank
    memory_bank = MemoryBank()
    
    print("✅ Health Coach ready!")
    print(f"   - Specialized Agents: 4 (Nutrition, Fitness, Sleep, Mental Wellness)")
    print(f"   - Memory Bank: Active")
    print("=" * 60)
    
    # User profile (will be built during conversation)
    user_profile = None
    conversation_history = []
    
    print("\n💬 Welcome to your Personal Health & Wellness Coach!")
    print("\nI'm here to help you with:")
    print("  • Nutrition planning and meal guidance")
    print("  • Fitness programs and workout advice")
    print("  • Sleep quality and recovery optimization")
    print("  • Mental wellness and motivation")
    print("\nType 'quit' to exit, 'profile' to see your profile, 'clear' to start fresh.")
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
            
            if user_input.lower() == 'profile':
                if user_profile:
                    print(f"\n📋 Your Profile:")
                    for key, value in user_profile.items():
                        if key != 'preferences':
                            print(f"   {key.replace('_', ' ').title()}: {value}")
                else:
                    print("\n⚠️  No profile created yet. Share your health goals to build your profile!")
                print()
                continue
            
            if user_input.lower() == 'clear':
                conversation_history = []
                user_profile = None
                print("\n🔄 Conversation cleared. Let's start fresh!\n")
                continue
            
            if user_input.lower() == 'help':
                print("\n📚 Available Commands:")
                print("   quit - Exit the program")
                print("   profile - View your health profile")
                print("   clear - Clear conversation history and start fresh")
                print("   help - Show this help message")
                print("   Or just chat naturally with your health coach!\n")
                continue
            
            # Add to conversation history
            conversation_history.append({"role": "user", "content": user_input})
            
            # Build context with conversation history
            context = {
                "user_profile": user_profile,
                "conversation_history": conversation_history[-5:]  # Last 5 exchanges
            }
            
            # Process with coordinator
            print("\n🤖 Coach: ", end="", flush=True)
            result = execute_health_workflow(
                coordinator=coordinator,
                user_input=user_input,
                context=context
            )
            
            response = result['final_response']
            print(response)
            print()
            
            # Add to conversation history
            conversation_history.append({"role": "assistant", "content": response})
            
            # Try to extract profile information from first few interactions
            if not user_profile and len(conversation_history) <= 10:
                # Simple profile extraction (can be enhanced)
                if any(word in user_input.lower() for word in ['lose weight', 'gain muscle', 'get fit']):
                    if not user_profile:
                        user_profile = {}
                    if 'lose weight' in user_input.lower():
                        user_profile['primary_goal'] = 'lose_weight'
                    elif 'gain muscle' in user_input.lower():
                        user_profile['primary_goal'] = 'build_muscle'
                    elif 'get fit' in user_input.lower():
                        user_profile['primary_goal'] = 'general_fitness'
                    
                    # Save to memory bank
                    memory_bank.update_user_profile("user_001", user_profile)
            
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using Health Coach! Stay healthy!")
            break
        except Exception as e:
            logger.error(f"Error in conversation: {e}")
            print(f"\n❌ Sorry, I encountered an error: {str(e)}")
            print("Let's try again!\n")


if __name__ == "__main__":
    main()
