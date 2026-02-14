import os
import json
import google.generativeai as genai
from typing import Dict, Any
from dotenv import load_dotenv

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

# Load environment variables
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(DOTENV_PATH)

# ---------------------------------------------------------
# MAIN GENERATOR FUNCTION
# ---------------------------------------------------------

def generate_diet_plan(targets: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates a personalized diet plan using the Gemini API.
    """
    
    # 1. Fetch API Key inside the function
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "error": "API Key is missing.",
            "details": "GEMINI_API_KEY not found in environment variables. Please check your .env file."
        }

    try:
        genai.configure(api_key=api_key)
        
        # 2. Construct the Prompt
        prompt = f"""
        You are an expert nutritionist and chef. Create a highly detailed daily diet plan based on the following specific constraints.

        USER PROFILE:
        - Diet Type: {profile.get('diet_type', 'General')}
        - Cuisine Preference: {profile.get('cuisine', 'General')}
        - Regional Style: {profile.get('region', 'General')}
        - Allergies/Exclusions: {', '.join(profile.get('allergies', [])) if profile.get('allergies') else "None"}
        - Meals Per Day: {profile.get('meals_per_day', 4)}

        NUTRITIONAL TARGETS (Strictly adhere to these):
        - Total Calories: {targets['calories']} kcal
        - Protein: {targets['macros']['protein']}g
        - Carbs: {targets['macros']['carbs']}g
        - Fats: {targets['macros']['fats']}g

        INSTRUCTIONS:
        1. Generate specific, culturally accurate meal names.
        2. Provide a short recipe/prep note for each main item.
        3. Ensure the total macros sum up close to the targets (+/- 10%).
        4. RETURN ONLY VALID JSON. Do not include markdown formatting like ```json ... ```.

        REQUIRED JSON FORMAT:
        {{
          "summary": {{
            "total_calories": 0,
            "protein": 0,
            "carbs": 0,
            "fats": 0,
            "note": "Short summary of the plan"
          }},
          "meals": [
            {{
              "meal_name": "Breakfast",
              "food_items": [
                {{
                  "item": "Name of food",
                  "quantity": "e.g., 2 slices / 1 bowl",
                  "calories": 0,
                  "protein": 0,
                  "carbs": 0,
                  "fats": 0,
                  "prep_note": "Brief instruction"
                }}
              ]
            }}
          ]
        }}
        """

        # 3. Try Generating Content (Using models from your available list)
        # Updated list based on your error log
        models_to_try = [
            'gemini-2.0-flash', 
            'gemini-2.5-flash', 
            'gemini-flash-latest',
            'gemini-1.5-flash' # Keeping as fallback just in case
        ]
        
        response = None
        last_error = None

        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                break # If successful, stop trying
            except Exception as e:
                last_error = e
                continue

        if not response:
            return {
                "error": "Could not generate plan with any available model.",
                "details": f"Last attempted model error: {str(last_error)}"
            }

        # 4. Clean and Parse JSON
        raw_text = response.text
        clean_json = raw_text.strip()
        
        # Remove markdown code blocks if present
        if clean_json.startswith("```json"):
            clean_json = clean_json.replace("```json", "", 1)
        if clean_json.startswith("```"):
            clean_json = clean_json.replace("```", "", 1)
        if clean_json.endswith("```"):
            clean_json = clean_json.replace("```", "", 1)
        
        diet_plan = json.loads(clean_json.strip())
        return diet_plan

    except json.JSONDecodeError:
        return {
            "error": "Failed to parse diet plan.",
            "details": "The AI returned invalid JSON. Please try again."
        }
    except Exception as e:
        return {
            "error": "An unexpected error occurred.",
            "details": str(e)
        }

# ---------------------------------------------------------
# TESTING BLOCK
# ---------------------------------------------------------
if __name__ == "__main__":
    test_targets = {
        "calories": 2200,
        "macros": {"protein": 150, "fats": 70, "carbs": 240}
    }
    
    test_profile = {
        "diet_type": "Vegetarian",
        "cuisine": "Indian",
        "region": "North Indian",
        "allergies": ["None"],
        "meals_per_day": 4
    }

    print("Generating test plan...")
    plan = generate_diet_plan(test_targets, test_profile)
    print(json.dumps(plan, indent=2))
        