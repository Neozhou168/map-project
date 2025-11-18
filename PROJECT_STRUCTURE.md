# 📁 Project Structure

```
venue-geocoder/
├── app.py                      # Main Flask application (handles routes, file upload)
├── utils.py                    # Core logic (geocoding, Excel/KML processing)
├── templates/
│   ├── index.html             # Upload page with drag-and-drop UI
│   └── result.html            # Download page with file links
├── requirements.txt           # Python dependencies
├── Procfile                   # Railway/Heroku deployment config
├── runtime.txt                # Python version specification
├── .env.example               # Template for environment variables
├── .gitignore                 # Git ignore rules
├── README.md                  # Full documentation
├── QUICKSTART.md             # Quick deployment guide
└── create_test_file.py       # Generate sample Excel for testing

```

## File Descriptions

### Core Application Files

**app.py** (Main Application)
- Flask web server setup
- Route handlers for:
  - `/` - Home page with upload form
  - `/process` - File processing endpoint
  - `/download/<path>` - File download handler
- File upload validation
- Temporary file management

**utils.py** (Processing Logic)
- `geocode_google()` - Google Geocoding API integration
- `geocode_amap()` - Amap API integration (fallback)
- `build_google_urls()` - Generate Maps URLs
- `detect_columns()` - Auto-detect Excel column names
- `process_venue_file()` - Main processing pipeline

### Templates

**templates/index.html**
- Modern, responsive upload interface
- Drag-and-drop file upload
- File validation
- Instructions and info box

**templates/result.html**
- Download links for generated files
- Usage instructions for KML
- "Process another file" button

### Configuration Files

**requirements.txt**
- Flask 3.0.0 - Web framework
- pandas 2.1.4 - Excel/data processing
- openpyxl 3.1.2 - Excel file manipulation
- requests 2.31.0 - HTTP requests for APIs
- Werkzeug 3.0.1 - WSGI utilities
- gunicorn 21.2.0 - Production server

**Procfile**
```
web: gunicorn app:app
```
Tells Railway/Heroku to run the app with Gunicorn

**runtime.txt**
```
python-3.11.6
```
Specifies Python version for deployment

**.env.example**
Template for environment variables:
- GOOGLE_API_KEY
- AMAP_API_KEY
- SECRET_KEY
- PORT

### Documentation

**README.md**
- Complete project documentation
- API key setup instructions
- Deployment guides
- Excel format requirements
- Troubleshooting tips

**QUICKSTART.md**
- 5-minute deployment guide
- Minimal steps to get started
- Essential configuration only

### Utilities

**create_test_file.py**
Quick script to generate a sample Excel file for testing

**.gitignore**
Prevents committing:
- .env files
- Python cache
- Virtual environments
- Temporary/output files

## Data Flow

```
1. User uploads Excel file
   ↓
2. app.py receives file → saves to temp directory
   ↓
3. utils.py processes file:
   - Reads Excel with pandas
   - Auto-detects columns
   - Geocodes each venue (Google → Amap fallback)
   - Generates URLs
   - Creates enhanced Excel
   - Generates KML file
   ↓
4. result.html displays download links
   ↓
5. User downloads both files
   ↓
6. Temp directory cleaned up
```

## Environment Variables Flow

```
Development (Local):
.env file → app.py → utils.py

Production (Railway):
Railway Variables → Environment → app.py → utils.py
```

## API Integration

```
Venue Name
    ↓
Google Geocoding API
    ↓ (if fails)
Amap API (fallback)
    ↓
Coordinates (lat, lng)
    ↓
Google Maps URLs + KML
```

## Key Features in Code

### Auto Column Detection (utils.py)
Recognizes various column names:
- Chinese: 城市, 景点, 地点, 店, 市
- English: city, place, name
- Falls back to first two columns

### Geocoding Strategy (utils.py)
1. Try Google Geocoding (more global coverage)
2. Fall back to Amap (better for China)
3. Skip venue if both fail
4. Continue processing remaining venues

### Error Handling (app.py)
- File size limits (16MB)
- File type validation
- Graceful error messages
- Temporary file cleanup

### User Experience (templates/)
- Drag-and-drop upload
- Real-time file info display
- Loading indicators
- Clear download instructions

## Deployment Ready

✅ **Railway**: Procfile + requirements.txt
✅ **Heroku**: Same configuration works
✅ **Docker**: Can add Dockerfile if needed
✅ **VPS**: Can run with gunicorn directly

## Security Considerations

🔒 **API Keys**: Stored in environment variables
🔒 **File Upload**: Size limits + type validation
🔒 **Temp Files**: Automatically cleaned up
🔒 **Secret Key**: Required for session security

## Next Steps for Customization

Want to extend the app? Here are some ideas:

1. **Add more geocoding services**:
   - Edit `utils.py` → add new `geocode_xxx()` function

2. **Change UI theme**:
   - Edit `templates/index.html` and `result.html` CSS

3. **Add authentication**:
   - Add Flask-Login to `requirements.txt`
   - Create user management routes in `app.py`

4. **Add database for history**:
   - Add SQLAlchemy to `requirements.txt`
   - Create models and store processing history

5. **Add progress tracking**:
   - Implement WebSocket or Server-Sent Events
   - Show real-time progress during geocoding

## Testing Checklist

Before deploying:
- [ ] Set all environment variables
- [ ] Test with sample Excel file
- [ ] Verify both files download correctly
- [ ] Test KML import in Google Maps
- [ ] Check Excel URLs work
- [ ] Test error handling (wrong file type, etc.)

---

**Ready to deploy?** Follow the QUICKSTART.md guide!
