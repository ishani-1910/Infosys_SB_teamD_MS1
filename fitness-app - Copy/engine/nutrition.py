import os
import json

# Load logic from JSON
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(BASE_DIR, "config/diet_rules.json")) as f:
    DIET_RULES = json.load(f)

def calculate_bmr(weight_kg, height_cm, age, gender):
    """
    Calculates BMR using the Mifflin-St Jeor equation.
    """
    # Base formula: 10*weight + 6.25*height - 5*age
    base_bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
    
    if gender.lower() == "male":
        return base_bmr + 5
    elif gender.lower() == "female":
        return base_bmr - 161
    else:
        # Average for non-binary/other
        return base_bmr - 78

def calculate_nutritional_needs(profile, goal, activity_level):
    """
    Returns a dictionary with daily calorie target and macro grams.
    """
    gender = profile.get("gender", "male") # Default fallback
    weight = profile.get("weight_kg")
    height = profile.get("height_cm")
    age = profile.get("age")
    
    # 1. Calculate BMR
    bmr = calculate_bmr(weight, height, age, gender)
    
    # 2. Calculate TDEE (Total Daily Energy Expenditure)
    multiplier = DIET_RULES["activity_multipliers"].get(activity_level, 1.2)
    tdee = bmr * multiplier
    
    # 3. Adjust for Goal (Surplus/Deficit)
    goal_rules = DIET_RULES["goal_modifiers"].get(goal, DIET_RULES["goal_modifiers"]["general_fitness"])
    daily_calories = int(tdee + goal_rules["calorie_surplus"])
    
    # Safety Floor (Don't starve the user)
    if gender.lower() == "male" and daily_calories < 1500:
        daily_calories = 1500
    elif gender.lower() == "female" and daily_calories < 1200:
        daily_calories = 1200
        
    # 4. Calculate Macros (Grams)
    # Protein = 4 cal/g, Carbs = 4 cal/g, Fats = 9 cal/g
    split = goal_rules["macro_split"]
    
    protein_grams = int((daily_calories * split["protein"]) / 4)
    fat_grams = int((daily_calories * split["fats"]) / 9)
    carb_grams = int((daily_calories * split["carbs"]) / 4)
    
    return {
        "calories": daily_calories,
        "macros": {
            "protein": protein_grams,
            "fats": fat_grams,
            "carbs": carb_grams
        }
    }