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

print("PROFILE:", profile)
print("WEEKLY:", weekly)
print("DAILY:", daily_plan)
