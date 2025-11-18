# ✅ Deployment Checklist

Use this checklist to ensure smooth deployment of your Venue Geocoder application.

## Pre-Deployment Setup

### 1. Get API Keys
- [ ] **Google Maps API Key**
  - [ ] Create project in Google Cloud Console
  - [ ] Enable Geocoding API
  - [ ] Enable Maps Embed API (optional)
  - [ ] Create API Key
  - [ ] Save key securely

- [ ] **Amap API Key** (Optional but recommended for Chinese locations)
  - [ ] Register at Amap Developer Console
  - [ ] Create Web Service application
  - [ ] Save key securely

### 2. Prepare Code Repository
- [ ] Initialize git repository: `git init`
- [ ] Add all files: `git add .`
- [ ] Commit: `git commit -m "Initial commit"`
- [ ] Create GitHub repository
- [ ] Push code: `git push -u origin main`

### 3. Local Testing (Optional but Recommended)
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env`
- [ ] Add your API keys to `.env`
- [ ] Run app: `python app.py`
- [ ] Test at http://localhost:5000
- [ ] Upload test Excel file
- [ ] Verify downloads work
- [ ] Check KML in Google Maps

## Railway Deployment

### 1. Initial Setup
- [ ] Go to https://railway.app/
- [ ] Sign up/Login with GitHub
- [ ] Click "New Project"
- [ ] Select "Deploy from GitHub repo"
- [ ] Choose your repository
- [ ] Wait for automatic detection and deployment

### 2. Configure Environment Variables
Go to your project → Variables tab and add:

- [ ] `GOOGLE_API_KEY` = your_google_key
- [ ] `AMAP_API_KEY` = your_amap_key (optional)
- [ ] `SECRET_KEY` = random_string_at_least_32_chars

**Generate a secure SECRET_KEY**:
```python
import secrets
print(secrets.token_hex(32))
```

### 3. Verify Deployment
- [ ] Check deployment status (should show "Success")
- [ ] Copy the public URL (like `https://your-app.up.railway.app`)
- [ ] Visit the URL
- [ ] Verify page loads correctly

### 4. Test in Production
- [ ] Upload a small test Excel file (3-5 venues)
- [ ] Verify processing completes
- [ ] Download both files
- [ ] Check Excel URLs work
- [ ] Import KML to Google Maps
- [ ] Verify all venues appear on map

## Post-Deployment

### 1. Monitor and Optimize
- [ ] Check Railway logs for errors
- [ ] Monitor API usage in Google Cloud Console
- [ ] Set up billing alerts if using paid tier
- [ ] Monitor Railway usage metrics

### 2. Security Best Practices
- [ ] Never commit `.env` file to git
- [ ] Rotate SECRET_KEY periodically
- [ ] Restrict API keys to specific domains (optional)
- [ ] Set up API key usage quotas
- [ ] Review Railway security settings

### 3. Optional Enhancements
- [ ] Add custom domain in Railway
- [ ] Set up SSL certificate
- [ ] Configure Railway auto-scaling
- [ ] Add monitoring/alerting
- [ ] Set up backup strategy

## Troubleshooting Checklist

### If deployment fails:
- [ ] Check Railway logs for error messages
- [ ] Verify all files are in repository
- [ ] Ensure requirements.txt is correct
- [ ] Check Procfile syntax
- [ ] Verify Python version in runtime.txt

### If geocoding fails:
- [ ] Verify GOOGLE_API_KEY is set in Railway
- [ ] Check API is enabled in Google Cloud
- [ ] Verify API key has proper permissions
- [ ] Check Google Cloud Console for errors
- [ ] Verify you haven't exceeded quota

### If file upload fails:
- [ ] Check file size (< 16MB)
- [ ] Verify file is .xlsx or .xls format
- [ ] Check file has city and place columns
- [ ] Try with simpler/smaller file first

### If downloads don't work:
- [ ] Check Railway logs for errors
- [ ] Verify temp directory permissions
- [ ] Check file paths in code
- [ ] Test locally first

## Excel File Requirements

### Required Format
- [ ] File is .xlsx or .xls format
- [ ] Contains city column (城市, city, 市, etc.)
- [ ] Contains place column (景点, 地点, 店, name, etc.)
- [ ] Rows have valid data (no empty rows)
- [ ] File size under 16MB

### Sample Data Structure
```
| 城市 | 景点     |
|------|----------|
| 南京 | 先锋书店 |
| 上海 | 外滩     |
```
or
```
| City      | Place Name    |
|-----------|---------------|
| New York  | Central Park  |
| Paris     | Eiffel Tower  |
```

## API Quotas and Costs

### Google Geocoding API
- [ ] Free tier: $200 credit/month
- [ ] ~40,000 requests/month free
- [ ] Monitor usage in Google Cloud Console
- [ ] Set up billing alerts

### Amap API
- [ ] Free tier: 300,000 requests/day
- [ ] Usually sufficient for most needs
- [ ] Monitor in Amap console

### Railway
- [ ] Free tier: 500 hours/month
- [ ] $5/month for Starter plan
- [ ] Monitor usage in Railway dashboard

## Maintenance Checklist

### Weekly
- [ ] Check Railway logs for errors
- [ ] Monitor API usage
- [ ] Verify application is responsive

### Monthly
- [ ] Review API costs
- [ ] Check for dependency updates
- [ ] Review user feedback (if applicable)
- [ ] Backup environment configurations

### Quarterly
- [ ] Update dependencies: `pip list --outdated`
- [ ] Review security settings
- [ ] Test with new data sources
- [ ] Update documentation if needed

## Success Metrics

After deployment, verify:
- [ ] Application loads in < 3 seconds
- [ ] File upload works smoothly
- [ ] Geocoding success rate > 80%
- [ ] Both files download correctly
- [ ] KML imports to Google Maps successfully
- [ ] Excel URLs all work
- [ ] No errors in Railway logs
- [ ] API costs within budget

## Emergency Contacts

Keep these handy:
- Railway Support: https://help.railway.app/
- Google Cloud Support: https://cloud.google.com/support
- Your GitHub repository: _______________
- Railway project URL: _______________

## Next Steps After Deployment

1. **Share with users**
   - [ ] Send application URL
   - [ ] Provide sample Excel file
   - [ ] Share usage instructions

2. **Collect feedback**
   - [ ] Set up feedback mechanism
   - [ ] Monitor user issues
   - [ ] Track feature requests

3. **Plan improvements**
   - [ ] Review enhancement ideas
   - [ ] Prioritize features
   - [ ] Schedule updates

---

## Quick Reference Commands

### Local Development
```bash
# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run
python app.py

# Test
curl -F "file=@test_venues.xlsx" http://localhost:5000/process
```

### Git Commands
```bash
# Initial setup
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_REPO_URL
git push -u origin main

# Updates
git add .
git commit -m "Update message"
git push
```

### Generate Secret Key
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

**Ready to deploy?** Start from the top and check off each item! 🚀
