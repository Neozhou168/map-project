import os
import requests
import pandas as pd
from urllib.parse import quote
from openpyxl import load_workbook

# ====== API Keys - Should be set as environment variables ======
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')
AMAP_API_KEY = os.environ.get('AMAP_API_KEY', '')

def geocode_google(address: str):
    """Use Google Geocoding API to get coordinates"""
    if not GOOGLE_API_KEY:
        return None
    
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": GOOGLE_API_KEY}
    
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get("status") == "OK" and data.get("results"):
            loc = data["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]
    except Exception as e:
        print(f"Google geocoding error: {e}")
    
    return None

def geocode_amap(keywords: str):
    """Use Amap Place Search API to get coordinates"""
    if not AMAP_API_KEY:
        return None
    
    url = "https://restapi.amap.com/v3/place/text"
    params = {"keywords": keywords, "key": AMAP_API_KEY}
    
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get("status") == "1" and data.get("pois"):
            loc_str = data["pois"][0].get("location")
            if loc_str:
                lng_str, lat_str = loc_str.split(",")
                return float(lat_str), float(lng_str)
    except Exception as e:
        print(f"Amap geocoding error: {e}")
    
    return None

def build_google_urls(lat, lng):
    """Generate Direct URL and Embed URL for Google Maps"""
    query = f"{lat},{lng}"
    encoded = quote(query, safe="")
    direct = f"https://www.google.com/maps/search/?api=1&query={encoded}"
    
    if GOOGLE_API_KEY:
        embed = f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_API_KEY}&q={encoded}"
    else:
        embed = ""
    
    return direct, embed

def detect_columns(df: pd.DataFrame):
    """Automatically detect city and place column names"""
    city_col = None
    place_col = None
    
    for col in df.columns:
        col_lower = str(col).lower()
        if city_col is None and ("城" in col or "city" in col_lower or "市" in col):
            city_col = col
        if place_col is None and ("景" in col or "点" in col or "店" in col or "name" in col_lower or "地点" in col or "场所" in col):
            place_col = col
    
    # If still not found, try to use first two columns
    if city_col is None and len(df.columns) >= 1:
        city_col = df.columns[0]
    if place_col is None and len(df.columns) >= 2:
        place_col = df.columns[1]
    
    if city_col is None or place_col is None:
        raise ValueError(f"Cannot detect city and place columns. Available columns: {list(df.columns)}")
    
    return city_col, place_col

def process_venue_file(input_path: str, output_dir: str):
    """
    Process an Excel file with venue data
    Returns a dictionary with success status and file paths
    """
    try:
        # Read Excel file
        df = pd.read_excel(input_path)
        
        # Detect columns
        city_col, place_col = detect_columns(df)
        
        # Initialize result lists
        lat_list, lng_list, direct_urls, embed_urls = [], [], [], []
        
        # Process each row
        for idx, row in df.iterrows():
            city = str(row[city_col]).strip()
            place = str(row[place_col]).strip()
            full_name = f"{city} {place}"
            
            print(f"Processing: {full_name}")
            
            # Try Google geocoding first
            coord = geocode_google(full_name)
            
            # Fall back to Amap if Google fails
            if coord is None and AMAP_API_KEY:
                print(f"  Google failed, trying Amap...")
                coord = geocode_amap(full_name)
            
            # Build URLs if coordinates found
            if coord is None:
                print(f"  Could not geocode: {full_name}")
                lat, lng, direct, embed = None, None, None, None
            else:
                lat, lng = coord
                direct, embed = build_google_urls(lat, lng)
                print(f"  Success: {lat}, {lng}")
            
            lat_list.append(lat)
            lng_list.append(lng)
            direct_urls.append(direct)
            embed_urls.append(embed)
        
        # Add new columns to dataframe
        df["lat"] = lat_list
        df["lng"] = lng_list
        df["google_direct_url"] = direct_urls
        df["google_embed_url"] = embed_urls
        
        # Generate output filename
        base_name = os.path.basename(input_path).replace(".xlsx", "").replace(".xls", "")
        excel_filename = f"{base_name}_output.xlsx"
        kml_filename = f"{base_name}.kml"
        
        excel_path = os.path.join(output_dir, excel_filename)
        kml_path = os.path.join(output_dir, kml_filename)
        
        # Save Excel file
        df.to_excel(excel_path, index=False)
        print(f"Generated: {excel_path}")
        
        # Generate KML content
        placemarks = []
        for idx, row in df.iterrows():
            lat = row["lat"]
            lng = row["lng"]
            if pd.isna(lat) or pd.isna(lng):
                continue
            
            name = f"{row[city_col]} {row[place_col]}"
            placemark = f"""
    <Placemark>
        <name>{name}</name>
        <Point>
            <coordinates>{lng},{lat},0</coordinates>
        </Point>
    </Placemark>"""
            placemarks.append(placemark)
        
        kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
{''.join(placemarks)}
</Document>
</kml>
"""
        
        # Save KML file
        with open(kml_path, "w", encoding="utf-8") as f:
            f.write(kml_content)
        print(f"Generated: {kml_path}")
        
        return {
            'success': True,
            'excel_path': excel_path,
            'kml_path': kml_path,
            'excel_filename': excel_filename,
            'kml_filename': kml_filename
        }
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return {
            'success': False,
            'error': str(e)
        }
