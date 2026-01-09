EXERCISES = {

    "strength": {

        "lower_body": [
            {
                "name": "Bodyweight Squat",
                "level": "beginner",
                "joint_stress": "medium",
                "avoid_if": ["joint_issues"],
                "sets": 3,
                "reps": "12-15"
            },
            {
                "name": "Goblet Squat",
                "level": "intermediate",
                "joint_stress": "medium",
                "avoid_if": ["joint_issues"],
                "sets": 4,
                "reps": "8-12"
            },
            {
                "name": "Leg Press",
                "level": "beginner",
                "joint_stress": "medium",
                "avoid_if": ["joint_issues"],
                "sets": 3,
                "reps": "10-12"
            },
            {
                "name": "Glute Bridge",
                "level": "beginner",
                "joint_stress": "low",
                "avoid_if": [],
                "sets": 3,
                "reps": "12-15"
            },
            {
                "name": "Hip Thrust",
                "level": "intermediate",
                "joint_stress": "medium",
                "avoid_if": [],
                "sets": 4,
                "reps": "8-12"
            },
            {
                "name": "Romanian Deadlift",
                "level": "intermediate",
                "joint_stress": "medium",
                "avoid_if": ["back"],
                "sets": 4,
                "reps": "6-10"
            },
            {
                "name": "Step-ups",
                "level": "beginner",
                "joint_stress": "medium",
                "avoid_if": ["knee"],
                "sets": 3,
                "reps": "10-12"
            },
            {
                "name": "Split Squat",
                "level": "intermediate",
                "joint_stress": "medium",
                "avoid_if": ["knee"],
                "sets": 3,
                "reps": "8-10"
            }
        ],

        "upper_push": [
            {
                "name": "Push-ups",
                "level": "beginner",
                "joint_stress": "low",
                "avoid_if": ["shoulder"],
                "sets": 3,
                "reps": "8-12"
            },
            {
                "name": "Incline Push-ups",
                "level": "beginner",
                "joint_stress": "low",
                "avoid_if": ["shoulder"],
                "sets": 3,
                "reps": "10-15"
            },
            {
                "name": "Bench Press",
                "level": "intermediate",
                "joint_stress": "medium",
                "avoid_if": ["shoulder"],
                "sets": 4,
                "reps": "6-10"
            },
            {
                "name": "Dumbbell Bench Press",
                "level": "intermediate",
                "joint_stress": "medium",
                "avoid_if": ["shoulder"],
                "sets": 4,
                "reps": "8-12"
            },
            {
                "name": "Dumbbell Shoulder Press",
                "level": "intermediate",
                "joint_stress": "medium",
                "avoid_if": ["shoulder"],
                "sets": 3,
                "reps": "8-12"
            },
            {
                "name": "Machine Chest Press",
                "level": "beginner",
                "joint_stress": "low",
                "avoid_if": ["shoulder"],
                "sets": 3,
                "reps": "10-12"
            }
        ],

        "upper_pull": [
            {
                "name": "Lat Pulldown",
                "level": "beginner",
                "joint_stress": "low",
                "avoid_if": [],
                "sets": 3,
                "reps": "10-12"
            },
            {
                "name": "Seated Cable Row",
                "level": "beginner",
                "joint_stress": "low",
                "avoid_if": [],
                "sets": 3,
                "reps": "10-12"
            },
            {
                "name": "Dumbbell Row",
                "level": "intermediate",
                "joint_stress": "medium",
                "avoid_if": ["back"],
                "sets": 4,
                "reps": "8-12"
            },
            {
                "name": "Assisted Pull-ups",
                "level": "intermediate",
                "joint_stress": "medium",
                "avoid_if": ["shoulder"],
                "sets": 3,
                "reps": "6-10"
            },
            {
                "name": "Face Pulls",
                "level": "beginner",
                "joint_stress": "low",
                "avoid_if": [],
                "sets": 3,
                "reps": "12-15"
            }
        ],

        "core": [
            {
                "name": "Plank",
                "level": "beginner",
                "joint_stress": "low",
                "avoid_if": [],
                "sets": 3,
                "reps": "30-45 sec"
            },
            {
                "name": "Dead Bug",
                "level": "beginner",
                "joint_stress": "low",
                "avoid_if": [],
                "sets": 3,
                "reps": "10-12"
            },
            {
                "name": "Bird Dog",
                "level": "beginner",
                "joint_stress": "low",
                "avoid_if": [],
                "sets": 3,
                "reps": "10-12"
            },
            {
                "name": "Hanging Knee Raises",
                "level": "intermediate",
                "joint_stress": "medium",
                "avoid_if": ["back"],
                "sets": 3,
                "reps": "8-12"
            },
            {
                "name": "Cable Crunch",
                "level": "intermediate",
                "joint_stress": "low",
                "avoid_if": [],
                "sets": 3,
                "reps": "12-15"
            }
        ]
    },

    "cardio": {
        "low_impact": [
            {"name": "Brisk Walking", "avoid_if": [], "time": "20-40 min"},
            {"name": "Cycling", "avoid_if": [], "time": "30-45 min"},
            {"name": "Stationary Bike", "avoid_if": [], "time": "30-45 min"},
            {"name": "Elliptical", "avoid_if": [], "time": "20-30 min"},
            {"name": "Swimming", "avoid_if": [], "time": "20-30 min"}
        ],
        "moderate": [
            {"name": "Jogging", "avoid_if": ["joint_issues"], "time": "20-30 min"},
            {"name": "Rowing Machine", "avoid_if": ["back"], "time": "15-25 min"},
            {"name": "Stair Climber", "avoid_if": ["knee"], "time": "15-20 min"}
        ],
        "high_impact": [
            {"name": "Running", "avoid_if": ["joint_issues"], "time": "20-30 min"},
            {"name": "Jump Rope", "avoid_if": ["joint_issues"], "time": "10-15 min"},
            {"name": "Sprint Intervals", "avoid_if": ["cardiac"], "time": "10-15 min"}
        ]
    },

    "mobility": [
        {"name": "Dynamic Stretching", "time": "10-15 min"},
        {"name": "Hip Mobility Flow", "time": "10-15 min"},
        {"name": "Shoulder Mobility Flow", "time": "10-15 min"},
        {"name": "Hamstring Stretch", "time": "5-10 min"},
        {"name": "Yoga Flow", "time": "20-30 min"},
        {"name": "Foam Rolling", "time": "10-15 min"}
    ],

    "hiit": [
        {"name": "Bike Intervals", "avoid_if": ["cardiac", "hypertension"], "time": "15-20 min"},
        {"name": "Bodyweight Circuit", "avoid_if": ["joint_issues", "cardiac"], "time": "15-20 min"},
        {"name": "Kettlebell Swings", "avoid_if": ["back"], "time": "10-15 min"},
        {"name": "Battle Ropes", "avoid_if": ["shoulder"], "time": "10-15 min"}
    ]
}
