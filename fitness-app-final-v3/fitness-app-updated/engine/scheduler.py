import os
import json
import re
from dotenv import load_dotenv
from .ai_handler import generate_with_ai

load_dotenv()

def extract_json_from_text(text):
    """Extract JSON from AI response, handling markdown and extra text."""
    text = text.strip()
    
    # Remove markdown code blocks
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        parts = text.split("```")
        if len(parts) >= 3:
            text = parts[1]
    
    # Find first { and last }
    start = text.find("{")
    end = text.rfind("}")
    
    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]
    
    return text.strip()


def generate_workout_plan(profile, goal, duration_months, additional_info=""):
    """
    Generates a detailed week-by-week workout plan by iterating through each month.
    """
    
    full_schedule = []
    overall_summary = ""
    
    for current_month in range(1, duration_months + 1):
        
        start_week = ((current_month - 1) * 4) + 1
        
        # Simplified, clearer prompt
        prompt = f"""Create a 4-week workout plan for Month {current_month}.

USER: Goal={goal}, Experience={profile.get('experience')}, Injuries={', '.join(profile.get('injuries', [])) or 'None'}

Generate weeks {start_week} to {start_week+3}. Return ONLY valid JSON:

{{
  "month_summary": "Month {current_month} description",
  "weeks": [
    {{"week_number": {start_week}, "focus": "Strength", "workouts": [{{"day": "Monday", "focus": "Chest", "exercises": ["Bench 4x8", "Dips 3x10"]}}, {{"day": "Tuesday", "focus": "Back", "exercises": ["Pullups 4x8", "Rows 4x8"]}}, {{"day": "Wednesday", "focus": "Rest", "exercises": []}}, {{"day": "Thursday", "focus": "Legs", "exercises": ["Squats 4x8", "Lunges 3x10"]}}, {{"day": "Friday", "focus": "Shoulders", "exercises": ["Press 4x8", "Raises 3x12"]}}, {{"day": "Saturday", "focus": "Cardio", "exercises": ["Run 20min"]}}, {{"day": "Sunday", "focus": "Rest", "exercises": []}}]}},
    {{"week_number": {start_week+1}, "focus": "Hypertrophy", "workouts": [{{"day": "Monday", "focus": "Chest", "exercises": ["Incline 4x10", "Flyes 3x12"]}}, {{"day": "Tuesday", "focus": "Back", "exercises": ["Deadlifts 4x6", "Pulldowns 3x12"]}}, {{"day": "Wednesday", "focus": "Rest", "exercises": []}}, {{"day": "Thursday", "focus": "Legs", "exercises": ["Front Squats 4x10", "RDLs 3x10"]}}, {{"day": "Friday", "focus": "Shoulders", "exercises": ["Arnold Press 4x10", "Rows 3x12"]}}, {{"day": "Saturday", "focus": "Full Body", "exercises": ["Burpees 3x10"]}}, {{"day": "Sunday", "focus": "Rest", "exercises": []}}]}},
    {{"week_number": {start_week+2}, "focus": "Power", "workouts": [{{"day": "Monday", "focus": "Chest", "exercises": ["Bench 5x5", "Close-grip 4x8"]}}, {{"day": "Tuesday", "focus": "Back", "exercises": ["Pullups 5x5", "T-Bar 4x8"]}}, {{"day": "Wednesday", "focus": "Rest", "exercises": []}}, {{"day": "Thursday", "focus": "Legs", "exercises": ["Squats 5x5", "Split Squats 3x10"]}}, {{"day": "Friday", "focus": "Shoulders", "exercises": ["Military Press 5x5", "Shrugs 4x12"]}}, {{"day": "Saturday", "focus": "HIIT", "exercises": ["Sprints 10x30s"]}}, {{"day": "Sunday", "focus": "Rest", "exercises": []}}]}},
    {{"week_number": {start_week+3}, "focus": "Deload", "workouts": [{{"day": "Monday", "focus": "Chest", "exercises": ["Light Bench 3x10"]}}, {{"day": "Tuesday", "focus": "Back", "exercises": ["Light Rows 3x10"]}}, {{"day": "Wednesday", "focus": "Rest", "exercises": []}}, {{"day": "Thursday", "focus": "Legs", "exercises": ["Goblet Squats 3x12"]}}, {{"day": "Friday", "focus": "Shoulders", "exercises": ["Light Press 3x10"]}}, {{"day": "Saturday", "focus": "Walk", "exercises": ["Walking 30min"]}}, {{"day": "Sunday", "focus": "Rest", "exercises": []}}]}}
  ]
}}"""

        # Try up to 3 times
        max_retries = 3
        for attempt in range(max_retries):
            try:
                success, response_text, error = generate_with_ai(prompt, max_tokens=8192, key_type='workout')
                
                if not success:
                    if attempt < max_retries - 1:
                        continue
                    return {
                        "error": f"Could not generate Month {current_month}",
                        "details": str(error),
                        "partial_data": full_schedule
                    }
                
                # Extract and parse JSON
                raw_text = extract_json_from_text(response_text)
                month_data = json.loads(raw_text)
                
                # Validate
                if "weeks" not in month_data:
                    raise ValueError("Missing 'weeks' field")
                
                # Success!
                full_schedule.extend(month_data["weeks"])
                
                if current_month == 1:
                    overall_summary = month_data.get("month_summary", "")
                
                break
                
            except (json.JSONDecodeError, ValueError) as e:
                if attempt < max_retries - 1:
                    continue
                print(f"ERROR Month {current_month}: {str(e)}")
                print(f"Response: {response_text[:300]}")
                return {
                    "error": f"Invalid JSON for Month {current_month}",
                    "details": f"Parse error: {str(e)}",
                    "partial_data": full_schedule
                }
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                return {
                    "error": f"Error Month {current_month}", 
                    "details": str(e),
                    "partial_data": full_schedule
                }

    return {
        "summary": f"A {duration_months}-month progressive plan. {overall_summary}",
        "schedule": full_schedule
    }