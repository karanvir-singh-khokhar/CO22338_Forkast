# 🍽️ Restaurant Review Analyzer - Deployment Guide

## Quick Deploy to Streamlit Cloud (Recommended)

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
   - Name: `restaurant-review-analyzer`
   - Make it Public
   - Don't initialize with README (we already have one)

### Step 2: Push Code to GitHub

Open terminal in your project folder and run:

```bash
git init
git add .
git commit -m "Initial commit - Restaurant Review Analyzer"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/restaurant-review-analyzer.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `restaurant-review-analyzer`
5. Branch: `main`
6. Main file path: `app/streamlit_app.py`
7. Click "Deploy!"

**⏱️ Deployment takes 3-5 minutes**

### Step 4: Your App is Live! 🎉

You'll get a URL like: `https://your-app-name.streamlit.app`

---

## Alternative: Deploy to Heroku

### Requirements:
- Heroku account
- Heroku CLI installed

### Create Procfile:
```
web: sh setup.sh && streamlit run app/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

### Deploy Commands:
```bash
heroku login
heroku create restaurant-review-nlp
git push heroku main
heroku open
```

---

## Alternative: Run Locally with Public URL

### Using Ngrok:

1. Install ngrok: https://ngrok.com/download
2. Run your app: `streamlit run app/streamlit_app.py`
3. In another terminal: `ngrok http 8501`
4. Share the ngrok URL

---

## Environment Setup

The app will automatically:
- Install Python packages from `requirements.txt`
- Download spaCy model via `setup.sh`
- Configure Streamlit settings from `.streamlit/config.toml`

## Troubleshooting

### If spaCy model fails to download:
Add to `packages.txt`:
```
python3-dev
build-essential
```

### If deployment is slow:
- Remove unused packages from requirements.txt
- Use lighter spaCy model: `en_core_web_sm`

### Memory issues:
- Streamlit Cloud has 1GB RAM limit
- Our app uses ~200-300MB (safe)

---

## Your Deployed App Features

✅ Real-time restaurant review analysis
✅ Sentiment detection
✅ Aspect-based analysis (Food, Service, Ambiance, Price)
✅ 14+ cuisine classification
✅ Named entity recognition
✅ Beautiful dark theme UI

**Share your deployed URL with anyone!** 🚀
