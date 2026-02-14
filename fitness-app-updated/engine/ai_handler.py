"""
AI API Handler for RoutineX
Supports both Google Gemini and OpenAI APIs with automatic fallback
"""

import os
import json
from dotenv import load_dotenv

load_dotenv()

def generate_with_ai(prompt, max_tokens=8192):
    """
    Generate content using available AI APIs.
    Tries Gemini first, then OpenAI if available.
    
    Returns:
        tuple: (success: bool, response_text: str or None, error_dict: dict or None)
    """
    
    # Try Gemini first
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        success, response, error = _generate_with_gemini(prompt, gemini_key, max_tokens)
        if success:
            return True, response, None
        # Store gemini error but continue to try OpenAI
        gemini_error = error
    else:
        gemini_error = "No GEMINI_API_KEY found in .env"
    
    # Try OpenAI as fallback
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        success, response, error = _generate_with_openai(prompt, openai_key, max_tokens)
        if success:
            return True, response, None
        # Both failed
        return False, None, {
            "gemini_error": gemini_error,
            "openai_error": error
        }
    
    # No working API
    return False, None, {
        "error": "No working API key found",
        "details": f"Gemini error: {gemini_error}. No OpenAI key configured. Add GEMINI_API_KEY or OPENAI_API_KEY to your .env file."
    }


def _generate_with_gemini(prompt, api_key, max_tokens):
    """Try to generate with Gemini API"""
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        
        # Use the most stable model
        generation_config = {
            'temperature': 0.7,
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': max_tokens,
        }
        
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config=generation_config
        )
        
        # Safety settings to avoid blocking
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        response = model.generate_content(
            prompt,
            safety_settings=safety_settings
        )
        
        if response and response.text:
            return True, response.text, None
        else:
            return False, None, "Gemini returned empty response"
            
    except Exception as e:
        error_msg = str(e)
        
        if "API key not valid" in error_msg or "API_KEY_INVALID" in error_msg:
            details = "Invalid Gemini API key. Get one from https://makersuite.google.com/app/apikey"
        elif "429" in error_msg or "quota" in error_msg.lower():
            details = "Gemini rate limit exceeded. Wait 60 seconds or try OpenAI."
        elif "PERMISSION_DENIED" in error_msg:
            details = "Permission denied. API key doesn't have access to Gemini."
        else:
            details = f"Gemini error: {error_msg}"
        
        return False, None, details


def _generate_with_openai(prompt, api_key, max_tokens):
    """Try to generate with OpenAI API"""
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Most cost-effective model
            messages=[
                {"role": "system", "content": "You are an expert fitness coach and nutritionist. Always respond with valid JSON when requested."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=max_tokens,
        )
        
        if response.choices and response.choices[0].message.content:
            return True, response.choices[0].message.content, None
        else:
            return False, None, "OpenAI returned empty response"
            
    except Exception as e:
        error_msg = str(e)
        
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            details = "Invalid OpenAI API key. Get one from https://platform.openai.com/api-keys"
        elif "rate_limit" in error_msg.lower() or "429" in error_msg:
            details = "OpenAI rate limit exceeded. Wait a moment and try again."
        elif "quota" in error_msg.lower() or "insufficient" in error_msg.lower():
            details = "OpenAI quota exceeded. Check your usage at https://platform.openai.com/usage"
        else:
            details = f"OpenAI error: {error_msg}"
        
        return False, None, details


def get_available_apis():
    """Check which APIs are configured"""
    apis = []
    
    if os.getenv("GEMINI_API_KEY"):
        apis.append("Gemini")
    
    if os.getenv("OPENAI_API_KEY"):
        apis.append("OpenAI")
    
    return apis


def test_apis():
    """Test which APIs are working"""
    results = {}
    
    # Test Gemini
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        success, _, error = _generate_with_gemini("Say 'Hello'", gemini_key, 100)
        results["Gemini"] = "✅ Working" if success else f"❌ {error}"
    else:
        results["Gemini"] = "⚪ Not configured"
    
    # Test OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        success, _, error = _generate_with_openai("Say 'Hello'", openai_key, 100)
        results["OpenAI"] = "✅ Working" if success else f"❌ {error}"
    else:
        results["OpenAI"] = "⚪ Not configured"
    
    return results


if __name__ == "__main__":
    print("=" * 70)
    print("🤖 AI API Test - RoutineX")
    print("=" * 70)
    print()
    
    results = test_apis()
    
    for api_name, status in results.items():
        print(f"{api_name}: {status}")
    
    print()
    print("=" * 70)
    
    if any("✅" in status for status in results.values()):
        print("✅ At least one API is working! You're good to go.")
    else:
        print("❌ No working APIs found.")
        print("\nTo fix this, add to your .env file:")
        print("  GEMINI_API_KEY=your-key-here")
        print("  OR")
        print("  OPENAI_API_KEY=your-key-here")
        print("\nGet keys from:")
        print("  Gemini: https://makersuite.google.com/app/apikey")
        print("  OpenAI: https://platform.openai.com/api-keys")
