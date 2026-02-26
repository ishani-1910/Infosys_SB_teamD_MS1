# 🔑 API Setup Guide - RoutineX

## Overview

RoutineX now supports **TWO AI providers**:
1. **Google Gemini** (Recommended - Free tier available)
2. **OpenAI** (Fallback - Paid)

You need at least ONE API key for the app to work. Having BOTH provides better reliability!

---

## 🎯 Quick Decision Guide

### Use GEMINI if:
- ✅ You want a **free option**
- ✅ You're just testing or personal use
- ✅ 60 requests per minute is enough
- ✅ You're okay with occasional rate limits

### Use OPENAI if:
- ✅ You need **high reliability**
- ✅ You hit rate limits frequently
- ✅ You're okay with **paying per request**
- ✅ You need faster generation

### Use BOTH if:
- ✅ You want **maximum reliability**
- ✅ Gemini as free primary, OpenAI as paid backup
- ✅ Best user experience

---

## 🔧 SETUP: Google Gemini (FREE)

### Step 1: Get Your API Key

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"** or **"Get API Key"**
4. Copy the key (starts with `AIzaSy...`)

### Step 2: Add to .env File

1. Open (or create) the `.env` file in the `fitness-app` folder
2. Add this line:
   ```
   GEMINI_API_KEY=AIzaSyYourActualKeyHere
   ```
3. Save the file

### Step 3: Test It

```bash
python engine/ai_handler.py
```

Should show: `Gemini: ✅ Working`

### Gemini Specs:
- **Cost**: FREE (with limits)
- **Free Tier**: 60 requests per minute
- **Model**: gemini-pro
- **Best for**: Testing, personal use
- **Limits**: Rate limits if generating many plans quickly

---

## 💳 SETUP: OpenAI (PAID)

### Step 1: Get Your API Key

1. Go to: **https://platform.openai.com/api-keys**
2. Sign in or create an OpenAI account
3. Click **"Create new secret key"**
4. Give it a name (e.g., "RoutineX")
5. Copy the key (starts with `sk-proj-...` or `sk-...`)
6. **IMPORTANT**: Save it immediately - you can't see it again!

### Step 2: Add Credit Balance

1. Go to: **https://platform.openai.com/settings/organization/billing**
2. Add at least $5-$10 to start
3. Set usage limits if desired

### Step 3: Add to .env File

1. Open your `.env` file
2. Add this line:
   ```
   OPENAI_API_KEY=sk-proj-YourActualKeyHere
   ```
3. Save the file

### Step 4: Test It

```bash
python engine/ai_handler.py
```

Should show: `OpenAI: ✅ Working`

### OpenAI Specs:
- **Cost**: ~$0.01-0.02 per plan generation
- **Model**: gpt-4o-mini (most cost-effective)
- **Best for**: High reliability, frequent use
- **Limits**: Based on your account tier and balance

---

## 🚀 RECOMMENDED SETUP: BOTH APIS

### Why Use Both?

The app will automatically:
1. **Try Gemini first** (free)
2. **Fall back to OpenAI** if Gemini fails or is rate limited
3. Give you the **best of both worlds**

### Setup Both:

Your `.env` file should look like:

```env
# Primary (Free)
GEMINI_API_KEY=AIzaSyYourGeminiKeyHere

# Backup (Paid)
OPENAI_API_KEY=sk-proj-YourOpenAIKeyHere
```

### How It Works:

```
User clicks "Generate"
        ↓
  Try Gemini (free)
        ↓
  Success? → Use result ✅
        ↓ (if fails)
  Try OpenAI (paid)
        ↓
  Success? → Use result ✅
        ↓ (if both fail)
  Show error with details
```

---

## 💰 Cost Comparison

### Gemini (Free Tier):
- **Cost per plan**: FREE
- **Limit**: 60 requests/minute
- **Monthly cost**: $0 (for reasonable use)

### OpenAI (Paid):
- **Cost per workout plan**: ~$0.01-0.015
- **Cost per diet plan**: ~$0.01-0.015
- **Typical user (10 plans/week)**: ~$1-2/month

### Combined Strategy:
- Use Gemini for most generations (free)
- OpenAI kicks in only when needed
- **Best balance of cost and reliability**

