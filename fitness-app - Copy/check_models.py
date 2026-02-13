import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load your API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # Try the other common name if the first one fails
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("ERROR: API Key not found in .env file.")
else:
    print(f"OK: API Key found: {api_key[:5]}...*****")
    
    # 2. Configure Gemini
    genai.configure(api_key=api_key)

    print("\nSCANNING for available models...")
    try:
        found_any = False
        # 3. List all models and filter for those that can generate text
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"  - {m.name}")
                found_any = True
        
        if not found_any:
            print("WARNING: No models found that support 'generateContent'. Check your API key permissions.")
            
    except Exception as e:
        print(f"ERROR listing models: {e}")