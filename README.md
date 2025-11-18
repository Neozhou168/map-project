# Venue Geocoder & Map Generator

A web application that converts Excel files containing venue information into KML map files and enhanced Excel files with Google Maps URLs.

## Features

- 🗺️ **Automatic Geocoding**: Converts venue names to coordinates using Google Geocoding API
- 📍 **Fallback Support**: Uses Amap API as fallback for Chinese locations
- 📊 **Enhanced Excel**: Adds latitude, longitude, Google Direct URLs, and Embed URLs
- 🗺️ **KML Generation**: Creates KML files for Google Maps/Google Earth visualization
- 🎨 **Modern UI**: Clean, responsive interface with drag-and-drop upload
- ☁️ **Cloud Ready**: Easily deployable to Railway, Heroku, or other platforms

## Prerequisites

- Python 3.9 or higher
- Google Maps API Key (with Geocoding API enabled)
- Amap API Key (optional, for Chinese location fallback)

## Getting API Keys

### Google Maps API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Geocoding API
   - Maps Embed API (if you want embed URLs)
4. Create credentials → API Key
5. (Optional) Restrict the API key to specific APIs for security

### Amap API Key (Optional)
1. Go to [Amap Developer Console](https://console.amap.com/)
2. Register and create an application
3. Select "Web服务" (Web Service) type
4. Copy the API key

## Local Development

1. **Clone or download the project**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   
   Create a `.env` file (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   AMAP_API_KEY=your_amap_api_key_here
   SECRET_KEY=your_random_secret_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```
   
   The app will be available at `http://localhost:5000`

## Deploying to Railway

Railway is a modern platform that makes deployment easy and free for small projects.

### Step 1: Prepare Your Repository

1. Initialize git repository (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Push to GitHub:
   ```bash
   git remote add origin your-github-repo-url
   git push -u origin main
   ```

### Step 2: Deploy on Railway

1. Go to [Railway.app](https://railway.app/)
2. Sign up/Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect the Python app and deploy it

### Step 3: Set Environment Variables

1. In your Railway project, go to **Variables** tab
2. Add the following variables:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   AMAP_API_KEY=your_amap_api_key_here
   SECRET_KEY=your_random_secret_key_here
   ```

3. Railway automatically sets the `PORT` variable

### Step 4: Deploy

Railway will automatically deploy your app. You'll get a public URL like:
`https://your-app-name.up.railway.app`

## Excel File Format

Your Excel file should contain at least two columns:

### Supported Column Names

**City Column** (one of):
- 城市 / city / City / 市

**Place/Venue Column** (one of):
- 景点 / 地点 / 场所 / 店 / name / Name

### Example

| 城市 | 景点 |
|------|------|
| 南京 | 先锋书店 |
| 上海 | 外滩 |
| 北京 | 故宫 |

Or:

| City | Place Name |
|------|------------|
| New York | Central Park |
| Paris | Eiffel Tower |
| Tokyo | Tokyo Tower |

## Output Files

### Enhanced Excel File
The output Excel file contains all original columns plus:
- `lat`: Latitude coordinate
- `lng`: Longitude coordinate
- `google_direct_url`: Direct link to open in Google Maps
- `google_embed_url`: Embed URL for iframe integration

### KML File
The KML file contains all successfully geocoded venues and can be:
- Imported into Google Maps (My Maps)
- Opened in Google Earth
- Used in other GIS applications

## How to Use KML Files

### Import to Google Maps:
1. Open [Google My Maps](https://www.google.com/mymaps)
2. Create a new map or open existing one
3. Click "Import" layer
4. Upload the KML file
5. All venues will appear as markers on the map

### Open in Google Earth:
1. Open Google Earth
2. File → Open
3. Select the KML file
4. Venues will be displayed with their names

## Troubleshooting

### No coordinates found
- Check that your Google API key is valid and has Geocoding API enabled
- Ensure the venue names are specific enough (include city name)
- Check your API quota hasn't been exceeded

### Deployment issues
- Verify all environment variables are set in Railway
- Check Railway logs for error messages
- Ensure requirements.txt includes all dependencies

### File upload fails
- Check file size (maximum 16MB)
- Ensure file is in .xlsx or .xls format
- Verify the file contains the expected columns

## File Structure

```
.
├── app.py                 # Main Flask application
├── utils.py              # Geocoding and processing logic
├── templates/
│   ├── index.html        # Upload page
│   └── result.html       # Download page
├── requirements.txt      # Python dependencies
├── Procfile             # Railway/Heroku configuration
├── .env.example         # Environment variables template
└── README.md           # This file
```

## API Rate Limits

### Google Geocoding API
- Free tier: $200 credit per month
- ~40,000 free requests per month
- After that: $5 per 1,000 requests

### Amap API
- Free tier: 300,000 requests per day
- Sufficient for most use cases

## Security Notes

- Never commit your `.env` file with real API keys
- Use environment variables for all sensitive data
- Consider restricting API keys to specific domains/IPs in production
- Regularly rotate your SECRET_KEY

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Railway deployment logs
3. Verify API keys are correctly set
4. Ensure Excel file format matches requirements

## Future Enhancements

Potential features to add:
- Batch processing of multiple files
- Custom map styling options
- Export to other formats (GeoJSON, CSV)
- Address validation before geocoding
- Caching to reduce API calls
- Progress bar for large files
- Map preview before download
