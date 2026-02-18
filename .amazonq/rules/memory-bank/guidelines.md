# Development Guidelines

## Code Quality Standards

### Django Model Conventions
- **Audit Trail Registration**: All models MUST be registered with auditlog for 21 CFR Part 11 compliance
  ```python
  from auditlog.registry import auditlog
  auditlog.register(ModelName)
  ```
- **Timestamp Fields**: Include `created_at` (auto_now_add=True) and `updated_at` (auto_now=True) on all models
- **Verbose Names**: Use `verbose_name` parameter for all fields to provide human-readable labels
- **Foreign Key Relations**: Always specify `related_name` for reverse lookups and `on_delete` behavior
- **UUID Primary Keys**: Use UUID fields for models requiring globally unique identifiers (e.g., `pool_id = models.UUIDField(primary_key=True, default=uuid4)`)
- **Soft Deletes**: Implement soft delete pattern with `deleted_at` field instead of hard deletes where audit trail is critical
  ```python
  def delete(self, **kwargs):
      from django.utils import timezone
      self.deleted_at = timezone.now()
      self.save()
      return True
  ```

### Field Naming and Types
- **GS1 Standards**: Use appropriate field types for GS1 identifiers:
  - GTIN: `CharField(max_length=14)` with unique constraint
  - GLN: `CharField(max_length=13)` with unique constraint
  - SGTIN/SGLN: Store as URN format strings
- **Choice Fields**: Define choices as module-level constants in UPPERCASE with descriptive tuples
  ```python
  STATUS_CHOICES = [
      ('ACTIVE', 'Active/Generating'),
      ('EXHAUSTED', 'Exhausted/Used Up'),
  ]
  ```
- **Network Fields**: Use `GenericIPAddressField` for IP addresses, `CharField(max_length=17)` for MAC addresses
- **Internationalization**: Use `gettext_lazy` for translatable strings: `from django.utils.translation import gettext_lazy as _`

### Model Methods and Properties
- **String Representation**: Always implement `__str__()` method returning meaningful identifier
- **EPCIS URI Generation**: Provide `@property` methods for EPCIS-compliant URI formats
  ```python
  @property
  def epcis_uri(self):
      return f"urn:epc:id:sgln:{self.gln}.{self.sub_location or '0'}"
  ```
- **EPCIS Document Generation**: Implement `get_epcis_json()` and `to_epcis_xml()` methods for event models
- **Absolute URLs**: Define `get_absolute_url()` for models with detail views

## View Patterns

### Class-Based Views (CBV)
- **Preferred Approach**: Use Django's generic class-based views for CRUD operations
- **Standard View Classes**:
  - `ListView`: For index/list pages (set `context_object_name` for template clarity)
  - `DetailView`: For detail pages
  - `CreateView`: For creation forms (specify `fields` list)
  - `UpdateView`: For edit forms (specify `fields` list)
  - `DeleteView`: For deletion confirmation
- **Template Naming**: Follow convention `<app_name>/<action>.html` (e.g., `Batch/create.html`)
- **Success URLs**: Define `success_url` as string path or use `reverse_lazy()` for named URLs
- **Authentication**: Use `LoginRequiredMixin` for views requiring authentication

### View Configuration
```python
class BatchIndex(ListView):
    model = Batch
    template_name = 'Batch/index.html'
    context_object_name = 'batches'  # Clear variable name in template
```

### Custom Business Logic in Views
- **Form Validation**: Override `form_valid()` for custom logic after form validation
- **Object Retrieval**: Override `get_object()` for custom object lookup logic
- **Context Data**: Override `get_context_data()` to add extra context variables
- **Dispatch Logic**: Override `dispatch()` for request-level logic (e.g., redirect authenticated users)

## URL Configuration

### URL Patterns
- **Namespace**: Always define `app_name` for namespaced URL routing
  ```python
  app_name = "batch"
  ```
