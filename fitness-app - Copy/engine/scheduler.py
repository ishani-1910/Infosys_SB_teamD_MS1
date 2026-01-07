import random
from engine.exercises import EXERCISES
from engine.modifiers import apply_safety_filters


DAY_LIMITS = {
    "strength": 5,
    "cardio": 2,
    "mobility": 4,
    "hiit": 2,
}


def _clean_inputs(medical_conditions, injuries):
    if medical_conditions in (["none"], "none", None):
        medical_conditions = []
    if injuries in (["none"], "none", None):
        injuries = []
    return medical_conditions, injuries


def _generate_week_template(goal, days_per_week):
    templates = {
        "muscle_gain": ["strength", "strength", "rest", "strength", "cardio", "strength"],
        "fat_loss": ["strength", "cardio", "strength", "cardio", "mobility", "rest"],
        "general_fitness": ["strength", "cardio", "mobility", "strength", "rest"],
        "endurance": ["cardio", "cardio", "strength", "cardio", "mobility"],
        "mobility_flexibility": ["mobility", "mobility", "cardio", "mobility", "rest"],
    }

    pattern = templates.get(goal, templates["general_fitness"])
    return {f"Day {i+1}": pattern[i % len(pattern)] for i in range(days_per_week)}


def _sample(exercises, limit):
    return random.sample(exercises, min(len(exercises), limit))


def _build_strength_day(pool):
    buckets = {
        "lower_body": [],
        "upper_push": [],
        "upper_pull": [],
        "core": [],
    }

    for ex in pool:
        for g in ex.get("group", []):
            if g in buckets:
                buckets[g].append(ex)

    selected = []
    for group in buckets.values():
        if group:
            selected.append(random.choice(group))

    leftovers = [ex for ex in pool if ex not in selected]
    selected += _sample(leftovers, DAY_LIMITS["strength"] - len(selected))

    return selected[:DAY_LIMITS["strength"]]


def create_weekly_schedule(goal, experience, medical_conditions, injuries, days_per_week):
    medical_conditions, injuries = _clean_inputs(medical_conditions, injuries)
    template = _generate_week_template(goal, days_per_week)

    plan = {}

    for day, day_type in template.items():
        if day_type == "rest":
            plan[day] = []
            continue

        if day_type == "strength":
            pool = [
                ex for group in EXERCISES["strength"].values()
                for ex in group if ex["level"] == experience
            ]
            exercises = _build_strength_day(pool)

        else:
            pool = []
            for ex in EXERCISES[day_type]:
                if isinstance(ex, dict):
                    if ex.get("level", experience) == experience:
                        pool.append(ex)
                else:
                    # ex is a string (exercise name)
                    pool.append(ex)

            exercises = _sample(pool, DAY_LIMITS[day_type])

        if medical_conditions or injuries:
            exercises = apply_safety_filters(exercises, medical_conditions, injuries)

        if not exercises:
            exercises = _sample(pool, 3)

        plan[day] = exercises

    formatted = []

    for day_name, exercises in plan.items():
        formatted.append({
            "day": day_name,
            "day_type": template[day_name],  # <-- USE ORIGINAL DAY TYPE
            "exercises": exercises
        })

    return formatted
