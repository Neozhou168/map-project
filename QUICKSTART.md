# 🚀 Quick Start Guide

## Immediate Deployment to Railway (5 minutes)

### 1. Get Your API Keys First

Before deploying, you need:

**Google Maps API Key** (Required):
- Go to: https://console.cloud.google.com/
- Create project → Enable "Geocoding API" → Create API Key
- Copy the key

**Amap API Key** (Optional, for Chinese locations):
- Go to: https://console.amap.com/
- Register → Create Web Service app → Copy key

### 2. Deploy to Railway

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Go to https://railway.app/
   - Login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Wait for deployment (automatic)

3. **Add Environment Variables**:
   In Railway dashboard, go to Variables tab and add:
   ```
   GOOGLE_API_KEY=your_key_here
   AMAP_API_KEY=your_key_here (optional)
   SECRET_KEY=random_secret_string_here
   ```

4. **Done!** 🎉
   Your app is live at: `https://your-app.up.railway.app`

### 3. Test Locally First (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the app
python app.py

# Visit http://localhost:5000
```

## Usage

1. Upload an Excel file with columns like:
   - 城市 (city) and 景点 (place), or
   - City and Place Name

2. Click "Generate Files"

3. Download:
   - Enhanced Excel with Google Maps URLs
   - KML file for Google Maps/Earth

## File Requirements

✅ Excel format (.xlsx or .xls)
✅ Contains city and place/venue columns
✅ Maximum 16MB file size

## Need Help?

Check the full README.md for:
- Detailed API setup
- Excel format examples
- Troubleshooting guide
- KML file usage instructions

---

**Pro Tips**:
- Test with a small file first (5-10 venues)
- Google Geocoding has 40,000 free requests/month
- Use Amap for better results with Chinese locations
- The app auto-detects column names in Chinese and English
