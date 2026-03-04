# XTrace REST API Documentation

## Overview
The XTrace REST API provides programmatic access to all core functionality of the track and trace system. All endpoints require authentication and follow RESTful conventions.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The API uses Session Authentication and Basic Authentication. Include credentials with each request.

### Login via Browser
Navigate to: `http://localhost:8000/api-auth/login/`

## API Endpoints

### Products
- **List/Create**: `GET/POST /api/products/`
- **Retrieve/Update/Delete**: `GET/PUT/PATCH/DELETE /api/products/{id}/`
- **Filters**: `?status=true&code=PROD001`
- **Search**: `?search=product_name`

### Batches
- **List/Create**: `GET/POST /api/batches/`
- **Retrieve/Update/Delete**: `GET/PUT/PATCH/DELETE /api/batches/{id}/`
- **Filters**: `?batch_number=BATCH001&product={product_id}`
- **Search**: `?search=batch_number`

### Equipment
- **List/Create**: `GET/POST /api/equipment/`
- **Retrieve/Update/Delete**: `GET/PUT/PATCH/DELETE /api/equipment/{id}/`
- **Filters**: `?plant_gln=1234567890123&manufacturer=Acme`
- **Search**: `?search=equipment_name`

### Serial Numbers
- **List/Create**: `GET/POST /api/serial-numbers/`
- **Retrieve/Update/Delete**: `GET/PUT/PATCH/DELETE /api/serial-numbers/{id}/`
- **Filters**: `?status=ALLOCATED&pool={pool_id}`
- **Search**: `?search=serial_number`

### Serial Number Pools
- **List/Create**: `GET/POST /api/serial-number-pools/`
- **Retrieve/Update/Delete**: `GET/PUT/PATCH/DELETE /api/serial-number-pools/{pool_id}/`
- **Filters**: `?status=ACTIVE`

### Storage Locations
- **List/Create**: `GET/POST /api/storage-locations/`
- **Retrieve/Update/Delete**: `GET/PUT/PATCH/DELETE /api/storage-locations/{id}/`
- **Filters**: `?location_type=physical&gln=1234567890123`
- **Search**: `?search=location_name`

### EPCIS Events
- **List/Create**: `GET/POST /api/epcis-events/`
- **Retrieve/Update/Delete**: `GET/PUT/PATCH/DELETE /api/epcis-events/{id}/`
- **Get JSON**: `GET /api/epcis-events/{id}/json/`
- **Get XML**: `GET /api/epcis-events/{id}/xml/`
- **Filters**: `?event_type=ObjectEvent&action=OBSERVE`

## Example Requests

### Create a Product
```bash
curl -X POST http://localhost:8000/api/products/ \
  -u username:password \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product A",
    "description": "Description",
    "code": "PROD001",
    "primary_gtin": "12345678901234",
    "manufactured_at": "2024-01-01",
    "shelf_life_days": 365,
    "unit": "d",
    "status": true
  }'
```

### List Products with Filtering
```bash
curl -X GET "http://localhost:8000/api/products/?status=true&search=Product" \
  -u username:password
```

### Get EPCIS Event as JSON
```bash
curl -X GET http://localhost:8000/api/epcis-events/1/json/ \
  -u username:password
```

### Get EPCIS Event as XML
```bash
curl -X GET http://localhost:8000/api/epcis-events/1/xml/ \
  -u username:password
```

## Response Format
All responses follow standard REST conventions:
- **200 OK**: Successful GET/PUT/PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Validation errors
- **401 Unauthorized**: Authentication required
- **404 Not Found**: Resource not found

## Pagination
List endpoints return paginated results (50 items per page):
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [...]
}
```

## Installation
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Testing
Access the browsable API at: `http://localhost:8000/api/`
