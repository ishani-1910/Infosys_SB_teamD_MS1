import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Fallback for API key
if not api_key:
    api_key = os.environ.get("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

def generate_workout_plan(profile, goal, duration_months, additional_info=""):
    """
    Generates a detailed week-by-week workout plan by iterating through each month.
    Ensures that 3 months = 12 distinct weeks.
    """
    
    full_schedule = []
    overall_summary = ""
    
    # We will loop through each month to guarantee detail
    for current_month in range(1, duration_months + 1):
        
        # Calculate the week numbers for this month (e.g., Month 1 = Weeks 1-4, Month 2 = Weeks 5-8)
        start_week = ((current_month - 1) * 4) + 1
        end_week = current_month * 4
        
        # Context for the specific month
        user_details = f"""
        - **User Profile:**
          - Goal: {goal}
          - Experience: {profile.get('experience')}
          - Injuries: {', '.join(profile.get('injuries', []))}
          - Equipment/Notes: "{additional_info}"
        
        - **Current Phase:** MONTH {current_month} of {duration_months}.
        - **Weeks to Generate:** Week {start_week} to Week {end_week}.
        """

        # Prompt tailored for the specific month
        prompt = f"""
        You are an elite fitness coach building a long-term plan.
        We are currently planning **Month {current_month}** (Weeks {start_week}-{end_week}).

        **CONTEXT:**
        {user_details}

        **INSTRUCTIONS:**
        1. Generate a detailed routine for **Weeks {start_week}, {start_week+1}, {start_week+2}, and {start_week+3}**.
        2. **Progression:**
           - If this is Month 1: Focus on stability and form.
           - If this is a Middle Month: Increase intensity/volume (Progressive Overload).
           - If this is the Final Month: Peak intensity or cutting.
        3. **Format:** Return valid JSON with a list of 4 specific weeks.

        **JSON OUTPUT FORMAT:**
        {{
            "month_summary": "Specific goal for this month.",
            "weeks": [
                {{
                    "week_number": {start_week},
                    "focus": "Hypertrophy / Strength / etc",
                    "workouts": [
                        {{ "day": "Monday", "focus": "Chest & Tri", "exercises": ["Bench Press - 3x10", "..."] }},
                        ... (7 days)
                    ]
                }},
                ... (Repeat for all 4 weeks of this month)
            ]
        }}
        """

        try:
            # Generate this month's chunk
            model = genai.GenerativeModel('gemini-2.5-flash') 
            response = model.generate_content(prompt)
            
            raw_text = response.text.strip()
            # Clean JSON formatting
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "", 1).replace("```", "", 1)
            
            month_data = json.loads(raw_text)
            
            # Append this month's weeks to the master plan
            if "weeks" in month_data:
                full_schedule.extend(month_data["weeks"])
            
            # Capture the summary from the first month as the main intro
            if current_month == 1:
                overall_summary = month_data.get("month_summary", "Follow the plan below.")

        except Exception as e:
            # If a month fails, return what we have with an error note
            return {
                "error": f"Error generating Month {current_month}: {str(e)}", 
                "partial_data": full_schedule
            }

    # Return the complete stacked list
    return {
        "summary": f"A {duration_months}-month progressive plan. {overall_summary}",
        "schedule": full_schedule
    }