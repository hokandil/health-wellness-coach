# Import Error Fix Summary

## Problem
The application was failing with:
```
ImportError: cannot import name 'GoogleLLM' from 'google.adk.models'
```

## Root Causes

### 1. Incorrect Import Name
- **Issue**: Code was importing `GoogleLLM` which doesn't exist in `google.adk.models`
- **Correct Import**: Should be `Gemini` class

### 2. Incorrect API Usage
- **Issue**: Code was calling `llm.generate_content()` which doesn't exist
- **Correct Method**: `llm.generate_content_async()` which returns an async generator

### 3. Wrong Request Format
- **Issue**: Passing string directly to `generate_content_async()`
- **Correct Format**: Must pass `LlmRequest` object with `Content` and `Part` objects

### 4. Invalid Model Name
- **Issue**: Using `gemini-2.0-flash-exp` which returns 404
- **Correct Model**: `gemini-1.5-flash` (stable model)

## Changes Made

### Files Modified:
1. **src/tools/fitness_tools.py**
   - Changed import from `GoogleLLM` to `Gemini, LlmRequest`
   - Added imports for `Content, Part` from `google.genai.types`
   - Made `generate_workout_plan` async
   - Updated to use `LlmRequest` with proper structure
   - Changed model to `gemini-1.5-flash`
   - Iterate over async generator to collect response

2. **src/tools/nutrition_tools.py**
   - Same changes for `analyze_meal_macros` function
   - Same changes for `generate_meal_plan` function

3. **src/utils/observability.py**
   - Updated `trace_tool` decorator to support both sync and async functions
   - Added `inspect.iscoroutinefunction` check

4. **pytest.ini** (new file)
   - Added to fix pytest import issues
   - Sets `pythonpath = .` for proper module resolution

## Correct Usage Pattern

```python
from google.adk.models import Gemini, LlmRequest
from google.genai.types import Content, Part

# Initialize
llm = Gemini(model="gemini-1.5-flash", api_key=api_key)

# Create request
request = LlmRequest(contents=[Content(parts=[Part(text=prompt)])])

# Call async generator
full_response_text = ""
async for chunk in llm.generate_content_async(request):
    if hasattr(chunk, 'text') and chunk.text:
        full_response_text += chunk.text
```

## Testing
Run `python test_fix.py` to verify the fix works correctly.

## Next Steps
Restart `main.py` to pick up the changes, as the running process still has the old code loaded.
