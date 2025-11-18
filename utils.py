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

def get_amap_address(keywords: str):
    """Use Amap Place Search API to get address and coordinates in Chinese"""
    if not AMAP_API_KEY:
        return None
    
    url = "https://restapi.amap.com/v3/place/text"
    # Ensure we get Chinese results by setting output format and encoding
    params = {
        "keywords": keywords,
        "key": AMAP_API_KEY,
        "output": "json",  # JSON output format
        "city": "",  # Search across all cities (or could be specific city code)
    }
    
    try:
        # Ensure proper encoding for Chinese characters
        r = requests.get(url, params=params, timeout=10)
        r.encoding = 'utf-8'  # Ensure UTF-8 encoding for Chinese
        data = r.json()
        
        if data.get("status") == "1" and data.get("pois"):
            poi = data["pois"][0]
            
            # Extract Chinese address components
            name = poi.get("name", "")  # Venue name in Chinese
            address = poi.get("address", "")  # Street address in Chinese
            pname = poi.get("pname", "")  # Province name in Chinese
            cityname = poi.get("cityname", "")  # City name in Chinese
            adname = poi.get("adname", "")  # District name in Chinese
            
            # Build full Chinese address
            # Format: Name, Province City District Address
            address_parts = []
            if name:
                address_parts.append(name)
            
            # Build location string: Province + City + District + Street
            location_parts = []
            if pname:
                location_parts.append(pname)
            if cityname and cityname != pname:  # Avoid duplication
                location_parts.append(cityname)
            if adname:
                location_parts.append(adname)
            if address:
                location_parts.append(address)
            
            location_str = "".join(location_parts)
            if location_str:
                address_parts.append(location_str)
            
            full_address = ", ".join(address_parts) if len(address_parts) > 1 else "".join(address_parts)
            
            # Get coordinates
            loc_str = poi.get("location")
            if loc_str and full_address:
                lng_str, lat_str = loc_str.split(",")
                
                print(f"  Amap returned Chinese address: {full_address}")
                
                return {
                    'address': full_address,
                    'lat': float(lat_str),
                    'lng': float(lng_str)
                }
    except Exception as e:
        print(f"Amap search error: {e}")
    
    return None

def build_google_urls(lat, lng):
    """Generate Direct URL and Embed URL for Google Maps using coordinates"""
    query = f"{lat},{lng}"
    encoded = quote(query, safe="")
    direct = f"https://www.google.com/maps/search/?api=1&query={encoded}"
    
    if GOOGLE_API_KEY:
        embed = f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_API_KEY}&q={encoded}"
    else:
        embed = ""
    
    return direct, embed

def build_google_urls_from_address(address: str):
    """Generate Direct URL and Embed URL for Google Maps using address"""
    encoded = quote(address, safe="")
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
        address_list, direct_urls, embed_urls = [], [], []
        coords_for_kml = []  # Store (lat, lng, name) tuples for KML
        
        # Process each row
        for idx, row in df.iterrows():
            city = str(row[city_col]).strip()
            place = str(row[place_col]).strip()
            full_name = f"{city} {place}"
            
            print(f"Processing: {full_name}")
            
            # Try Google geocoding first with venue name
            coord = geocode_google(full_name)
            address = ""
            
            if coord is not None:
                # Google found it directly
                print(f"  Found on Google: {coord}")
                lat, lng = coord
                direct, embed = build_google_urls(lat, lng)
                coords_for_kml.append((lat, lng, full_name))
            else:
                # Google failed, try Amap
                print(f"  Google failed, trying Amap...")
                amap_result = get_amap_address(full_name)
                
                if amap_result:
                    # Amap found it - use the ADDRESS for Google Maps URLs
                    address = amap_result['address']
                    lat = amap_result['lat']
                    lng = amap_result['lng']
                    
                    print(f"  Found on Amap: {address}")
                    print(f"  Coordinates: {lat}, {lng}")
                    
                    # Build Google Maps URLs using ADDRESS (not coordinates)
                    direct, embed = build_google_urls_from_address(address)
                    coords_for_kml.append((lat, lng, full_name))
                else:
                    # Both failed
                    print(f"  Could not find: {full_name}")
                    direct, embed = "", ""
            
            address_list.append(address)
            direct_urls.append(direct)
            embed_urls.append(embed)
        
        # Add new columns to dataframe (no lat/lng, just address)
        df["address"] = address_list
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
        
        # Generate KML content (only for venues with coordinates)
        placemarks = []
        for lat, lng, name in coords_for_kml:
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