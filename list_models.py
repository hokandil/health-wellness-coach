import os
from dotenv import load_dotenv

# Fix for SSL PermissionError
os.environ['SSLKEYLOGFILE'] = ''

# Load environment variables
load_dotenv()

import asyncio
from google.genai import Client

# Setup environment same as main.py
if not os.getenv('GOOGLE_API_KEY') and os.getenv('BYTEZ_API_KEY'):
    print("Using BYTEZ_API_KEY as GOOGLE_API_KEY")
    os.environ['GOOGLE_API_KEY'] = os.getenv('BYTEZ_API_KEY')

async def list_models():
    print(f"Checking models with API Key: {os.environ.get('GOOGLE_API_KEY', 'Not Set')[:5]}...")
    try:
        client = Client()
        print("Client initialized. Fetching models...")
        # List models
        # client.aio.models.list() is a coroutine that returns an async iterator or list
        # Based on previous errors, it seems to be a coroutine.
        models = await client.aio.models.list()
        for model in models:
            print(f" - {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    asyncio.run(list_models())
