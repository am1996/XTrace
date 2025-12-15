from uuid import uuid4 
from django.db import models
from django.contrib.auth.models import User

from XTrace import settings

# Create your models here.
# --- Status Choices ---
SN_STATUS_CHOICES = [
    ('ALLOCATED', 'Allocated to Pool (Ready to use)'),
    ('PRINTED', 'Printed/Reserved by Production Line'),
    ('CONSUMED', 'Shipped/Reported Consumed'),
    ('VOID', 'Void/Scrapped (Permanently retired)'),
]

POOL_STATUS_CHOICES = [
    ('NEW', 'New/Allocated'),
    ('ACTIVE', 'Active/Generating'),
    ('EXHAUSTED', 'Exhausted/Used Up'),
    ('VOID', 'Void/Canceled')
]

class SerialNumberPool(models.Model):
    """
    Defines a block/range of unique serial numbers generated for a specific GTIN.
    """
    pool_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    
    # Tracking
    total_to_generate = models.IntegerField(help_text="Total requested count of S/Ns.")
    generated_count = models.IntegerField(default=0, help_text="Count of S/Ns successfully created in the SN table.")
    
    status = models.CharField(max_length=10, choices=POOL_STATUS_CHOICES, default='NEW', db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Pool {self.pool_id}"