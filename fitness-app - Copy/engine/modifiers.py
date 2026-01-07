from engine.exercises import EXERCISES

# ------------------------------
# Safety modifiers for medical conditions & injuries
# ------------------------------

def apply_medical_conditions(exercises, medical_conditions):
    if not medical_conditions or medical_conditions == "none":
        return exercises

    safe = []

    for ex in exercises:
        # 🚨 HARD GUARD — THIS FIXES YOUR ERROR
        if not isinstance(ex, dict):
            continue

        avoid = ex.get("avoid_if", [])

        # medical_conditions may be list or string
        if isinstance(medical_conditions, str):
            conditions = [medical_conditions]
        else:
            conditions = medical_conditions

        if not any(cond in avoid for cond in conditions):
            safe.append(ex)

    return safe

# ------------------------------
# Safety modifiers for injuries
# ------------------------------

def apply_injuries(exercises, injuries):
    if not injuries or injuries == "none":
        return exercises

    safe = []

    for ex in exercises:
        if not isinstance(ex, dict):
            continue

        avoid = ex.get("avoid_if", [])

        if isinstance(injuries, str):
            injury_list = [injuries]
        else:
            injury_list = injuries

        if not any(injury in avoid for injury in injury_list):
            safe.append(ex)

    return safe

# ------------------------------
# Combined modifier function
# ------------------------------

def apply_safety_filters(exercises, medical_conditions=[], injuries=[]):
    """
    Applies all safety filters to a list of exercises.
    Returns only safe exercises.
    """
    exercises = apply_medical_conditions(exercises, medical_conditions)
    exercises = apply_injuries(exercises, injuries)
    return exercises

# ------------------------------
# Example usage
# ------------------------------
if __name__ == "__main__":
    from engine.logic import generate_weekly_plan

    # Example: beginner muscle gain with joint issues
    goal = "muscle_gain"
    experience = "beginner"
    medical_conditions = ["joint_issues"]
    injuries = ["knee"]

    plan = generate_weekly_plan(goal, experience, medical_conditions, available_days=6)

    for i, day in enumerate(plan, 1):
        print(f"Day {i}: {day['day_type']}")
        safe_exs = apply_safety_filters(day["exercises"], medical_conditions, injuries)
        for ex in safe_exs:
            print(f"  - {ex['name']} | Sets: {ex.get('sets', '-')}, Reps/Time: {ex.get('reps', ex.get('time', '-'))}")
        print()
