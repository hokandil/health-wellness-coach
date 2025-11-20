# 🏥 Personal Health & Wellness Coach

An AI-powered multi-agent system for comprehensive health and wellness guidance. This project demonstrates advanced AI agent concepts including multi-agent orchestration, tool usage, memory management, and agent-to-agent communication.

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

# Edit .env and add your Google AI API key
# Get your key from: https://makersuite.google.com/app/apikey
```

Edit `.env`:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Run Demo

```bash
python main.py
```

## 📚 Features Demonstrated

### Day 1: Multi-Agent Systems
- ✅ 4 specialized agents + coordinator
- ✅ Parallel execution (daily check-ins)
- ✅ Sequential execution (coordinated planning)
- ✅ Single agent routing

### Day 2: Tools & MCP
- ✅ Custom Python tools (calorie calculation, workout generation)
- ✅ Gemini integration for meal/workout planning
- ✅ MET-based calorie burn calculation
- ✅ Sleep cycle optimization

### Day 3: Memory & Sessions
- ✅ Memory Bank for user profiles
- ✅ Progress tracking over time
- ✅ Preference learning
- ✅ Context-aware recommendations

### Day 4: Observability & Evaluation
- ✅ Logging system
- ✅ Agent decision tracing
- ✅ Safety checks (calorie floors, sleep minimums)

### Day 5: A2A & Production
- ✅ Agent-to-agent coordination
- ✅ Conflict resolution (e.g., nutrition vs fitness goals)
- ✅ Production-ready architecture

## 🎬 Demo Scenarios

### Scenario 1: New User Onboarding
Creates user profile and generates personalized health plan.

### Scenario 2: Daily Check-In
Multi-agent parallel analysis of sleep, nutrition, energy, and workout readiness.

### Scenario 3: Tool Usage
Direct demonstration of nutrition, fitness, and sleep tools.

### Scenario 4: Interactive Chat
Natural conversation with the health coach.

## 🛠️ Project Structure

```
health-wellness-coach/
├── config/
│   ├── settings.py          # Configuration management
│   └── prompts.py            # Agent system prompts
├── src/
│   ├── agents/
│   │   ├── base_agent.py     # Base agent class
│   │   ├── coordinator.py    # Main orchestrator
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
├── main.py                   # Demo application
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

Each agent has:
- Specialized system prompt
- Domain-specific tools
- Gemini 2.0 Flash model
- Context-aware processing

### Memory

- User profile storage (JSON-based)
- Progress tracking
- Preference learning
- Historical data analysis

## 📖 Usage Examples

### Example 1: Calculate Nutrition Targets

```python
from src.tools.nutrition_tools import calculate_daily_calories, calculate_macro_targets

# Calculate TDEE
calories = calculate_daily_calories(
    age=32,
    weight_kg=82,
    height_cm=178,
    gender="male",
    activity_level="moderate",
    goal="lose_weight"
)

# Calculate macros
macros = calculate_macro_targets(
    target_calories=calories['target_calories'],
    weight_kg=82,
    goal="lose_weight"
)

print(f"Daily Target: {calories['target_calories']} calories")
print(f"Protein: {macros['protein']['grams']}g")
print(f"Carbs: {macros['carbs']['grams']}g")
print(f"Fats: {macros['fats']['grams']}g")
```

### Example 2: Multi-Agent Workflow

```python
from src.agents.coordinator import HealthCoordinator
from src.agents.nutrition_agent import NutritionAgent
from src.agents.fitness_agent import FitnessAgent

# Initialize agents
coordinator = HealthCoordinator(sub_agents={
    "nutrition_agent": NutritionAgent(),
    "fitness_agent": FitnessAgent()
})

# Execute workflow
result = coordinator.execute_workflow(
    user_input="I want to lose weight and build muscle",
    context={"user_profile": user_profile}
)

print(result['final_response'])
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
| A2A Protocol | Agents negotiate balanced health plans |
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

This project is created for educational purposes as part of the 5-Day AI Agents Intensive Course.

## 🙏 Acknowledgments

Built using:
- Google Gemini 2.0 Flash
- Python 3.10+
- Concepts from the 5-Day AI Agents Intensive Course

---

**Note**: This is a health coaching assistant, not a replacement for professional medical advice. Always consult healthcare providers for medical concerns.
