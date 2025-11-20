"""
Personal Health & Wellness Coach - Main Demo Application

This demonstrates the multi-agent health coaching system with:
- 4 specialized agents (Nutrition, Fitness, Sleep, Mental Wellness)
- Health Coordinator for orchestration
- Memory Bank for user profiles
- Multi-agent workflows (parallel, sequential, single)
"""

import sys
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.agents.coordinator import HealthCoordinator
from src.agents.nutrition_agent import NutritionAgent
from src.agents.fitness_agent import FitnessAgent
from src.agents.sleep_agent import SleepAgent
from src.agents.mental_wellness_agent import MentalWellnessAgent
from src.memory.memory_bank import MemoryBank
from config.settings import Settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def initialize_system():
    """Initialize the health coach system with all agents"""
    print("🏥 Initializing Personal Health & Wellness Coach...")
    print("=" * 60)
    
    # Check API key
    if not Settings.GOOGLE_API_KEY:
        print("\n⚠️  WARNING: GOOGLE_API_KEY not set!")
        print("Please create a .env file with your Gemini API key.")
        print("Copy .env.example to .env and add your key.\n")
        return None, None
    
    # Initialize specialized agents
    nutrition_agent = NutritionAgent()
    fitness_agent = FitnessAgent()
    sleep_agent = SleepAgent()
    mental_wellness_agent = MentalWellnessAgent()
    
    # Initialize coordinator with sub-agents
    coordinator = HealthCoordinator(sub_agents={
        "nutrition_agent": nutrition_agent,
        "fitness_agent": fitness_agent,
        "sleep_agent": sleep_agent,
        "mental_wellness_agent": mental_wellness_agent
    })
    
    # Initialize memory bank
    memory_bank = MemoryBank()
    
    print("✅ System initialized successfully!")
    print(f"   - Coordinator: {coordinator.name}")
    print(f"   - Specialized Agents: {len(coordinator.sub_agents)}")
    print(f"   - Memory Bank: Active")
    print("=" * 60)
    
    return coordinator, memory_bank


def demo_scenario_1_new_user():
    """Demo: New user onboarding"""
    print("\n📋 DEMO SCENARIO 1: New User Onboarding")
    print("-" * 60)
    
    coordinator, memory_bank = initialize_system()
    if not coordinator:
        return
    
    # Create sample user profile
    user_profile = {
        "age": 32,
        "gender": "male",
        "current_weight_kg": 82,
        "height_cm": 178,
        "activity_level": "moderate",
        "primary_goal": "lose_weight",
        "dietary_restrictions": ["lactose"],
        "preferences": {
            "liked_foods": ["chicken", "salmon", "broccoli", "quinoa"],
            "disliked_foods": ["brussels_sprouts"]
        },
        "fitness_goals": ["lose_weight", "build_muscle"],
        "training_days_per_week": 3,
        "available_equipment": ["bodyweight", "dumbbells"]
    }
    
    # Store user profile
    memory_bank.update_user_profile("user_001", user_profile)
    print("✅ User profile created and stored")
    
    # User request
    user_input = "Hi! I want to lose 15 pounds in 3 months. Can you help me create a plan?"
    
    print(f"\n👤 User: {user_input}")
    print("\n🤖 Processing with Health Coordinator...")
    
    # Execute workflow
    result = coordinator.execute_workflow(
        user_input=user_input,
        context={"user_profile": user_profile}
    )
    
    print(f"\n📊 Routing Decision:")
    print(f"   - Primary Agent: {result['routing']['primary_agent']}")
    print(f"   - Execution Mode: {result['routing']['execution_mode']}")
    
    print(f"\n💬 Response:")
    print(result['final_response'])


def demo_scenario_2_daily_checkin():
    """Demo: Daily check-in with parallel agent execution"""
    print("\n📋 DEMO SCENARIO 2: Daily Check-In (Parallel Execution)")
    print("-" * 60)
    
    coordinator, memory_bank = initialize_system()
    if not coordinator:
        return
    
    user_profile = memory_bank.get_user_profile("user_001")
    if not user_profile:
        print("⚠️  No user profile found. Run Scenario 1 first.")
        return
    
    user_input = """Good morning! Here's my daily check-in:
- Slept 6.5 hours last night
- Had coffee and toast for breakfast
- Feeling a bit tired
- Workout scheduled for 6 PM today"""
    
    print(f"\n👤 User: {user_input}")
    print("\n🤖 Processing with multiple agents in parallel...")
    
    result = coordinator.execute_workflow(
        user_input=user_input,
        context={"user_profile": user_profile}
    )
    
    print(f"\n📊 Agents Consulted: {list(result['agent_responses'].keys())}")
    print(f"\n💬 Synthesized Response:")
    print(result['final_response'])