- **RESTful Patterns**: Follow RESTful conventions:
  - List: `''` → `batch_list`
  - Create: `'create/'` → `batch_create`
  - Detail: `'<int:pk>/'` → `batch_details`
  - Update: `'<int:pk>/update/'` → `batch_update`
  - Delete: `'<int:pk>/delete/'` → `batch_delete`
- **URL Naming**: Use descriptive names with `<model>_<action>` pattern
- **Include Pattern**: Use `include()` with namespace in root URLs
  ```python
  path('web/batch/', include('Batch.urls', namespace='batch'))
  ```

## Service Layer Pattern

### Business Logic Separation
- **Service Modules**: Extract complex business logic into dedicated `service.py` files
- **Transaction Management**: Use `@transaction.atomic()` decorator for database consistency
- **Locking**: Use `select_for_update()` for row-level locking in concurrent operations
  ```python
  with transaction.atomic():
      pool = SerialNumberPool.objects.select_for_update().get(pool_id=pool_id)
      pool.generated_count += quantity
      pool.save()
  ```

### Custom Managers
- **Manager Classes**: Create custom managers for model-level business logic
  ```python
  class SerialNumberPoolManager(models.Manager):
      def create_pool_for_product(self, total_count, user=None):
          pool = self.create(total_to_generate=total_count, generated_by=user)
          return pool
  ```
- **Manager Assignment**: Assign custom manager to model: `objects = CustomManager()`

## EPCIS Compliance Patterns

### EPCIS 2.0 JSON-LD Generation
- **Context**: Always include GS1 context URL: `https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld`
- **Document Structure**: Wrap events in EPCISDocument envelope with schemaVersion "2.0"
- **Event Fields**: Include required fields: type, eventID (urn:uuid format), eventTime (ISO format), eventTimeZoneOffset
- **URN Format**: Use URN format for business vocabulary: `urn:epcglobal:cbv:bizstep:{value}`
- **Digital Links**: Use GS1 Digital Link format for locations: `https://id.gs1.org/414/{gln}`

### EPCIS 2.0 XML Generation
- **Namespaces**: Register and use proper namespaces:
  ```python
  NS_EPCIS = "urn:epcglobal:epcis:xsd:2"
  ET.register_namespace('epcis', NS_EPCIS)
  ```
- **Schema Location**: Include xsi:schemaLocation attribute in root element
- **Pretty Printing**: Use minidom.parseString().toprettyxml() for readable output
- **CBV 2.0 URIs**: Use HTTPS format for business vocabulary: `https://ref.gs1.org/cbv/bizstep/{value}`

### EPCIS Event Types
Support all five EPCIS 2.0 event types:
- ObjectEvent: Individual item observations
- AggregationEvent: Parent-child relationships
- TransactionEvent: Business transaction associations
- TransformationEvent: Input-output transformations
- AssociationEvent: Object associations

## Security and Compliance

### Authentication and Authorization
- **Login Required**: Use `LoginRequiredMixin` or `@login_required` decorator
- **User Context**: Access current user via `self.request.user` in views
- **Redirect Logic**: Set `redirect_authenticated_user = True` to prevent logged-in users from accessing login/register pages

### Audit Trail Requirements
- **Automatic Tracking**: django-auditlog middleware automatically logs all model changes
- **User Attribution**: Ensure user is set in request context for audit trail attribution
- **Immutable Logs**: Never delete audit log entries; use soft deletes for data

### Data Integrity
- **Unique Constraints**: Enforce uniqueness on critical identifiers (GTIN, GLN, serial numbers)
- **Foreign Key Protection**: Use `on_delete=models.PROTECT` for critical relationships
- **Validation**: Implement model-level validation in `clean()` method

## Code Style and Formatting

### Import Organization
1. Standard library imports
2. Django imports (grouped by module)
3. Third-party imports (auditlog, etc.)
4. Local application imports
```python
import uuid
from django.db import models
from django.utils import timezone
from auditlog.registry import auditlog
from Product.models import Product
```

