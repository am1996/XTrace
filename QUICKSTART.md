# XTrace API - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Start the Server
```bash
python manage.py runserver
```

### Step 2: Access the Browsable API
Open your browser and navigate to:
```
http://localhost:8000/api/
```

### Step 3: Login
Click "Log in" in the top right corner or go to:
```
http://localhost:8000/api-auth/login/
```

## 📋 Available Endpoints

Once logged in, you can access:

| Endpoint | Description |
|----------|-------------|
| `/api/products/` | Manage products with GTIN identifiers |
| `/api/batches/` | Manage production batches |
| `/api/equipment/` | Track manufacturing equipment |
| `/api/serial-numbers/` | Individual serial number tracking |
| `/api/serial-number-pools/` | Serial number pool management |
| `/api/storage-locations/` | Storage location with GLN |
| `/api/epcis-events/` | EPCIS 2.0 compliant events |

## 🔍 Try It Out

### Using the Browsable API (Easiest)
1. Go to http://localhost:8000/api/products/
2. Click the "GET" button to see all products
3. Scroll down to the form to create a new product
4. Fill in the fields and click "POST"

### Using cURL
```bash
# List all products
curl -u admin:password http://localhost:8000/api/products/

# Get a specific product
curl -u admin:password http://localhost:8000/api/products/1/

# Create a new product
curl -X POST http://localhost:8000/api/products/ \
  -u admin:password \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sample Product",
    "description": "Test product",
    "code": "PROD001",
    "primary_gtin": "12345678901234",
    "manufactured_at": "2024-01-01",
    "shelf_life_days": 365,
    "unit": "d",
    "status": true
  }'
```

### Using Python
```python
import requests
from requests.auth import HTTPBasicAuth

# Setup
BASE_URL = "http://localhost:8000/api/"
auth = HTTPBasicAuth('admin', 'password')

# List products
response = requests.get(f"{BASE_URL}products/", auth=auth)
print(response.json())

# Create a product
data = {
    "name": "Sample Product",
    "code": "PROD001",
    "primary_gtin": "12345678901234",
    # ... other fields
}
response = requests.post(f"{BASE_URL}products/", json=data, auth=auth)
print(response.json())
```

## 🎯 Special Features

### EPCIS Event Export
Get EPCIS events in JSON-LD or XML format:

```bash
# Get as JSON-LD
curl -u admin:password http://localhost:8000/api/epcis-events/1/json/

# Get as XML
curl -u admin:password http://localhost:8000/api/epcis-events/1/xml/
```

### Filtering & Search
```bash
# Filter products by status
curl -u admin:password "http://localhost:8000/api/products/?status=true"

# Search products by name
curl -u admin:password "http://localhost:8000/api/products/?search=Product"

# Filter batches by product
curl -u admin:password "http://localhost:8000/api/batches/?product=1"
```

## 📖 Full Documentation
See `API_README.md` for complete documentation.

## ✅ System Check
Run this to verify everything is working:
```bash
python manage.py check
python test_api.py
```

## 🔐 Security
- All endpoints require authentication
- Audit trails are automatically maintained
- 21 CFR Part 11 compliant
- EPCIS 2.0 standard compliant
