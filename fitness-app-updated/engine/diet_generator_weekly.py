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
    
    # Remove markdown
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        parts = text.split("```")
        if len(parts) >= 3:
            text = parts[1]
    
    # Find JSON object
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

    prompt = f"""Create a 7-day diet plan.

TARGETS: {cals} kcal/day, P:{prot}g, C:{carb}g, F:{fats}g
USER: Diet={profile.get('diet_type', 'General')}, Allergies={', '.join(profile.get('allergies', [])) or 'None'}
MEALS: {meals} meals/day

Return ONLY valid JSON:

{{
  "summary": {{"total_calories_per_day": {cals}, "protein_per_day": {prot}, "carbs_per_day": {carb}, "fats_per_day": {fats}, "note": "Balanced plan"}},
  "days": [
    {{"day": "Monday", "total_calories": {cals}, "meals": [{{"meal_name": "Breakfast", "food_items": [{{"item": "Oatmeal", "quantity": "1 bowl", "calories": 300, "protein": 10, "carbs": 50, "fats": 5, "prep_note": "Cook with milk"}}]}}, {{"meal_name": "Lunch", "food_items": [{{"item": "Chicken Salad", "quantity": "1 plate", "calories": 400, "protein": 40, "carbs": 20, "fats": 15, "prep_note": "Grilled"}}]}}, {{"meal_name": "Snack", "food_items": [{{"item": "Protein Shake", "quantity": "1 scoop", "calories": 150, "protein": 25, "carbs": 5, "fats": 3, "prep_note": "Mix with water"}}]}}, {{"meal_name": "Dinner", "food_items": [{{"item": "Salmon", "quantity": "200g", "calories": 350, "protein": 40, "carbs": 10, "fats": 18, "prep_note": "Baked"}}]}}]}},
    {{"day": "Tuesday", "total_calories": {cals}, "meals": [{{"meal_name": "Breakfast", "food_items": [{{"item": "Eggs", "quantity": "3 eggs", "calories": 300, "protein": 18, "carbs": 2, "fats": 20, "prep_note": "Scrambled"}}]}}, {{"meal_name": "Lunch", "food_items": [{{"item": "Turkey Wrap", "quantity": "1 wrap", "calories": 400, "protein": 35, "carbs": 30, "fats": 12, "prep_note": "Whole wheat"}}]}}, {{"meal_name": "Snack", "food_items": [{{"item": "Greek Yogurt", "quantity": "1 cup", "calories": 150, "protein": 15, "carbs": 10, "fats": 5, "prep_note": "Plain"}}]}}, {{"meal_name": "Dinner", "food_items": [{{"item": "Beef Stir-fry", "quantity": "1 plate", "calories": 450, "protein": 40, "carbs": 25, "fats": 18, "prep_note": "With veggies"}}]}}]}},
    {{"day": "Wednesday", "total_calories": {cals}, "meals": [{{"meal_name": "Breakfast", "food_items": [{{"item": "Pancakes", "quantity": "3 pancakes", "calories": 350, "protein": 12, "carbs": 60, "fats": 8, "prep_note": "Protein pancakes"}}]}}, {{"meal_name": "Lunch", "food_items": [{{"item": "Fish Tacos", "quantity": "2 tacos", "calories": 400, "protein": 35, "carbs": 30, "fats": 15, "prep_note": "Grilled fish"}}]}}, {{"meal_name": "Snack", "food_items": [{{"item": "Almonds", "quantity": "30g", "calories": 170, "protein": 6, "carbs": 6, "fats": 15, "prep_note": "Raw"}}]}}, {{"meal_name": "Dinner", "food_items": [{{"item": "Chicken Curry", "quantity": "1 bowl", "calories": 400, "protein": 38, "carbs": 25, "fats": 15, "prep_note": "Mild spice"}}]}}]}},
    {{"day": "Thursday", "total_calories": {cals}, "meals": [{{"meal_name": "Breakfast", "food_items": [{{"item": "Smoothie Bowl", "quantity": "1 bowl", "calories": 320, "protein": 15, "carbs": 45, "fats": 10, "prep_note": "With berries"}}]}}, {{"meal_name": "Lunch", "food_items": [{{"item": "Quinoa Bowl", "quantity": "1 bowl", "calories": 420, "protein": 20, "carbs": 50, "fats": 15, "prep_note": "With chickpeas"}}]}}, {{"meal_name": "Snack", "food_items": [{{"item": "Apple with PB", "quantity": "1 apple", "calories": 180, "protein": 5, "carbs": 25, "fats": 8, "prep_note": "Natural PB"}}]}}, {{"meal_name": "Dinner", "food_items": [{{"item": "Pork Chops", "quantity": "200g", "calories": 380, "protein": 42, "carbs": 5, "fats": 22, "prep_note": "Pan-seared"}}]}}]}},
    {{"day": "Friday", "total_calories": {cals}, "meals": [{{"meal_name": "Breakfast", "food_items": [{{"item": "Avocado Toast", "quantity": "2 slices", "calories": 340, "protein": 12, "carbs": 35, "fats": 18, "prep_note": "Whole grain"}}]}}, {{"meal_name": "Lunch", "food_items": [{{"item": "Shrimp Pasta", "quantity": "1 plate", "calories": 450, "protein": 30, "carbs": 50, "fats": 15, "prep_note": "Light sauce"}}]}}, {{"meal_name": "Snack", "food_items": [{{"item": "Protein Bar", "quantity": "1 bar", "calories": 200, "protein": 20, "carbs": 20, "fats": 7, "prep_note": "Ready to eat"}}]}}, {{"meal_name": "Dinner", "food_items": [{{"item": "Lamb Kebab", "quantity": "150g", "calories": 350, "protein": 35, "carbs": 10, "fats": 20, "prep_note": "Grilled"}}]}}]}},
    {{"day": "Saturday", "total_calories": {cals}, "meals": [{{"meal_name": "Breakfast", "food_items": [{{"item": "Waffles", "quantity": "2 waffles", "calories": 360, "protein": 10, "carbs": 55, "fats": 12, "prep_note": "Whole wheat"}}]}}, {{"meal_name": "Lunch", "food_items": [{{"item": "Burger Bowl", "quantity": "1 bowl", "calories": 440, "protein": 38, "carbs": 30, "fats": 20, "prep_note": "Lean beef"}}]}}, {{"meal_name": "Snack", "food_items": [{{"item": "Cottage Cheese", "quantity": "1 cup", "calories": 160, "protein": 28, "carbs": 6, "fats": 2, "prep_note": "Low fat"}}]}}, {{"meal_name": "Dinner", "food_items": [{{"item": "Pizza", "quantity": "2 slices", "calories": 380, "protein": 20, "carbs": 45, "fats": 15, "prep_note": "Thin crust"}}]}}]}},
    {{"day": "Sunday", "total_calories": {cals}, "meals": [{{"meal_name": "Breakfast", "food_items": [{{"item": "French Toast", "quantity": "2 slices", "calories": 340, "protein": 14, "carbs": 50, "fats": 10, "prep_note": "Cinnamon"}}]}}, {{"meal_name": "Lunch", "food_items": [{{"item": "Roast Chicken", "quantity": "200g", "calories": 420, "protein": 45, "carbs": 15, "fats": 18, "prep_note": "With veggies"}}]}}, {{"meal_name": "Snack", "food_items": [{{"item": "Trail Mix", "quantity": "40g", "calories": 190, "protein": 6, "carbs": 20, "fats": 10, "prep_note": "Unsalted"}}]}}, {{"meal_name": "Dinner", "food_items": [{{"item": "Veggie Stir-fry", "quantity": "1 plate", "calories": 350, "protein": 15, "carbs": 40, "fats": 15, "prep_note": "Tofu"}}]}}]}}
  ]
}}"""

    # Retry up to 3 times
    max_retries = 3
    for attempt in range(max_retries):
        try:
            success, response_text, error = generate_with_ai(prompt, max_tokens=8192)
            
            if not success:
                if attempt < max_retries - 1:
                    continue
                return {
                    "error": "Could not generate diet plan.",
                    "details": str(error)
                }
            
            # Extract JSON
            raw_text = extract_json_from_text(response_text)
            diet_plan = json.loads(raw_text)
            
            # Validate
            if "days" not in diet_plan:
                raise ValueError("Missing 'days' field")
            
            return diet_plan
            
        except (json.JSONDecodeError, ValueError) as e:
            if attempt < max_retries - 1:
                continue
            print(f"ERROR Diet Plan: {str(e)}")
            print(f"Response: {response_text[:300]}")
            return {
                "error": "Failed to parse diet plan.",
                "details": f"Parse error: {str(e)}"
            }
        except Exception as e:
            if attempt < max_retries - 1:
                continue
            return {
                "error": "Unexpected error.",
                "details": str(e)
            }