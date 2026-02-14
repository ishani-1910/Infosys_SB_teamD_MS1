"""
API Key Test Script for RoutineX
Tests if your Gemini API key is working correctly
"""

import os
from dotenv import load_dotenv

print("=" * 70)
print("🔑 RoutineX API Key Test")
print("=" * 70)
print()

# Step 1: Load environment variables
print("📁 Step 1: Loading .env file...")
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ FAILED: No GEMINI_API_KEY found in .env file")
    print("\n🔧 FIX:")
    print("   1. Create a file named '.env' in the fitness-app folder")
    print("   2. Add this line: GEMINI_API_KEY=your-key-here")
    print("   3. Get your key from: https://makersuite.google.com/app/apikey")
    input("\nPress Enter to exit...")
    exit(1)

print(f"✅ API Key loaded: {api_key[:15]}...{api_key[-4:]}")
print()

# Step 2: Check key format
print("🔍 Step 2: Validating key format...")
if not api_key.startswith("AIzaSy"):
    print("⚠️  WARNING: API key doesn't start with 'AIzaSy'")
    print("   This might not be a valid Gemini API key")
    print("   Make sure you're using a key from Google AI Studio")
    print("   NOT a Google Cloud API key")
    print()
else:
    print("✅ Key format looks correct")
    print()

# Step 3: Test API connection
print("🌐 Step 3: Testing API connection...")
print("   (This may take a few seconds)")
print()

try:
    import google.generativeai as genai
    
    genai.configure(api_key=api_key)
    
    # Try each model
    models_to_test = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro'
    ]
    
    working_models = []
    failed_models = []
    
    for model_name in models_to_test:
        try:
            print(f"   Testing {model_name}...", end=" ")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello'")
            if response and response.text:
                print("✅ WORKING")
                working_models.append(model_name)
            else:
                print("❌ NO RESPONSE")
                failed_models.append((model_name, "No response"))
        except Exception as e:
            error_msg = str(e)
            print(f"❌ FAILED: {error_msg[:50]}")
            failed_models.append((model_name, error_msg))
    
    print()
    print("=" * 70)
    print("📊 TEST RESULTS")
    print("=" * 70)
    print()
    
    if working_models:
        print(f"✅ {len(working_models)} model(s) working:")
        for m in working_models:
            print(f"   ✓ {m}")
        print()
        print("🎉 SUCCESS! Your API key is working correctly!")
        print("   You can now use the RoutineX app.")
    else:
        print("❌ No models are working!")
        print()
        
    if failed_models:
        print(f"\n❌ {len(failed_models)} model(s) failed:")
        for m, err in failed_models:
            print(f"   ✗ {m}")
            print(f"     Error: {err[:60]}")
        print()
        
        # Provide specific guidance based on errors
        all_errors = " ".join([e for _, e in failed_models]).lower()
        
        if "403" in all_errors or "api key not valid" in all_errors:
            print("🔧 FIX: Your API key is invalid")
            print("   1. Go to: https://makersuite.google.com/app/apikey")
            print("   2. Create a new API key")
            print("   3. Replace the key in your .env file")
            
        elif "429" in all_errors or "quota" in all_errors:
            print("🔧 FIX: You've exceeded your quota")
            print("   1. Wait 60 seconds and try again")
            print("   2. Check your quota at: https://console.cloud.google.com/")
            
        elif "not exist" in all_errors or "not found" in all_errors:
            print("🔧 FIX: Models not accessible")
            print("   1. Make sure you're using a Gemini API key")
            print("   2. NOT a Google Cloud or other Google API key")
            print("   3. Get correct key from: https://makersuite.google.com/app/apikey")
            
        else:
            print("🔧 GENERAL FIXES:")
            print("   1. Check your internet connection")
            print("   2. Try disabling VPN")
            print("   3. Wait 60 seconds and try again")
            print("   4. Get a fresh API key from: https://makersuite.google.com/app/apikey")
    
except ImportError:
    print("❌ FAILED: google-generativeai package not installed")
    print("\n🔧 FIX:")
    print("   Run: pip install google-generativeai")
    
except Exception as e:
    print(f"❌ FAILED: Unexpected error: {e}")
    print("\n🔧 FIX:")
    print("   1. Check your internet connection")
    print("   2. Verify your API key is correct")
    print("   3. Try running: pip install --upgrade google-generativeai")

print()
print("=" * 70)
input("\nPress Enter to exit...")
