import json
import os
import itertools

# ---------- Load constraints ----------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, "config/workout_constraints.json")) as f:
    CONSTRAINTS = json.load(f)["global_constraints"]


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# ---------- Helper ----------

def is_high_intensity(workout_type):
    return workout_type in ["hiit"]


# ---------- Main allocator ----------

def allocate_week(
    weekly_schedule: dict,
    profile: dict,
    available_days: int = 7
) -> dict:

    days = DAYS[:available_days]
    plan = {day: "rest" for day in days}

    # Expand workouts into list
    workout_pool = []
    for workout, count in weekly_schedule.items():
        if workout != "rest":
            workout_pool.extend([workout] * count)

    # Prioritize order: strength → cardio → mobility → hiit
    priority_order = ["strength", "cardio", "mobility", "hiit"]
    workout_pool.sort(key=lambda x: priority_order.index(x))

    day_index = 0
    last_workout = None
    hiit_used = 0

    for workout in workout_pool:
        placed = False

        for _ in range(len(days)):
            day = days[day_index]

            # Skip if day already assigned
            if plan[day] != "rest":
                day_index = (day_index + 1) % len(days)
                continue

            # Constraint: no consecutive HIIT
            if (
                workout == "hiit"
                and last_workout == "hiit"
                and CONSTRAINTS["no_consecutive_hiit_days"]
            ):
                day_index = (day_index + 1) % len(days)
                continue

            # Constraint: rest after HIIT
            if (
                last_workout == "hiit"
                and workout != "rest"
                and CONSTRAINTS["rest_after_hiit"]
            ):
                day_index = (day_index + 1) % len(days)
                continue

            # Assign workout
            plan[day] = workout
            last_workout = workout

            if workout == "hiit":
                hiit_used += 1

            placed = True
            day_index = (day_index + 1) % len(days)
            break

        if not placed:
            # Fallback: place wherever possible
            for day in days:
                if plan[day] == "rest":
                    plan[day] = workout
                    break

    return plan

from engine.profiler import profile_user
from engine.scheduler import generate_weekly_schedule
from engine.allocator import allocate_week

profile = profile_user(
    age=28,
    height_cm=178,
    weight_kg=74,
    experience="advanced",
    medical_conditions=[]
)

weekly = generate_weekly_schedule(
    profile=profile,
    goal="muscle_gain",
    available_days=6
)

daily_plan = allocate_week(
    weekly_schedule=weekly,
    profile=profile,
    available_days=6
)

print(weekly)
print(daily_plan)