---

## 🧪 Testing Your Setup

### Test Script

Run this to test which APIs are working:

```bash
python engine/ai_handler.py
```

### Expected Output:

```
====================================================================
🤖 AI API Test - RoutineX
====================================================================

Gemini: ✅ Working
OpenAI: ✅ Working

====================================================================
✅ At least one API is working! You're good to go.
```

### Troubleshooting Test Results:

#### `Gemini: ❌ Invalid Gemini API key`
- Get new key from https://makersuite.google.com/app/apikey
- Make sure no spaces in .env file
- Key should start with `AIzaSy`

#### `Gemini: ❌ Gemini rate limit exceeded`
- Wait 60 seconds and try again
- Consider adding OpenAI as backup

#### `OpenAI: ❌ Invalid OpenAI API key`
- Get new key from https://platform.openai.com/api-keys
- Make sure no spaces in .env file
- Key should start with `sk-`

#### `OpenAI: ❌ OpenAI quota exceeded`
- Add funds at https://platform.openai.com/settings/organization/billing
- Check your usage limits

---

## 📝 .env File Format

### ✅ CORRECT Format:

```env
GEMINI_API_KEY=AIzaSyDhB3xXxXxXxXxXxXxXxXxXxXxX
OPENAI_API_KEY=sk-proj-xXxXxXxXxXxXxXxXxXxXxXxXxXxX
```

### ❌ WRONG Formats:

```env
# ❌ Has spaces around =
GEMINI_API_KEY = AIzaSy...

# ❌ Has quotes
GEMINI_API_KEY="AIzaSy..."

# ❌ Is commented out
# GEMINI_API_KEY=AIzaSy...

# ❌ Has extra text
GEMINI_API_KEY=AIzaSy... # my key

# ❌ Wrong line endings
GEMINI_API_KEY=AIzaSy...\r\n
```

**Simple rule**: Just the key name, equals sign, and the key. Nothing else!

---

## 🔐 Security Best Practices

### DO:
- ✅ Keep `.env` file in `.gitignore`
- ✅ Never commit API keys to GitHub
- ✅ Rotate keys if exposed
- ✅ Set usage limits on OpenAI dashboard
- ✅ Use different keys for dev/production

### DON'T:
- ❌ Share your API keys with anyone
- ❌ Post keys in public forums/Discord
- ❌ Hardcode keys in your code
- ❌ Use the same key across multiple projects
- ❌ Leave unused keys active

---

## 🎯 Quick Start Checklist

- [ ] Got at least ONE API key (Gemini or OpenAI)
- [ ] Created `.env` file in `fitness-app` folder
- [ ] Added `GEMINI_API_KEY=...` and/or `OPENAI_API_KEY=...`
- [ ] No spaces, quotes, or extra text in `.env`
- [ ] Saved the `.env` file
- [ ] Ran `python engine/ai_handler.py` to test
- [ ] Saw at least one ✅ Working message
- [ ] Ready to run the app!

---

## 🆘 Still Having Issues?

### If Gemini doesn't work:
1. Make sure key is from https://makersuite.google.com/app/apikey
2. NOT from Google Cloud Console
3. Key should start with `AIzaSy`
4. Try creating a fresh key

### If OpenAI doesn't work:
1. Make sure you have credit balance
2. Check usage limits aren't hit
3. Key should start with `sk-`
4. Try creating a fresh key

### If BOTH don't work:
1. Check internet connection
2. Check `.env` file format (no spaces, quotes)
3. Try running the test script
4. Check the full error messages

---

## 📚 Additional Resources

### Gemini:
- **Get API Key**: https://makersuite.google.com/app/apikey
- **Documentation**: https://ai.google.dev/docs
- **Pricing**: https://ai.google.dev/pricing

### OpenAI:
- **Get API Key**: https://platform.openai.com/api-keys
- **Add Balance**: https://platform.openai.com/settings/organization/billing
- **Pricing**: https://openai.com/api/pricing/
- **Usage Dashboard**: https://platform.openai.com/usage

---

**You're all set! Run the app and generate your first plan! 🎉**

```bash
streamlit run app.py
```
