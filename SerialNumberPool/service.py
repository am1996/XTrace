# SerialNumberPool/services.py (Simplified for Bulk)
import string
import secrets
from django.db import transaction

from SerialNumberPool.models import SerialNumberPool

# We keep the generator function
def generate_alphanumeric_serial(length):
    ALPHANUMERIC = string.ascii_letters + string.digits
    return ''.join(secrets.choice(ALPHANUMERIC) for i in range(length))

def reserve_pool_state_for_bulk(pool_id, quantity):
    """Locks the pool and updates the generated_count to reserve the quantity."""
    with transaction.atomic():
        try:
            pool = SerialNumberPool.objects.select_for_update().get(pool_id=pool_id)
            pool.generated_count += quantity
            pool.status = 'ACTIVE'
            pool.save()
            return pool
        except SerialNumberPool.DoesNotExist:
            raise ValueError(f"Pool '{pool_id}' does not exist.")