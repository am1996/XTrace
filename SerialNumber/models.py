from django.db import models
import SerialNumberPool
from SerialNumberPool.models import SN_STATUS_CHOICES

# Create your models here.
class SerialNumber(models.Model):
    """
    The record for every single unique serial number.
    Uniqueness constraint on full_serial_number is the key compliance mechanism.
    """
    # Max length should accommodate the longest required serial number code (e.g., 10-20 digits)
    full_serial_number = models.CharField(
        max_length=20, 
        unique=True, # STRICTLY ENFORCED: Guarantees no reuse.
        db_index=True
    )
    
    # Association to the Pool
    pool = models.ForeignKey('SerialNumberPool.SerialNumberPool', on_delete=models.PROTECT, related_name='serial_numbers')

    # Batch/Lot Assignment (Null until consumption/printing)
    batch_lot = models.CharField(
        max_length=20, 
        null=True, 
        blank=True,
        help_text="Assigned Batch/Lot Number at consumption."
    )
    expiration_date = models.DateField(null=True, blank=True)

    # State and Traceability
    status = models.CharField(max_length=10, choices=SN_STATUS_CHOICES, default='ALLOCATED', db_index=True)
    
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Individual Serial Number"
        verbose_name_plural = "Individual Serial Numbers"