# 🚀 QUICK START GUIDE - RoutineX Fitness App

## ⚡ GET UP AND RUNNING IN 5 MINUTES

Follow these steps **IN ORDER**:

---

## 📦 STEP 1: Extract the Files

1. Extract `fitness-app-fixed-v2.zip`
2. Open the `fitness-app` folder
3. You should see files like `app.py`, `requirements.txt`, etc.

---

## 🔑 STEP 2: Get Your API Key

1. Go to: **https://makersuite.google.com/app/apikey**
2. Click **"Create API Key"** or **"Get API Key"**
3. Copy the entire key (it starts with `AIzaSy`)
4. Keep this window open - you'll need it in the next step

**⚠️ IMPORTANT**: Use the key from Google AI Studio (makersuite), NOT from Google Cloud Console!

---

## 📝 STEP 3: Create .env File

1. Open the `fitness-app` folder
2. Create a new file named `.env` (yes, it starts with a dot)
3. Add this line (replace with YOUR key):
   ```
   GEMINI_API_KEY=AIzaSyDhB3xXxXxXxXxXxXxXxXxXxXxX
   ```
4. Save the file

**⚠️ COMMON MISTAKES TO AVOID:**
- ❌ Don't add spaces: `GEMINI_API_KEY = AIzaSy...`
- ❌ Don't add quotes: `GEMINI_API_KEY="AIzaSy..."`
- ✅ Correct format: `GEMINI_API_KEY=AIzaSy...`

---

## 🗄️ STEP 4: Fix Database (If You Had Old Version)

**Only do this if you previously used an older version of the app.**

### Option A: Fresh Start (Recommended)
Delete `routinex.db` if it exists in the fitness-app folder.
The app will create a new one when you start it.

### Option B: Keep Your Data
Open a terminal/command prompt in the fitness-app folder and run:
```bash
python migrate_database.py
```

---

## 📚 STEP 5: Install Dependencies

Open a terminal/command prompt in the `fitness-app` folder and run:

```bash
pip install -r requirements.txt
```

Wait for all packages to install (may take 1-2 minutes).

---

## ✅ STEP 6: Test Your API Key (Recommended)

Before running the full app, test if your API key works:

```bash
python test_api.py
```

**What you should see:**
```
✅ API Key loaded: AIzaSyDhB3xXxX...
✅ Key format looks correct
   Testing gemini-1.5-flash... ✅ WORKING
   Testing gemini-1.5-pro... ✅ WORKING
   Testing gemini-pro... ✅ WORKING

🎉 SUCCESS! Your API key is working correctly!
```

**If you see errors**, refer to the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) file.

---

## 🎯 STEP 7: Run the App

In the terminal/command prompt, run:

```bash
streamlit run app.py
```

The app should open in your browser at: **http://localhost:8501**

---

## 🎊 SUCCESS! Now What?

### First-Time Setup:
1. **Create an Account**: Click on "Profile" → Sign Up
2. **Generate a Plan**: Go to "Planner" → Choose "Combined Workout + Diet"
3. **Fill the Form**: Enter your details (age, weight, goals, etc.)
4. **Click Generate**: Wait 10-30 seconds for AI to create your plan
5. **View Results**: Click through the tabs to see your workout and diet plans

### Features to Explore:
- 💪 **Workout Plans**: Progressive training schedules
- 🥗 **Diet Plans**: Weekly meal plans with macros
- 🧘 **Mental Health**: Mood tracking and journaling
- 📊 **Profile**: View all your saved plans
- ✅ **Daily Check-in**: Track your progress (if enabled)

---

## ⚠️ COMMON ISSUES & QUICK FIXES

### Issue: "Could not generate with any available model"

**Cause**: API key problem

**Fix**:
1. Run `python test_api.py`
2. Check if your API key is correct in `.env`
3. Make sure you have internet connection
4. Wait 60 seconds if you just created the API key

### Issue: "no such column: win_date"

**Cause**: Old database structure

**Fix**:
1. Run `python migrate_database.py`
   OR
2. Delete `routinex.db` and restart the app

### Issue: Spinner text is invisible

**Cause**: Already fixed in this version!

**Verification**: Text should be white on dark background when generating plans.

### Issue: Diet plan shows code instead of formatted plan

**Cause**: Already fixed in this version!

**Verification**: Diet should show as cards with meals and macros, not raw JSON.

---

## 📊 SYSTEM REQUIREMENTS

- **Python**: 3.8 or higher
- **Internet**: Required for AI generation
- **Browser**: Modern browser (Chrome, Firefox, Edge, Safari)
- **API Key**: Free Google AI Studio API key

---

## 🆘 STILL NEED HELP?

1. **Check the terminal/console**: Error messages appear there first
2. **Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**: Detailed solutions for all issues
3. **Run test_api.py**: Diagnose API key issues
4. **Run migrate_database.py**: Fix database issues

---

## 📋 CHECKLIST - Before Asking for Help

- [ ] Python 3.8+ is installed (`python --version`)
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] `.env` file exists with `GEMINI_API_KEY=...`
- [ ] API key is from https://makersuite.google.com/app/apikey
- [ ] API key starts with `AIzaSy`
- [ ] `python test_api.py` shows at least one working model
- [ ] No `routinex.db` file OR ran `migrate_database.py`
- [ ] Internet connection is working
- [ ] Tried restarting the app

---

## 🎓 TIPS FOR BEST RESULTS

### For Workout Plans:
- Be specific about available equipment
- Mention injuries or limitations
- Choose realistic available days per week

### For Diet Plans:
- Specify dietary restrictions clearly
- Choose cuisine preferences
- Set realistic calorie targets

### Rate Limits:
- Free tier allows **60 requests per minute**
- If you hit the limit, wait 60 seconds
- Don't spam the generate button

---

## 🔄 UPDATING THE APP

If you get a new version:
1. Extract the new files to a different folder
2. Copy your `.env` file to the new folder
3. Copy `routinex.db` to the new folder (if you want to keep data)
4. Run `pip install -r requirements.txt` again
5. Run the app: `streamlit run app.py`

---

## 💡 BEST PRACTICES

### Do's ✅
- Create an account to save your plans
- Test API key before generating plans
- Wait for generation to complete (10-30 seconds)
- Keep your API key private

### Don'ts ❌
- Don't share your API key with others
- Don't spam the generate button
- Don't run multiple instances simultaneously
- Don't edit database files manually

---

**Ready to Transform Your Fitness Journey? Let's Go! 🚀**

---

**Last Updated**: February 14, 2026  
**Version**: 1.0.2 (Fixed)
