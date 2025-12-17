from uuid import uuid4 
from django.db import models
from django.contrib.auth.models import User

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

class SerialNumberPoolManager(models.Manager):
    def create_pool_for_product(self, total_count, user=None):
        """
        Creates a new SerialNumberPool.
        Note: Ensure 'product' logic is added if pools must link to products.
        """
        # Use self.create to immediately save to DB
        pool = self.create(
            total_to_generate=total_count,
            generated_by=user
        )
        return pool

class SerialNumberPool(models.Model):
    pool_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    
    total_to_generate = models.IntegerField(help_text="Total requested count of S/Ns.")
    generated_count = models.IntegerField(default=0, help_text="Count of S/Ns created.")
    
    status = models.CharField(max_length=10, choices=POOL_STATUS_CHOICES, default='NEW', db_index=True)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    manager = SerialNumberPoolManager()

    def __str__(self):
        return f"Pool {self.pool_id}"