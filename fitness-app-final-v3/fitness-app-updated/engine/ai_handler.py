"""
AI API Handler for RoutineX
Supports separate API keys and Native JSON Mode for stability.
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# We prefer 1.5-flash or 2.0-flash for large JSON tasks as they are very stable
MODELS_TO_TRY = [
    'gemini-2.0-flash',
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    'gemini-flash-latest'
]

def generate_with_ai(prompt, max_tokens=8192, key_type='workout', json_mode=False):
    """
    Generate content using available AI APIs.
    
    Args:
        prompt: The prompt to send to the AI
        max_tokens: Maximum tokens in response
        key_type: Either 'workout' or 'diet'
        json_mode: If True, forces the model to output valid JSON (Gemini only)
    """
    
    # 1. SELECT API KEY
    if key_type == 'diet':
        gemini_key = os.getenv("GEMINI_API_KEY_DIET") or os.getenv("GEMINI_API_KEY")
    else:
        gemini_key = os.getenv("GEMINI_API_KEY_WORKOUT") or os.getenv("GEMINI_API_KEY")
    
    gemini_error = None
    
    # 2. TRY GEMINI
    if gemini_key:
        success, response, error = _generate_with_gemini(prompt, gemini_key, max_tokens, json_mode)
        if success:
            return True, response, None
        gemini_error = error
    else:
        gemini_error = f"No GEMINI_API_KEY_{key_type.upper()} found in .env"
    
    # 3. FALLBACK TO OPENAI (If configured)
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        success, response, error = _generate_with_openai(prompt, openai_key, max_tokens, json_mode)
        if success:
            return True, response, None
        return False, None, {"gemini_error": gemini_error, "openai_error": error}
    
    return False, None, {"error": "No working API key found", "details": gemini_error}


def _generate_with_gemini(prompt, api_key, max_tokens, json_mode):
    """Try to generate with Gemini API using JSON mode if requested"""
    try:
        genai.configure(api_key=api_key)
        
        generation_config = {
            'temperature': 0.7,
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': max_tokens,
        }

        # ENABLE NATIVE JSON MODE
        if json_mode:
            generation_config['response_mime_type'] = 'application/json'
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        last_error = None
        
        for model_name in MODELS_TO_TRY:
            try:
                model = genai.GenerativeModel(model_name, generation_config=generation_config)
                response = model.generate_content(prompt, safety_settings=safety_settings)
                
                if response and response.text:
                    return True, response.text, None
                    
            except Exception as e:
                last_error = str(e)
                continue
                
        return False, None, f"All models failed. Last error: {last_error}"

    except Exception as e:
        return False, None, f"Gemini setup error: {str(e)}"


def _generate_with_openai(prompt, api_key, max_tokens, json_mode):
    """Try to generate with OpenAI API"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Force JSON object response for OpenAI if requested
        kwargs = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. " + ("Output JSON only." if json_mode else "")},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": max_tokens,
        }
        
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(**kwargs)
        
        if response.choices and response.choices[0].message.content:
            return True, response.choices[0].message.content, None
        else:
            return False, None, "OpenAI returned empty response"
            
    except Exception as e:
        return False, None, f"OpenAI error: {str(e)}"