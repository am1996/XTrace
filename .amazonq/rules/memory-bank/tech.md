# Technology Stack

## Programming Languages
- **Python 3.x**: Primary development language
- **HTML/CSS/JavaScript**: Frontend presentation layer
- **SQL**: Database queries via Django ORM

## Core Framework
- **Django 6.0.2**: High-level Python web framework
  - MVT (Model-View-Template) architecture
  - Built-in ORM for database abstraction
  - Admin interface for data management
  - URL routing and middleware support
  - Template engine for HTML rendering

## Key Dependencies

### Compliance & Audit
- **django-auditlog 3.4.1**: Automatic audit trail generation for 21 CFR Part 11 compliance
  - Tracks all model changes (create, update, delete)
  - Records user, timestamp, and change details
  - Provides tamper-proof audit logs

### Data Management
- **django-jsonfield 1.4.1**: JSON field support for flexible data storage
- **numpy 2.4.2**: Numerical computing for data processing
- **python-dateutil 2.9.0.post0**: Advanced date/time parsing and manipulation

### Frontend
- **Bootstrap 5.x**: Responsive CSS framework (included in staticfiles/)
  - Grid system for responsive layouts
  - Pre-built UI components
  - JavaScript plugins for interactivity

## Database
- **SQLite3**: Development database (db.sqlite3)
- **Production Options**: PostgreSQL, MySQL, Oracle (via Django ORM)

## Standards Compliance
- **EPCIS 2.0**: GS1 Electronic Product Code Information Services
  - JSON-LD format with @context from https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld
  - XML format with urn:epcglobal:epcis:xsd:2 namespace
- **GS1 Digital Links**: Modern URI-based product identification
- **21 CFR Part 11**: FDA electronic records and signatures compliance

## Development Tools

### Project Management
```bash
# Django management script
python manage.py <command>
```

### Common Commands
```bash
# Run development server
python manage.py runserver

# Create database migrations
python manage.py makemigrations

# Apply database migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Collect static files for production
python manage.py collectstatic

# Run tests
python manage.py test

# Open Django shell
python manage.py shell
```

### Database Migrations
Django's migration system tracks schema changes:
- Each app has a `migrations/` directory
- Migrations are versioned (0001_initial.py, 0002_*.py, etc.)
- Automatic schema evolution with rollback support

## Project Configuration

### Settings (XTrace/settings.py)
- **SECRET_KEY**: Django cryptographic signing key
- **DEBUG**: Development mode flag (True for dev, False for production)
- **ALLOWED_HOSTS**: Permitted host/domain names
- **INSTALLED_APPS**: Registered Django applications
- **MIDDLEWARE**: Request/response processing pipeline
- **DATABASES**: Database connection configuration
- **STATIC_URL**: URL prefix for static files
- **TIME_ZONE**: UTC for consistent timestamps

### URL Configuration (XTrace/urls.py)
- Root URL routing to app-specific URL configurations
- Admin interface at /admin/
- App-specific routes included via include()

### WSGI/ASGI
- **wsgi.py**: Web Server Gateway Interface for production deployment
- **asgi.py**: Asynchronous Server Gateway Interface for async support

## Deployment Considerations

### Production Settings
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS` with actual domain names
- Use environment variables for `SECRET_KEY`
- Switch to PostgreSQL or MySQL database
- Configure static file serving (nginx, whitenoise)
- Enable HTTPS and security middleware

### CI/CD
- GitHub Actions workflow defined in `.github/workflows/django.yml`
- Automated testing and deployment pipeline

## Development Environment Setup

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Requirements
```
Django==6.0.2
django-auditlog==3.4.1
django-jsonfield==1.4.1
numpy==2.4.2
python-dateutil==2.9.0.post0
```

## Code Organization Standards
- **Models**: Define in `models.py` with Django ORM
- **Views**: Implement in `views.py` using class-based or function-based views
- **URLs**: Configure in `urls.py` with path() or re_path()
- **Templates**: Store in `templates/<app_name>/` directory
- **Static Files**: Place in `staticfiles/` for CSS/JS assets
- **Migrations**: Auto-generated in `migrations/` directory
- **Admin**: Customize in `admin.py` for Django admin interface

## Testing Framework
- Django's built-in test framework (unittest-based)
- Test files: `tests.py` in each app
- Run with: `python manage.py test`
