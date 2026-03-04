"""
Quick test script to verify API endpoints are working.
Run after: pip install -r requirements.txt && python manage.py migrate
"""
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost:8000/api/"

def test_api_endpoints():
    # Replace with your credentials
    auth = HTTPBasicAuth('admin', 'admin')
    
    endpoints = [
        'products/',
        'batches/',
        'equipment/',
        'serial-numbers/',
        'serial-number-pools/',
        'storage-locations/',
        'epcis-events/',
    ]
    
    print("Testing API Endpoints...")
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", auth=auth)
            status = "✓" if response.status_code == 200 else "✗"
            print(f"{status} {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"✗ {endpoint} - Error: {str(e)}")

if __name__ == "__main__":
    test_api_endpoints()
