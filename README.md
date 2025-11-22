# 🏥 Personal Health & Wellness Coach

An AI-powered multi-agent system for comprehensive health and wellness guidance. This project demonstrates advanced AI agent concepts using the **Google Agent Development Kit (ADK)** and **Google Gemini** models. It features multi-agent orchestration, tool usage, memory management, and agent-to-agent communication.

## 🎯 Project Overview

This health coach provides personalized guidance across four key wellness domains:
- **Nutrition**: Meal planning, macro calculations, dietary guidance
- **Fitness**: Workout programming, exercise recommendations
- **Sleep**: Sleep quality analysis, schedule optimization
- **Mental Wellness**: Motivation, stress management, emotional support

### Why Multi-Agent Architecture?

Health is multi-dimensional and interconnected. This system uses specialized agents that:
- Have deep expertise in their domain
- Coordinate through a Health Coordinator
- Negotiate balanced recommendations (e.g., nutrition + fitness alignment)
- Remember user preferences and progress over time

## 🏗️ Architecture

```
Health Coordinator (Orchestrator)
├── Nutrition Agent (Meal planning, macros)
├── Fitness Agent (Workouts, exercise)
├── Sleep Agent (Sleep quality, recovery)
└── Mental Wellness Agent (Motivation, support)

Tools Layer
├── Nutrition Tools (calorie calc, meal gen)
├── Fitness Tools (workout gen, calorie burn)
└── Sleep Tools (quality assessment, scheduling)

Memory Layer
└── Memory Bank (User profiles, progress tracking)
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to project directory
cd health-wellness-coach

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env
```

Edit `.env` and add your Google AI API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
MODEL_NAME=gemini-2.5-flash  # Optional, defaults to gemini-2.5-flash
```

### 3. Run Demo

```bash
python main.py
```

## 📚 Features Demonstrated

### Multi-Agent Systems
- ✅ 4 specialized agents + coordinator
- ✅ Parallel execution (daily check-ins)
- ✅ Sequential execution (coordinated planning)
- ✅ Single agent routing

### Tools & ADK
- ✅ Custom Python tools (calorie calculation, workout generation)
- ✅ Gemini integration for meal/workout planning
- ✅ MET-based calorie burn calculation
- ✅ Sleep cycle optimization
- ✅ **Google ADK Integration**: Uses `google-adk` for agent orchestration and tool management.

### Memory & Sessions
- ✅ Memory Bank for user profiles
- ✅ Progress tracking over time
- ✅ Preference learning
- ✅ Context-aware recommendations

### Observability & Evaluation
- ✅ Logging system
- ✅ Agent decision tracing
- ✅ Safety checks (calorie floors, sleep minimums)

## 🎬 Demo Scenarios

### Scenario 1: New User Onboarding
Creates user profile and generates personalized health plan.

### Scenario 2: Daily Check-In
Multi-agent parallel analysis of sleep, nutrition, energy, and workout readiness.

### Scenario 3: Interactive Chat
Natural conversation with the health coach. Ask questions like:
- "I want to lose weight"
- "Create a workout plan for me"
- "How can I sleep better?"

## 🛠️ Project Structure

```
health-wellness-coach/
├── config/
│   ├── settings.py          # Configuration management
│   └── prompts.py           # Agent system prompts
├── src/
│   ├── agents/
│   │   ├── base_agent.py    # Base agent factory & ADK setup
│   │   ├── coordinator.py   # Main orchestrator
│   │   ├── nutrition_agent.py
│   │   ├── fitness_agent.py
│   │   ├── sleep_agent.py
│   │   └── mental_wellness_agent.py
│   ├── tools/
│   │   ├── nutrition_tools.py  # Calorie calc, meal planning
│   │   ├── fitness_tools.py    # Workout generation
│   │   └── sleep_tools.py      # Sleep analysis
│   └── memory/
│       └── memory_bank.py      # User profile storage
├── main.py                  # Demo application
├── requirements.txt
└── README.md
```

## 🔧 Key Components

### Tools

**Nutrition Tools:**
- `calculate_daily_calories()` - TDEE using Mifflin-St Jeor equation
- `calculate_macro_targets()` - Protein/carbs/fats distribution
- `analyze_meal_macros()` - Meal nutrition analysis
- `generate_meal_plan()` - AI-powered 7-day meal plans

**Fitness Tools:**
- `assess_fitness_level()` - Fitness evaluation
- `generate_workout_plan()` - Periodized training programs
- `calculate_calories_burned()` - MET-based calorie estimation

**Sleep Tools:**
- `assess_sleep_quality()` - Multi-factor sleep scoring
- `recommend_sleep_schedule()` - Sleep cycle optimization
- `analyze_sleep_patterns()` - Long-term trend analysis

### Agents

Each agent is built using the Google ADK `Agent` class and configured with:
- Specialized system prompt
- Domain-specific tools
- **Gemini 2.5 Flash** model
- Context-aware processing

## 📖 Usage Examples

### Running the Health Coach

The main entry point is `main.py`, which initializes the `HealthCoordinator` and starts an interactive session.

```python
# From main.py
from src.agents.coordinator import health_coordinator
from src.core.runner_manager import RunnerManager

# The coordinator manages sub-agents (Nutrition, Fitness, Sleep, Mental Wellness)
runner = RunnerManager(health_coordinator)
runner.run_interactive()
```

### Using Tools Directly

You can also import and use the tools directly in your own scripts:

```python
from src.tools.nutrition_tools import calculate_daily_calories

# Calculate TDEE
calories = calculate_daily_calories(
    age=32,
    weight_kg=82,
    height_cm=178,
    gender="male",
    activity_level="moderate",
    goal="lose_weight"
)

print(f"Daily Target: {calories['target_calories']} calories")
```

## 🎓 Course Concepts Mapping

| Concept | Implementation |
|---------|----------------|
| Multi-Agent Systems | 4 specialized agents + coordinator |
| Parallel Execution | Daily check-ins analyzed by all agents simultaneously |
| Sequential Execution | Nutrition → Fitness coordination for meal timing |
| Custom Tools | 11 Python functions for health calculations |
| Gemini Integration | Meal planning, workout generation, motivation |
| Memory Bank | User profiles, preferences, progress history |
| Context Engineering | Dynamic context assembly from user history |
| Observability | Logging, routing decisions, safety checks |

## 🔐 Safety Features

- Minimum calorie thresholds (1200 cal women, 1500 cal men)
- Sleep duration warnings (<7 hours)
- Overtraining detection
- Stress level assessment
- Professional help recommendations when needed

## 🚧 Future Enhancements

- [ ] Biometric integration (wearables)
- [ ] Computer vision for food logging
- [ ] Social/community features
- [ ] Advanced ML for preference learning
- [ ] Healthcare provider integration
- [ ] Multi-language support

## 📝 License

This project is created for educational purposes.

## 🙏 Acknowledgments

Built using:
- **Google ADK (Agent Development Kit)**
- **Google Gemini 2.5 Flash**
- Python 3.10+

---

**Note**: This is a health coaching assistant, not a replacement for professional medical advice. Always consult healthcare providers for medical concerns.
