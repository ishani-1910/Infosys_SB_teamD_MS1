from engine.exercises import EXERCISES

# ------------------------------
# Weekly templates by goal & experience
# ------------------------------

WEEKLY_TEMPLATES = {
    "muscle_gain": {
        "beginner": ["strength", "rest", "strength", "cardio", "rest", "strength"],
        "intermediate": ["strength", "cardio", "strength", "mobility", "strength", "rest"],
        "advanced": ["strength", "strength", "cardio", "strength", "mobility", "strength"]
    },
    "fat_loss": {
        "beginner": ["strength", "rest", "cardio", "mobility", "rest", "cardio"],
        "intermediate": ["strength", "cardio", "HIIT", "mobility", "strength", "cardio"],
        "advanced": ["strength", "HIIT", "cardio", "strength", "HIIT", "mobility"]
    },
    "general_fitness": {
        "beginner": ["strength", "cardio", "mobility", "rest", "strength", "cardio"],
        "intermediate": ["strength", "cardio", "strength", "mobility", "cardio", "rest"],
        "advanced": ["strength", "HIIT", "strength", "cardio", "mobility", "strength"]
    },
    "endurance": {
        "beginner": ["cardio", "rest", "cardio", "mobility", "rest", "cardio"],
        "intermediate": ["cardio", "strength", "cardio", "mobility", "cardio", "rest"],
        "advanced": ["cardio", "HIIT", "strength", "cardio", "mobility", "HIIT"]
    },
    "mobility_flexibility": {
        "beginner": ["mobility", "rest", "mobility", "strength", "rest", "mobility"],
        "intermediate": ["mobility", "strength", "mobility", "cardio", "strength", "mobility"],
        "advanced": ["mobility", "strength", "mobility", "strength", "cardio", "mobility"]
    }
}

# ------------------------------
# Default exercise rules per level
# ------------------------------

EXERCISE_RULES = {
    "beginner": {"sets": 3, "reps": "12-15", "rest": "60-90 sec"},
    "intermediate": {"sets": 4, "reps": "8-12", "rest": "90-120 sec"},
    "advanced": {"sets": 5, "reps": "6-10", "rest": "90-120 sec"}
}

# ------------------------------
# Core logic: filter exercises based on level and medical condition
# ------------------------------

def filter_exercises(workout_type, experience, medical_conditions):
    selected = []
    if workout_type not in EXERCISES:
        return selected

    # strength subcategories
    if workout_type == "strength":
        for group in EXERCISES["strength"]:
            for ex in EXERCISES["strength"][group]:
                if ex["level"] in [experience, "beginner"]:
                    if not any(cond in medical_conditions for cond in ex.get("avoid_if", [])):
                        selected.append(ex)

    # cardio
    elif workout_type == "cardio":
        for category in EXERCISES["cardio"]:
            for ex in EXERCISES["cardio"][category]:
                if experience == "beginner" and ex.get("impact") == "low":
                    if not any(cond in medical_conditions for cond in ex.get("avoid_if", [])):
                        selected.append(ex)
                elif experience in ["intermediate", "advanced"]:
                    if not any(cond in medical_conditions for cond in ex.get("avoid_if", [])):
                        selected.append(ex)

    # mobility
    elif workout_type == "mobility":
        for ex in EXERCISES["mobility"]:
            selected.append(ex)

    # hiit
    elif workout_type == "hiit":
        for ex in EXERCISES["hiit"]:
            if experience in ["intermediate", "advanced"]:
                if not any(cond in medical_conditions for cond in ex.get("avoid_if", [])):
                    selected.append(ex)

    return selected

# ------------------------------
# Main function to generate weekly plan
# ------------------------------

def generate_weekly_plan(goal, experience, medical_conditions, available_days=6):
    """
    Returns weekly schedule with exercises.
    """
    goal_key = goal.lower()
    exp_key = experience.lower()

    template = WEEKLY_TEMPLATES.get(goal_key, {}).get(exp_key, [])

    # Respect available days
    schedule_days = template[:available_days]

    weekly_plan = []

    for day_type in schedule_days:
        exercises = filter_exercises(day_type.lower(), exp_key, medical_conditions)
        daily_plan = {
            "day_type": day_type,
            "exercises": exercises,
            "rules": EXERCISE_RULES[exp_key]
        }
        weekly_plan.append(daily_plan)

    return weekly_plan

# ------------------------------
# Example usage
# ------------------------------
if __name__ == "__main__":
    goal = "muscle_gain"
    experience = "beginner"
    medical_conditions = []

    plan = generate_weekly_plan(goal, experience, medical_conditions, available_days=6)
    for i, day in enumerate(plan, 1):
        print(f"Day {i}: {day['day_type']}")
        for ex in day["exercises"]:
            print(f"  - {ex['name']} | Sets: {ex.get('sets', '-')}, Reps/Time: {ex.get('reps', ex.get('time', '-'))}")
        print()
