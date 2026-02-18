import os
import google.generativeai as genai
from dotenv import load_dotenv

# Path to the .env file in the root
load_dotenv(dotenv_path="../.env")

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
    print("ERROR: GOOGLE_API_KEY not set.")
else:
    genai.configure(api_key=api_key)
    print("Listing available models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"LLM: {m.name}")
            if 'embedContent' in m.supported_generation_methods:
                print(f"Embedding: {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")
