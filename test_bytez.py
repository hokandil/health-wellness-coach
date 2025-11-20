from bytez import Bytez
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("BYTEZ_API_KEY")
print(f"Key: {key}")

try:
    sdk = Bytez(key)
    model = sdk.model("google/gemini-2.5-flash")
    
    print("Sending request...")
    result = model.run([
      {
        "role": "user",
        "content": "Hello"
      }
    ])
    
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")
    
    if isinstance(result, (list, tuple)):
        print(f"Length: {len(result)}")

except Exception as e:
    print(f"Error: {e}")
