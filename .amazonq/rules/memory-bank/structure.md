# Project Structure

## Architecture Overview
XTRACE follows a Django-based modular architecture with domain-driven design principles. Each business domain is encapsulated in a dedicated Django app, promoting separation of concerns and maintainability.

## Directory Structure

```
XTrace/
├── XTrace/                    # Django project configuration
│   ├── settings.py           # Application settings and configuration
│   ├── urls.py               # Root URL routing
│   ├── wsgi.py               # WSGI application entry point
│   ├── asgi.py               # ASGI application entry point
│   └── templatetags/         # Custom template tags
│       └── form_tags.py      # Form rendering utilities
│
├── Product/                   # Product management domain
│   ├── models.py             # Product data models
│   ├── views.py              # Product views and controllers
│   ├── admin.py              # Django admin configuration
│   ├── urls.py               # Product-specific URL routing
│   └── migrations/           # Database schema migrations
│
├── Batch/                     # Batch management domain
│   ├── models.py             # Batch data models
│   ├── views.py              # Batch views and controllers
│   ├── admin.py              # Django admin configuration
│   ├── urls.py               # Batch-specific URL routing
│   └── migrations/           # Database schema migrations
│
├── SerialNumber/              # Serial number tracking domain
│   ├── models.py             # Serial number data models
│   ├── views.py              # Serial number views
│   ├── urls.py               # Serial number URL routing
│   ├── management/           # Custom management commands
│   └── migrations/           # Database schema migrations
│
├── SerialNumberPool/          # Serial number pool management
│   ├── models.py             # Pool data models
│   ├── service.py            # Business logic layer
│   ├── views.py              # Pool views and controllers
│   ├── urls.py               # Pool-specific URL routing
│   └── migrations/           # Database schema migrations
│
├── Equipment/                 # Equipment tracking domain
│   ├── models.py             # Equipment data models
│   ├── views.py              # Equipment views
│   ├── urls.py               # Equipment URL routing
│   └── migrations/           # Database schema migrations
│
├── StorageLocation/           # Storage location management
│   ├── models.py             # Location data models
│   ├── views.py              # Location views
│   ├── urls.py               # Location URL routing
│   └── migrations/           # Database schema migrations
│
├── EPCISEvent/                # EPCIS event generation and management
│   ├── models.py             # EPCIS event models with JSON-LD/XML generation
│   ├── views.py              # Event views and controllers
│   ├── urls.py               # Event URL routing
│   └── migrations/           # Database schema migrations
│
├── User/                      # User management and authentication
│   ├── models.py             # User-related models
│   ├── views.py              # Authentication views
│   ├── urls.py               # User URL routing
│   └── admin.py              # User admin configuration
│
├── utils/                     # Shared utilities
│   └── epcis_generator.py    # EPCIS document generation utilities
│
├── templates/                 # HTML templates
│   ├── base.html             # Base template with common layout
│   ├── home.html             # Homepage template
│   ├── Product/              # Product-specific templates
│   ├── Batch/                # Batch-specific templates
│   ├── SerialNumber/         # Serial number templates
│   ├── SerialNumberPool/     # Pool templates
│   ├── Equipment/            # Equipment templates
│   ├── StorageLocation/      # Location templates
│   ├── EPCISEvent/           # EPCIS event templates
│   └── User/                 # User authentication templates
│
├── staticfiles/               # Static assets
│   ├── css/                  # Stylesheets (Bootstrap)
│   └── js/                   # JavaScript files (Bootstrap)
│
├── .github/workflows/         # CI/CD configuration
│   └── django.yml            # GitHub Actions workflow
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── db.sqlite3                # SQLite database (development)
└── README.md                 # Project documentation
```

## Core Components

### Django Apps (Domain Modules)
Each app follows Django's standard structure with models, views, URLs, and templates:
- **Product**: Manages product definitions and GS1 identifiers
- **Batch**: Handles production batch tracking and lifecycle
- **SerialNumber**: Tracks individual serialized items
- **SerialNumberPool**: Manages serial number allocation and pooling
- **Equipment**: Monitors equipment used in production
- **StorageLocation**: Tracks physical storage locations
- **EPCISEvent**: Generates EPCIS 2.0 compliant events (JSON-LD and XML)
- **User**: Handles authentication and user management

### Shared Components
- **XTrace/**: Project-level configuration and URL routing
- **utils/**: Reusable utilities for EPCIS generation
- **templates/**: HTML templates with Bootstrap styling
- **staticfiles/**: CSS and JavaScript assets

## Architectural Patterns

### Model-View-Template (MVT)
Django's MVT pattern separates concerns:
- **Models**: Data layer with ORM-based database access
- **Views**: Business logic and request handling
- **Templates**: Presentation layer with Django template language

### Domain-Driven Design
Each business domain is isolated in its own app with:
- Clear boundaries between domains
- Domain-specific models and business logic
- Independent URL routing and templates

### Service Layer Pattern
Complex business logic is extracted into service modules (e.g., SerialNumberPool/service.py) to keep views thin and promote reusability.

### Audit Trail Integration
django-auditlog middleware automatically tracks all model changes for 21 CFR Part 11 compliance, providing comprehensive audit trails without manual instrumentation.

## Data Flow
1. **User Request** → URL routing (urls.py)
2. **View Processing** → Business logic execution (views.py)
3. **Model Operations** → Database interaction (models.py)
4. **Audit Logging** → Automatic change tracking (auditlog middleware)
5. **Template Rendering** → HTML response (templates/)
6. **EPCIS Generation** → JSON-LD/XML output (EPCISEvent/models.py)

## Integration Points
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **Audit System**: django-auditlog for 21 CFR Part 11 compliance
- **EPCIS Output**: JSON-LD and XML formats for trading partner integration
- **Static Assets**: Bootstrap for responsive UI