def demo_scenario_3_tool_usage():
    """Demo: Direct tool usage"""
    print("\n📋 DEMO SCENARIO 3: Tool Usage Examples")
    print("-" * 60)
    
    from src.tools.nutrition_tools import calculate_daily_calories, calculate_macro_targets
    from src.tools.fitness_tools import calculate_calories_burned
    from src.tools.sleep_tools import assess_sleep_quality, recommend_sleep_schedule
    
    print("\n🍽️  Nutrition Tool: Calculate Daily Calories")
    calories = calculate_daily_calories(
        age=32,
        weight_kg=82,
        height_cm=178,
        gender="male",
        activity_level="moderate",
        goal="lose_weight"
    )
    print(f"   BMR: {calories['bmr']} cal")
    print(f"   TDEE: {calories['tdee']} cal")
    print(f"   Target (weight loss): {calories['target_calories']} cal")
    
    print("\n🍽️  Nutrition Tool: Calculate Macro Targets")
    macros = calculate_macro_targets(
        target_calories=calories['target_calories'],
        weight_kg=82,
        goal="lose_weight"
    )
    print(f"   Protein: {macros['protein']['grams']}g ({macros['protein']['percentage']}%)")
    print(f"   Carbs: {macros['carbs']['grams']}g ({macros['carbs']['percentage']}%)")
    print(f"   Fats: {macros['fats']['grams']}g ({macros['fats']['percentage']}%)")
    
    print("\n🏋️  Fitness Tool: Calculate Calories Burned")
    workout = calculate_calories_burned(
        activity="running",
        duration_minutes=30,
        weight_kg=82,
        intensity="moderate"
    )
    print(f"   Activity: {workout['activity']} ({workout['intensity']})")
    print(f"   Duration: {workout['duration_minutes']} minutes")
    print(f"   Calories Burned: {workout['calories_burned']} cal")
    
    print("\n😴 Sleep Tool: Assess Sleep Quality")
    sleep_assessment = assess_sleep_quality(
        hours_slept=6.5,
        times_woke_up=2,
        time_to_fall_asleep_minutes=20,
        felt_rested=False,
        caffeine_after_2pm=True,
        screen_time_before_bed=True
    )
    print(f"   Sleep Quality Score: {sleep_assessment['sleep_quality_score']}/10")
    print(f"   Rating: {sleep_assessment['rating']}")
    print(f"   Issues: {', '.join(sleep_assessment['issues_identified'][:2])}")
    
    print("\n😴 Sleep Tool: Recommend Sleep Schedule")
    schedule = recommend_sleep_schedule(
        desired_wake_time="06:30",
        sleep_cycles_needed=5
    )
    print(f"   Wake Time: {schedule['wake_time']}")
    print(f"   Recommended Bedtime: {schedule['recommended_bedtime']}")
    print(f"   Total Sleep: {schedule['total_sleep_hours']} hours ({schedule['sleep_cycles']} cycles)")


def interactive_mode():
    """Interactive chat mode"""
    print("\n💬 INTERACTIVE MODE")
    print("-" * 60)
    
    coordinator, memory_bank = initialize_system()
    if not coordinator:
        return
    
    # Try to load existing user profile
    user_profile = memory_bank.get_user_profile("user_001")
    
    print("\nYou can now chat with your health coach!")
    print("Type 'quit' to exit, 'profile' to see your profile, 'help' for commands.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'quit':
                print("\n👋 Goodbye! Stay healthy!")
                break
            
            if user_input.lower() == 'profile':
                if user_profile:
                    print(f"\n📋 Your Profile:")
                    print(f"   Age: {user_profile.get('age')}")
                    print(f"   Weight: {user_profile.get('current_weight_kg')}kg")
                    print(f"   Goal: {user_profile.get('primary_goal')}")
                else:
                    print("\n⚠️  No profile found. Create one by chatting with the coach!")
                continue
            
            if user_input.lower() == 'help':
                print("\n📚 Available Commands:")
                print("   quit - Exit the program")
                print("   profile - View your profile")
                print("   help - Show this help message")
                print("   Or just chat naturally with your health coach!\n")
                continue
            
            # Process with coordinator
            result = coordinator.execute_workflow(
                user_input=user_input,
                context={"user_profile": user_profile} if user_profile else None
            )
            
            print(f"\nCoach: {result['final_response']}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Stay healthy!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print("   🏥 PERSONAL HEALTH & WELLNESS COACH")
    print("   AI Multi-Agent System for Holistic Health Guidance")
    print("=" * 60)
    
    print("\nAvailable Demos:")
    print("1. New User Onboarding")
    print("2. Daily Check-In (Multi-Agent Parallel Execution)")
    print("3. Tool Usage Examples")
    print("4. Interactive Chat Mode")
    print("5. Run All Demos")
    print("0. Exit")
    
    choice = input("\nSelect demo (0-5): ").strip()
    
    if choice == "1":
        demo_scenario_1_new_user()
    elif choice == "2":
        demo_scenario_2_daily_checkin()
    elif choice == "3":
        demo_scenario_3_tool_usage()
    elif choice == "4":
        interactive_mode()
    elif choice == "5":
        demo_scenario_1_new_user()
        input("\nPress Enter to continue to next demo...")
        demo_scenario_2_daily_checkin()
        input("\nPress Enter to continue to next demo...")
        demo_scenario_3_tool_usage()
    elif choice == "0":
        print("\n👋 Goodbye!")
    else:
        print("\n❌ Invalid choice. Please run again and select 0-5.")


if __name__ == "__main__":
    main()
