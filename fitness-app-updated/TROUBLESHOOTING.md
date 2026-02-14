# 🔧 TROUBLESHOOTING GUIDE - RoutineX Fitness App

## 🚨 CRITICAL FIXES - READ THIS FIRST!

This guide addresses the two main issues:
1. **Database Error**: `no such column: win_date`
2. **API Error**: "Could not generate with any available model"

---

## ❌ ISSUE #1: Database Error - `no such column: win_date`

### What Causes This?
When you click on the Profile page, you see:
```
sqlite3.OperationalError: no such column: win_date
```

This happens because an older version of the database was created without the `win_date` column.

### ✅ SOLUTION - Two Options:

#### **OPTION A: Run the Migration Script (Keeps Your Data)**
```bash
python migrate_database.py
```

This will:
- Add the missing `win_date` column
- Update existing records
- Preserve all your data

#### **OPTION B: Delete the Database (Fresh Start)**
1. Close the app completely
2. Delete the file `routinex.db` in the fitness-app folder
3. Restart the app - it will create a fresh database

**⚠️ WARNING**: Option B will delete all your saved data!

---

## ❌ ISSUE #2: API Generation Fails

### What You See:
When you try to generate workout or diet plans:
```
Workout generation failed: Could not generate Month 1 with any available model.
Diet generation failed: Could not generate plan with any available model.
```

### Root Causes:
1. **Missing or Invalid API Key**
2. **No API Quota Available**
3. **Wrong API Key Format**
4. **Network/Connection Issues**

### ✅ SOLUTION - Step by Step:

#### **STEP 1: Check Your API Key**

1. Open the `.env` file in the `fitness-app` folder
2. Make sure it looks like this:
   ```
   GEMINI_API_KEY=AIzaSy...your-actual-key-here...
   ```

3. Verify there are:
   - ✅ NO spaces around the `=` sign
   - ✅ NO quotes around the key
   - ✅ NO extra lines or comments

**❌ WRONG:**
```
GEMINI_API_KEY = "AIzaSy..."    ❌ Has spaces and quotes
# GEMINI_API_KEY=AIzaSy...       ❌ Is commented out
```

**✅ CORRECT:**
```
GEMINI_API_KEY=AIzaSyDhB3xXxXxXxXxXxXxXxXxXxXxX
```

#### **STEP 2: Get a Valid API Key**

1. Go to: https://makersuite.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the entire key (starts with `AIzaSy`)
4. Paste it in your `.env` file
5. Save the file

#### **STEP 3: Verify API Key Has Quota**

1. Go to: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com
2. Check your quota and usage
3. Make sure you haven't exceeded free tier limits:
   - **Free Tier**: 60 requests per minute
   - If exceeded, wait 1 minute and try again

#### **STEP 4: Test Your API Key**

Run this test script:

```python
# test_api.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"API Key loaded: {api_key[:10]}..." if api_key else "❌ No API key found!")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello")
        print("✅ API is working!")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ API Error: {e}")
else:
    print("❌ Please add GEMINI_API_KEY to .env file")
```

Save as `test_api.py` and run:
```bash
python test_api.py
```

#### **STEP 5: Check Network/Firewall**

If API key is valid but still not working:
1. Check your internet connection
2. Try disabling VPN temporarily
3. Check if your firewall is blocking Python
4. Try a different network

---

## 🔍 DETAILED ERROR MESSAGES

The updated code now shows more details when errors occur:

### If You See:
```
Attempted models: gemini-1.5-flash, gemini-1.5-pro, gemini-pro
Last error: 403 API key not valid
```
**FIX**: Your API key is invalid. Get a new one from Google AI Studio.

### If You See:
```
Last error: 429 Quota exceeded
```
**FIX**: You've hit the rate limit. Wait 60 seconds and try again.

### If You See:
```
Last error: The model 'models/gemini-1.5-flash' does not exist
```
**FIX**: Your API key doesn't have access to Gemini models. Make sure you're using a Gemini API key, not a different Google API key.

---

## 🎯 QUICK CHECKLIST

Before running the app, verify:

- [ ] `routinex.db` doesn't exist OR you've run `migrate_database.py`
- [ ] `.env` file exists in the `fitness-app` folder
- [ ] `GEMINI_API_KEY` is in `.env` with no spaces or quotes
- [ ] API key is from https://makersuite.google.com/app/apikey
- [ ] API key starts with `AIzaSy`
- [ ] You have internet connection
- [ ] You haven't exceeded quota (60 requests/min)

---

## 🚀 RECOMMENDED STARTUP SEQUENCE

```bash
# 1. Navigate to the app folder
cd fitness-app

# 2. Run database migration (if database exists)
python migrate_database.py

# 3. Test your API key (optional but recommended)
python test_api.py

# 4. Run the app
streamlit run app.py
```

---

## 📊 MODELS USED (in priority order)

The app will try these models in order:
1. `gemini-1.5-flash` - Most reliable, free tier
2. `gemini-1.5-pro` - More capable, may need paid tier
3. `gemini-pro` - Older stable model

If ALL fail, there's an issue with your API key or quota.

---

## 💡 COMMON MISTAKES

### Mistake #1: Wrong API Key Type
❌ Using Google Cloud API key instead of Gemini API key
✅ Use key from https://makersuite.google.com/app/apikey

### Mistake #2: Spaces in .env
❌ `GEMINI_API_KEY = AIzaSy...`
✅ `GEMINI_API_KEY=AIzaSy...`

### Mistake #3: Running Old Database
❌ Using `routinex.db` from old version
✅ Delete old database OR run `migrate_database.py`

### Mistake #4: Exceeding Quota
❌ Spamming generate button
✅ Wait 60 seconds between attempts if you hit rate limit

---

## 🆘 STILL NOT WORKING?

### Check Console Output
Look at the terminal/command prompt where you ran `streamlit run app.py`.
The error messages there are more detailed than what shows in the browser.

### Enable Debug Mode
Add this to the top of `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show more detailed error messages.

### Last Resort - Clean Install
1. Delete `routinex.db`
2. Delete `.env`
3. Create new `.env` with fresh API key
4. Run `streamlit run app.py`

---

## 📞 ADDITIONAL RESOURCES

- **Gemini API Documentation**: https://ai.google.dev/docs
- **Get API Key**: https://makersuite.google.com/app/apikey
- **Check Quota**: https://console.cloud.google.com/
- **Streamlit Docs**: https://docs.streamlit.io/

---

## ✅ VERIFICATION TESTS

### Test 1: Database
```python
import sqlite3
conn = sqlite3.connect("routinex.db")
c = conn.cursor()
c.execute("PRAGMA table_info(daily_wins)")
columns = [col[1] for col in c.fetchall()]
print("win_date exists:", "win_date" in columns)
conn.close()
```
**Expected**: `win_date exists: True`

### Test 2: API Key
```python
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print(f"Key found: {bool(key)}, starts correctly: {key.startswith('AIzaSy') if key else False}")
```
**Expected**: `Key found: True, starts correctly: True`

---

**Last Updated**: February 14, 2026
**Version**: 1.0.2 (Fixed)
