# 🚀 Quick Deployment Steps

Your project is ready to deploy! Follow these steps:

## Option 1: Streamlit Cloud (Easiest & Free)

### Step 1: Push to GitHub

1. **Create a GitHub account** (if you don't have one): https://github.com/signup

2. **Create a new repository** on GitHub:
   - Go to https://github.com/new
   - Repository name: `restaurant-review-analyzer`
   - Make it **Public**
   - DON'T initialize with README
   - Click "Create repository"

3. **Copy the repository URL** (it will look like):
   ```
   https://github.com/YOUR_USERNAME/restaurant-review-analyzer.git
   ```

4. **Run these commands** in your terminal (replace YOUR_USERNAME):

```powershell
cd "c:\Users\sdutt\OneDrive\Documents\Desktop\NLP\NLP Project Section B"

git branch -M main

git remote add origin https://github.com/YOUR_USERNAME/restaurant-review-analyzer.git

git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to: **https://share.streamlit.io/**

2. Click **"Sign in with GitHub"**

3. Click **"New app"**

4. Fill in the details:
   - **Repository**: Select `restaurant-review-analyzer`
   - **Branch**: `main`
   - **Main file path**: `app/streamlit_app.py`

5. Click **"Deploy!"**

6. Wait 3-5 minutes ⏱️

7. **Done!** 🎉 Your app will be live at:
   ```
   https://restaurant-review-analyzer-XXXX.streamlit.app
   ```

---

## Option 2: Run Locally with Public URL (Quick Test)

If you just want to share it temporarily without GitHub:

1. Install ngrok: https://ngrok.com/download

2. Run your app:
```powershell
streamlit run app/streamlit_app.py
```

3. In another terminal:
```powershell
ngrok http 8501
```

4. Share the ngrok URL (valid for 2 hours on free plan)

---

## What's Already Configured ✅

- ✅ `requirements.txt` - All dependencies
- ✅ `setup.sh` - Automatic spaCy model download
- ✅ `.streamlit/config.toml` - App configuration
- ✅ `packages.txt` - System dependencies
- ✅ `.gitignore` - Files to exclude from Git

---

## Need Help?

**Common Issues:**

1. **Git push asks for password?**
   - Use GitHub Personal Access Token instead of password
   - Go to GitHub Settings → Developer settings → Personal access tokens → Generate new token

2. **Streamlit Cloud deployment fails?**
   - Check the deployment logs
   - Make sure `app/streamlit_app.py` path is correct
   - Verify all files are pushed to GitHub

3. **App crashes on startup?**
   - Check if spaCy model is downloading correctly
   - Wait for the full deployment to complete

---

## Your App Features 🎯

✅ Real-time restaurant review analysis
✅ Sentiment detection (positive/negative/neutral)
✅ Aspect-based analysis (Food, Service, Ambiance, Price)
✅ 14+ cuisine types classification
✅ Named entity recognition (dishes, locations, people)
✅ Beautiful dark theme interface
✅ Sample reviews included

**Enjoy your deployed NLP application!** 🍽️🚀
