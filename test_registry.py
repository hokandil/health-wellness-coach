import os
# Fix for SSL PermissionError
os.environ['SSLKEYLOGFILE'] = ''

from google.adk.models import LLMRegistry, Gemini

print("Initial registry keys:", LLMRegistry._registry.keys() if hasattr(LLMRegistry, '_registry') else "Cannot access _registry")

print("\nRegistering models/gemini-2.5-flash...")
try:
    # Try decorator syntax: register(name)(class)
    LLMRegistry.register('models/gemini-2.5-flash')(Gemini)
    print("Registration successful.")
except Exception as e:
    print(f"Registration failed: {e}")

print("\nResolving models/gemini-2.5-flash...")
try:
    cls = LLMRegistry.resolve('models/gemini-2.5-flash')
    print(f"Resolved class: {cls}")
    print(f"Is Gemini? {cls == Gemini}")
except Exception as e:
    print(f"Resolution failed: {e}")

print("\nCreating instance...")
try:
    instance = cls(model='models/gemini-2.5-flash')
    print(f"Instance created: {instance}")
except Exception as e:
    print(f"Instantiation failed: {e}")
