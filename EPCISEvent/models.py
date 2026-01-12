from django.db import models

from Product.models import Product
from django.utils.translation import gettext_lazy as _

# Create your models here.
class EPCISEvent(models.Model):
    EVENT_TYPES = [
        ('ObjectEvent', 'Object Event'), # Observation, packing, etc.
        ('AggregationEvent', 'Aggregation'), # Putting items in a box
        ('TransactionEvent', 'Transaction'), # Change of ownership
    ]

    event_time = models.DateTimeField(verbose_name=_("When"))
    event_timezone_offset = models.CharField(max_length=10)
    
    # What
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    epc_list = models.TextField(help_text="List of EPCs involved in the event, separated by commas.")

    # Where
    read_point = models.CharField(max_length=255) # GLN (Global Location Number)
    biz_location = models.ForeignKey("StorageLocation.StorageLocation", on_delete=models.PROTECT, verbose_name=_("Business Location"))

    # Why
    biz_step = models.CharField(max_length=100, choices=[
        ('receiving', 'Receiving'),
        ('picking', 'Picking'),
        ('shipping', 'Shipping'),
        ('commissioning', 'Commissioning'),
    ])
    disposition = models.CharField(max_length=100) # e.g., "in_transit", "sellable"