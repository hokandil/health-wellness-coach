import os
# Fix for SSL PermissionError
os.environ['SSLKEYLOGFILE'] = ''

import google.adk.models
print(f"google.adk.models contents: {dir(google.adk.models)}")

try:
    from google.adk.models.google_llm import GoogleLLM
    print("Found GoogleLLM in google.adk.models.google_llm")
except ImportError:
    print("GoogleLLM not found in google.adk.models.google_llm")
    
try:
    from google.adk.models import Gemini
    print("Found Gemini in google.adk.models")
except ImportError:
    print("Gemini not found in google.adk.models")
