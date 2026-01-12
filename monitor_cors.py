#!/usr/bin/env python3
"""Monitor Render API for CORS headers and version"""
import requests
import time
from datetime import datetime

BASE_URL = "https://bamaco-calc-api.onrender.com"
CHECK_INTERVAL = 10  # seconds

print("🔍 Monitoring Render API deployment...")
print(f"URL: {BASE_URL}")
print(f"Checking every {CHECK_INTERVAL} seconds")
print(f"Waiting for version 1.1.0 with CORS enabled")
print(f"Press Ctrl+C to stop\n")

attempt = 0
while True:
    attempt += 1
    timestamp = datetime.now().strftime("%H:%M:%S")

    try:
        # Check health endpoint
        r = requests.get(f"{BASE_URL}/health",
                        headers={'Origin': 'http://localhost:8081'},
                        timeout=10)

        cors_header = r.headers.get('access-control-allow-origin')
        response_data = r.json()
        version = response_data.get('version', 'unknown')
        cors_in_response = response_data.get('cors_enabled', 'false')

        print(f"[{timestamp}] Attempt #{attempt}:")
        print(f"  Version: {version}")
        print(f"  CORS Header: {cors_header if cors_header else 'NOT FOUND'}")
        print(f"  Response says CORS: {cors_in_response}")

        if cors_header and version == "1.1.0":
            print(f"\n{'='*60}")
            print(f"✅ SUCCESS! CORS is now live!")
            print(f"{'='*60}")
            print(f"CORS Header: {cors_header}")
            print(f"Version: {version}")
            print(f"\n🎉 The API demo page should now work!")
            print(f"Refresh: http://localhost:8081/api_demo.html")
            break
        elif version == "1.1.0" and not cors_header:
            print(f"  ⚠️  New version deployed but CORS header still missing!")
        else:
            print(f"  ⏳ Old version still running, waiting for redeploy...")

    except requests.exceptions.Timeout:
        print(f"[{timestamp}] Attempt #{attempt}: Timeout (API may be waking up)")
    except Exception as e:
        print(f"[{timestamp}] Attempt #{attempt}: Error - {str(e)[:50]}")

    print()
