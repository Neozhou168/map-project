#!/usr/bin/env python3
"""
Quick test script to verify Amap API connection
Run this to check if your Amap API key is working
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
AMAP_API_KEY = os.environ.get('AMAP_API_KEY', '')

print("=" * 60)
print("AMAP API CONNECTION TEST")
print("=" * 60)

# Check if API key exists
if not AMAP_API_KEY:
    print("❌ ERROR: AMAP_API_KEY not found in .env file!")
    print("\nPlease add to your .env file:")
    print("AMAP_API_KEY=your_key_here")
    exit(1)

print(f"✅ API Key found: {AMAP_API_KEY[:10]}...{AMAP_API_KEY[-4:]}")
print()

# Test with a famous location that should definitely exist
test_queries = [
    "南京 先锋书店",
    "南京南站",
    "南京市",
]

url = "https://restapi.amap.com/v3/place/text"

for query in test_queries:
    print(f"\nTesting: '{query}'")
    print("-" * 40)
    
    params = {
        "keywords": query,
        "key": AMAP_API_KEY,
        "output": "json",
        "city": "",
    }
    
    try:
        r = requests.get(url, params=params, timeout=10)
        r.encoding = 'utf-8'
        
        print(f"HTTP Status: {r.status_code}")
        
        if r.status_code != 200:
            print(f"❌ HTTP Error: {r.status_code}")
            continue
        
        data = r.json()
        
        status = data.get("status", "unknown")
        info = data.get("info", "unknown")
        count = data.get("count", "0")
        
        print(f"Amap Status: {status}")
        print(f"Amap Info: {info}")
        print(f"Results Count: {count}")
        
        if status == "1" and int(count) > 0:
            print("✅ SUCCESS! Amap found results")
            poi = data["pois"][0]
            print(f"   Name: {poi.get('name', 'N/A')}")
            print(f"   Address: {poi.get('address', 'N/A')}")
            print(f"   Location: {poi.get('location', 'N/A')}")
        elif status == "1" and int(count) == 0:
            print("⚠️  API works, but no results found for this query")
        else:
            print(f"❌ ERROR: {info}")
            if "INVALID_USER_KEY" in info:
                print("   → Your API key is invalid!")
            elif "DAILY_QUERY_OVER_LIMIT" in info:
                print("   → You've exceeded your daily quota!")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)

print("\nInterpretation:")
print("✅ If you see 'SUCCESS' → Your Amap API is working!")
print("⚠️  If you see 'API works, but no results' → Venues not in database")
print("❌ If you see 'INVALID_USER_KEY' → Check your API key")
print("❌ If you see 'DAILY_QUERY_OVER_LIMIT' → Wait until tomorrow")