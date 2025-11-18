import os
import requests
import pandas as pd
from urllib.parse import quote

# ====== API Keys - Should be set as environment variables ======
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')
AMAP_API_KEY = os.environ.get('AMAP_API_KEY', '')

def geocode_google(address: str):
    """Use Google Geocoding API to get coordinates and quality info"""
    if not GOOGLE_API_KEY:
        return None
    
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": GOOGLE_API_KEY}
    
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get("status") == "OK" and data.get("results"):
            result = data["results"][0]
            loc = result["geometry"]["location"]
            location_type = result["geometry"].get("location_type", "UNKNOWN")
            formatted_address = result.get("formatted_address", "")
            place_id = result.get("place_id", "")
            
            return {
                'lat': loc["lat"],
                'lng': loc["lng"],
                'location_type': location_type,
                'formatted_address': formatted_address,
                'place_id': place_id
            }
    except Exception as e:
        print(f"Google geocoding error: {e}")
    
    return None

def get_amap_address(keywords: str):
    """Use Amap Place Search API to get Chinese address (coordinates will be obtained from Google)"""
    if not AMAP_API_KEY:
        print(f"  Amap API key not found!")
        return None
    
    url = "https://restapi.amap.com/v3/place/text"
    params = {
        "keywords": keywords,
        "key": AMAP_API_KEY,
        "output": "json",
        "city": "",
    }
    
    try:
        r = requests.get(url, params=params, timeout=10)
        r.encoding = 'utf-8'
        data = r.json()
        
        # Debug: print Amap response status
        status = data.get("status", "unknown")
        info = data.get("info", "unknown")
        count = data.get("count", 0)
        print(f"  Amap API response: status={status}, info={info}, count={count}")
        
        if data.get("status") == "1" and data.get("pois") and len(data.get("pois", [])) > 0:
            poi = data["pois"][0]
            
            name = poi.get("name", "")
            address = poi.get("address", "")
            pname = poi.get("pname", "")
            cityname = poi.get("cityname", "")
            adname = poi.get("adname", "")
            
            address_parts = []
            if name:
                address_parts.append(name)
            
            location_parts = []
            if pname:
                location_parts.append(pname)
            if cityname and cityname != pname:
                location_parts.append(cityname)
            if adname:
                location_parts.append(adname)
            if address:
                location_parts.append(address)
            
            location_str = "".join(location_parts)
            if location_str:
                address_parts.append(location_str)
            
            full_address = ", ".join(address_parts) if len(address_parts) > 1 else "".join(address_parts)
            
            loc_str = poi.get("location")
            if loc_str and full_address:
                lng_str, lat_str = loc_str.split(",")
                
                print(f"  Amap returned Chinese address: {full_address}")
                
                return {
                    'address': full_address,
                    'lat': float(lat_str),
                    'lng': float(lng_str)
                }
            else:
                print(f"  Amap: No location or address in result")
        else:
            print(f"  Amap: No results found for '{keywords}'")
    except Exception as e:
        print(f"  Amap search error: {e}")
    
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
        df = pd.read_excel(input_path)
        city_col, place_col = detect_columns(df)
        
        address_list, direct_urls, embed_urls = [], [], []
        coords_for_kml = []
        
        for idx, row in df.iterrows():
            city = str(row[city_col]).strip()
            place = str(row[place_col]).strip()
            full_name = f"{city} {place}"
            
            print(f"Processing: {full_name}")
            
            google_result = geocode_google(full_name)
            address = ""
            
            if google_result is not None:
                location_type = google_result['location_type']
                formatted_address = google_result['formatted_address']
                
                # Only fallback to Amap if Google's result is APPROXIMATE
                if location_type == "APPROXIMATE":
                    print(f"  Google result is APPROXIMATE: {formatted_address}")
                    print(f"  Trying Amap for more specific location...")
                    
                    amap_result = get_amap_address(full_name)
                    
                    if amap_result:
                        address = amap_result['address']
                        
                        print(f"  Found on Amap: {address}")
                        
                        # Geocode the Chinese address through Google to get Google coordinates
                        print(f"  Geocoding Chinese address through Google...")
                        google_from_chinese = geocode_google(address)
                        
                        if google_from_chinese:
                            lat = google_from_chinese['lat']
                            lng = google_from_chinese['lng']
                            print(f"  Google coordinates from Chinese address: {lat}, {lng}")
                            coords_for_kml.append((lat, lng, full_name))
                        else:
                            print(f"  Google could not geocode Chinese address")
                        
                        # Use the Chinese address for Google Maps URLs
                        direct, embed = build_google_urls_from_address(address)
                    else:
                        # Amap also failed - skip this venue entirely
                        print(f"  Amap also failed, skipping this venue (no KML, no URLs)")
                        direct, embed = "", ""
                        # Don't add to coords_for_kml
                else:
                    # Google found it with good precision (ROOFTOP, RANGE_INTERPOLATED, GEOMETRIC_CENTER)
                    print(f"  Found on Google with {location_type} precision")
                    print(f"  Address: {formatted_address}")
                    lat = google_result['lat']
                    lng = google_result['lng']
                    address = formatted_address
                    direct, embed = build_google_urls_from_address(formatted_address)
                    coords_for_kml.append((lat, lng, full_name))
            else:
                print(f"  Google failed, trying Amap...")
                amap_result = get_amap_address(full_name)
                
                if amap_result:
                    address = amap_result['address']
                    
                    print(f"  Found on Amap: {address}")
                    
                    # Geocode the Chinese address through Google to get Google coordinates
                    print(f"  Geocoding Chinese address through Google...")
                    google_from_chinese = geocode_google(address)
                    
                    if google_from_chinese:
                        lat = google_from_chinese['lat']
                        lng = google_from_chinese['lng']
                        print(f"  Google coordinates from Chinese address: {lat}, {lng}")
                        coords_for_kml.append((lat, lng, full_name))
                    else:
                        print(f"  Google could not geocode Chinese address")
                    
                    # Use the Chinese address for Google Maps URLs
                    direct, embed = build_google_urls_from_address(address)
                else:
                    print(f"  Could not find: {full_name}")
                    direct, embed = "", ""
            
            address_list.append(address)
            direct_urls.append(direct)
            embed_urls.append(embed)
        
        # ============================================================
        # WORKFLOW REQUIREMENT: Output must have ONLY these 5 columns
        # in this exact order:
        # 1. city
        # 2. venue
        # 3. address
        # 4. google_maps_direct_url
        # 5. google_maps_embed_url
        # ============================================================
        output_df = pd.DataFrame({
            'city': df[city_col],
            'venue': df[place_col],
            'address': address_list,
            'google_maps_direct_url': direct_urls,
            'google_maps_embed_url': embed_urls
        })
        
        base_name = os.path.basename(input_path).replace(".xlsx", "").replace(".xls", "")
        excel_filename = f"{base_name}_output.xlsx"
        kml_filename = f"{base_name}.kml"
        
        excel_path = os.path.join(output_dir, excel_filename)
        kml_path = os.path.join(output_dir, kml_filename)
        
        output_df.to_excel(excel_path, index=False)
        print(f"Generated: {excel_path}")
        
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