### Docstrings and Comments
- **Module Docstrings**: Include purpose and key functionality at module level
- **Method Docstrings**: Use triple-quoted strings for complex methods
- **Inline Comments**: Use sparingly; prefer self-documenting code
- **Configuration Comments**: Document settings and constants with inline comments

### Naming Conventions
- **Models**: PascalCase singular nouns (e.g., `SerialNumberPool`)
- **Variables**: snake_case (e.g., `batch_number`, `created_at`)
- **Constants**: UPPERCASE_WITH_UNDERSCORES (e.g., `SN_STATUS_CHOICES`)
- **Methods**: snake_case verbs (e.g., `create_pool_for_product()`)
- **Template Names**: lowercase with underscores (e.g., `batch_confirm_delete.html`)

## Template Patterns

### Template Organization
- **Base Template**: Use `base.html` for common layout and navigation
- **App-Specific Directories**: Organize templates by app: `templates/<AppName>/`
- **Naming Convention**: Use descriptive names: `create.html`, `details.html`, `index.html`, `<model>_confirm_delete.html`

### Template Tags
- **Custom Tags**: Register custom template tags in `templatetags/` directory
- **Form Rendering**: Create custom form tags for consistent form rendering
- **Tag Libraries**: Register in settings.py under TEMPLATES['OPTIONS']['libraries']

## Database Migrations

### Migration Best Practices
- **Initial Migration**: Always named `0001_initial.py`
- **Descriptive Names**: Subsequent migrations describe the change (e.g., `0002_equipment_deleted_at.py`)
- **Empty __init__.py**: All migration directories must have empty `__init__.py` file
- **Review Before Commit**: Always review auto-generated migrations for correctness
- **Data Migrations**: Use separate data migrations for complex data transformations

## Testing Standards

### Test Organization
- **Test Files**: Place tests in `tests.py` within each app
- **Test Classes**: Group related tests in test classes
- **Test Methods**: Prefix test methods with `test_`
- **Fixtures**: Use Django fixtures or factory patterns for test data

## Configuration Management

### Settings Organization
- **Environment Variables**: Use environment variables for sensitive data (SECRET_KEY, database credentials)
- **Debug Mode**: Set `DEBUG = False` in production
- **Allowed Hosts**: Configure `ALLOWED_HOSTS` appropriately for deployment
- **Static Files**: Configure `STATIC_URL`, `STATICFILES_DIRS`, and `STATIC_ROOT`
- **Installed Apps**: Register all custom apps in `INSTALLED_APPS`
- **Middleware Order**: Maintain correct middleware order (security, session, auth, auditlog)

### GS1 Configuration
- **Company Prefix**: Store in settings: `EPCIS_COMPANY_PREFIX`
- **Facility GLN**: Store in settings: `EPCIS_FACILITY_GLN`
- **Configuration Access**: Use `getattr(settings, 'KEY', 'default')` for optional settings

## Error Handling

### Exception Handling
- **Specific Exceptions**: Catch specific exceptions (e.g., `DoesNotExist`, `ValueError`)
- **Transaction Rollback**: Use `transaction.atomic()` to ensure rollback on errors
- **User Feedback**: Provide meaningful error messages to users
- **Logging**: Log errors for debugging and audit purposes

## Performance Optimization

### Database Queries
- **Select Related**: Use `select_related()` for foreign key relationships
- **Prefetch Related**: Use `prefetch_related()` for many-to-many and reverse foreign keys
- **Query Optimization**: Avoid N+1 queries by using joins
- **Indexing**: Add `db_index=True` to frequently queried fields

### Bulk Operations
- **Bulk Create**: Use `bulk_create()` for inserting multiple records
- **Bulk Update**: Use `bulk_update()` for updating multiple records
- **Atomic Operations**: Wrap bulk operations in `transaction.atomic()`
