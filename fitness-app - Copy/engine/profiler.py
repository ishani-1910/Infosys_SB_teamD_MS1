import json
import os

# ---------- Load JSON configs ----------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, "config/capacity_rules.json")) as f:
    CAPACITY_RULES = json.load(f)["capacity_tiers"]

with open(os.path.join(BASE_DIR, "config/medical_rules.json")) as f:
    MEDICAL_RULES = json.load(f)["medical_conditions"]

with open(os.path.join(BASE_DIR, "config/workout_constraints.json")) as f:
    WORKOUT_CONSTRAINTS = json.load(f)


# ---------- Helper functions ----------

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)


# ---------- Capacity scoring ----------

def score_age(age: int) -> int:
    if age < 30:
        return 3
    elif age < 45:
        return 2
    else:
        return 1


def score_bmi(bmi: float) -> int:
    if bmi < 25:
        return 3
    elif bmi < 30:
        return 2
    else:
        return 1


def score_experience(experience: str) -> int:
    return {
        "beginner": 1,
        "intermediate": 2,
        "advanced": 3
    }.get(experience, 1)


# ---------- Tier mapping ----------

def map_score_to_tier(total_score: int) -> str:
    if total_score <= 4:
        return "low"
    elif total_score <= 6:
        return "medium"
    else:
        return "high"


# ---------- Main profiler ----------

def profile_user(
    age: int,
    height_cm: float,
    weight_kg: float,
    experience: str,
    medical_conditions: list
) -> dict:

    bmi = calculate_bmi(weight_kg, height_cm)

    total_score = (
        score_age(age) +
        score_bmi(bmi) +
        score_experience(experience)
    )

    capacity_tier = map_score_to_tier(total_score)
    capacity_data = CAPACITY_RULES[capacity_tier]

    # ---------- Apply experience modifiers ----------
    exp_mod = WORKOUT_CONSTRAINTS["experience_modifiers"][experience]

    intensity_cap = exp_mod["intensity_cap"]
    hiit_allowed = capacity_data.get("hiit_allowed", False)

    if exp_mod["remove_hiit"]:
        hiit_allowed = False

    # ---------- Apply medical overrides ----------
    for condition in medical_conditions:
        if condition not in MEDICAL_RULES:
            continue

        medical_rule = MEDICAL_RULES[condition]

        if medical_rule["intensity_cap"]:
            intensity_cap = min(
                intensity_cap,
                medical_rule["intensity_cap"],
                key=lambda x: ["low", "medium", "high"].index(x)
            )

        if "hiit" in medical_rule["restrictions"]:
            hiit_allowed = False

    return {
        "bmi": bmi,
        "capacity_tier": capacity_tier,
        "intensity_cap": intensity_cap,
        "hiit_allowed": hiit_allowed,
        "max_workouts_per_week": capacity_data["max_workouts_per_week"],
        "mandatory_rest_days": capacity_data["mandatory_rest_days"],
        "session_duration_range": capacity_data["session_duration_minutes"]
    }
from engine.profiler import profile_user

profile = profile_user(
    age=35,
    height_cm=175,
    weight_kg=82,
    experience="beginner",
    medical_conditions=["hypertension"]
)

print(profile)
