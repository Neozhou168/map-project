# 🍎 macOS Local Testing Guide

## Quick Fix for Your Current Issue

Your pandas installation is failing. Try these solutions in order:

### Solution 1: Install without pandas first (Quickest)

```bash
# Install everything except pandas
pip3 install Flask openpyxl requests Werkzeug

# Install pandas separately (it will get the right pre-built version)
pip3 install pandas

# Verify installation
pip3 list | grep -E "Flask|pandas|openpyxl|requests"
```

### Solution 2: Use Python 3.11+ (Recommended)

Pandas works best with Python 3.11+. Check your version:

```bash
python3 --version
```

If it's older than 3.11, install newer Python:

```bash
# Using Homebrew
brew install python@3.11

# Then use python3.11 instead
python3.11 -m pip install Flask pandas openpyxl requests Werkzeug
python3.11 app.py
```

### Solution 3: Use Virtual Environment (Best Practice)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip inside venv
pip install --upgrade pip

# Install packages
pip install Flask pandas openpyxl requests Werkzeug

# Run app
python app.py  # Note: just 'python', not 'python3' when venv is active
```

## 🚀 Complete Setup Steps

### 1. Navigate to your project folder

```bash
cd ~/Desktop/hoho_developing/map-project
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install Flask pandas openpyxl requests Werkzeug
```

### 4. Load environment variables

Make sure your `.env` file exists with:

```bash
GOOGLE_API_KEY=AIzaSyA5m-jHPOpAV15gyawicBXCxY-atCSb1LI
AMAP_API_KEY=bfd68c3ee5c1688531a9206671eaf311
SECRET_KEY=d5fd30f20804e7a876ed6991011ac1a45a9eb1b69972138f7eb531ee973a287a
PORT=5000
```

### 5. Install python-dotenv (to load .env file)

```bash
pip install python-dotenv
```

### 6. Update app.py to load .env

Add this at the very top of `app.py`:

```python
from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, request, render_template, send_file, flash
# ... rest of the imports
```

### 7. Run the app

```bash
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

### 8. Test in browser

Open: http://localhost:5000

## 🧪 Generate Test File

```bash
python create_test_file.py
```

This creates `test_venues.xlsx` that you can upload.

## 🛑 Stop the Server

Press `CTRL + C` in the terminal.

## 🔄 Deactivate Virtual Environment

When done testing:

```bash
deactivate
```

## 🐛 Common Issues on macOS

### Issue: "pip: command not found"
**Solution:** Use `pip3` instead of `pip`

### Issue: "python: command not found"
**Solution:** Use `python3` instead of `python`

### Issue: Pandas compilation errors
**Solution:** 
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Or use pre-built pandas
pip3 install --only-binary :all: pandas
```

### Issue: Port 5000 already in use (AirPlay on macOS)
**Solution:** Change PORT in `.env` to 5001:
```bash
PORT=5001
```

Then visit: http://localhost:5001

Or disable AirPlay Receiver:
System Settings → General → AirDrop & Handoff → Turn off "AirPlay Receiver"

### Issue: ModuleNotFoundError
**Solution:** Make sure venv is activated:
```bash
source venv/bin/activate
```

### Issue: Permission denied
**Solution:** Don't use `sudo` with pip. Use virtual environment instead.

## ✅ Verification Checklist

Before testing, verify:

- [ ] Virtual environment is activated `(venv)` in prompt
- [ ] All packages installed: `pip list`
- [ ] `.env` file exists with API keys
- [ ] `python-dotenv` is installed
- [ ] App starts without errors
- [ ] Port 5000 (or 5001) is accessible

## 📁 Your Project Structure Should Be:

```
map-project/
├── venv/                  ← Virtual environment (created)
├── .env                   ← Environment variables (you create)
├── .env.example          ← Template
├── app.py
├── utils.py
├── static/
│   └── images/
│       └── logo.jpg
├── templates/
│   ├── index.html
│   └── result.html
├── requirements.txt
└── ... (other files)
```

## 🎯 Quick Test Command

One-liner to test everything:

```bash
cd ~/Desktop/hoho_developing/map-project && \
source venv/bin/activate && \
python app.py
```

## 🚀 After Local Testing Works

Once local testing is successful, you're ready to:
1. Commit to GitHub
2. Deploy to Railway
3. Add environment variables in Railway dashboard

---

**Need help?** Check the error message and match it with the common issues above!