import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from .ai_handler import generate_with_ai

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(DOTENV_PATH)


def extract_json_from_text(text):
    """Extract JSON from AI response."""
    text = text.strip()
    
    # If JSON mode is on, the AI might return raw JSON without markdown.
    # But sometimes it still adds markdown. Handle both.
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        parts = text.split("```")
        if len(parts) >= 3:
            text = parts[1]
    
    # Ensure we have the start and end of the object
    start = text.find("{")
    end = text.rfind("}")
    
    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]
    
    return text.strip()


def generate_weekly_diet_plan(targets: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates a personalized WEEKLY (7-day) diet plan.
    """

    cals = targets['calories']
    prot = targets['macros']['protein']
    carb = targets['macros']['carbs']
    fats = targets['macros']['fats']
    meals = profile.get('meals_per_day', 4)

    # Simplified prompt because JSON mode handles the structure enforcement
    prompt = f"""You are a nutritionist. Create a 7-day meal plan.

REQUIREMENTS:
- Calories: {cals} kcal/day
- Protein: {prot}g | Carbs: {carb}g | Fats: {fats}g  
- Diet: {profile.get('diet_type', 'General')}
- Allergies: {', '.join(profile.get('allergies', [])) or 'None'}
- Meals: {meals} per day

Return a valid JSON object with this exact structure:
{{
  "summary": {{
    "total_calories_per_day": {cals},
    "protein_per_day": {prot},
    "carbs_per_day": {carb},
    "fats_per_day": {fats},
    "note": "Summary text"
  }},
  "days": [
    {{
      "day": "Monday",
      "total_calories": {cals},
      "meals": [
        {{
          "meal_name": "Breakfast",
          "food_items": [
            {{
              "item": "Food name",
              "quantity": "Amount",
              "calories": 100,
              "protein": 10,
              "carbs": 10,
              "fats": 5,
              "prep_note": "Prep info"
            }}
          ]
        }}
      ]
    }}
  ]
}}
IMPORTANT: Generate valid JSON for all 7 days (Monday through Sunday). Do not truncate."""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            # ENABLE JSON MODE HERE
            success, response_text, error = generate_with_ai(
                prompt, 
                max_tokens=8192, 
                key_type='diet', 
                json_mode=True
            )
            
            if not success:
                if attempt < max_retries - 1: continue
                return {"error": "Could not generate diet plan.", "details": str(error)}
            
            # Extract and Parse
            raw_text = extract_json_from_text(response_text)
            diet_plan = json.loads(raw_text)
            
            if "days" not in diet_plan:
                raise ValueError("Missing 'days' field")
            
            return diet_plan
            
        except (json.JSONDecodeError, ValueError) as e:
            print(f"JSON Error (Attempt {attempt+1}): {e}")
            if attempt < max_retries - 1: continue
            return {
                "error": "Failed to parse diet plan.",
                "details": "The AI response was incomplete or invalid JSON."
            }
        except Exception as e:
            return {"error": "Unexpected error.", "details": str(e)}

    return {"error": "Failed after retries."}