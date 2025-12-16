from auditlog.registry import auditlog
from django.db import models
from django.urls import reverse

class Batch(models.Model):
    batch_number = models.CharField(max_length=100, unique=True, verbose_name="Batch Number")
    product = models.ForeignKey('Product.Product', on_delete=models.CASCADE, related_name='batches', verbose_name="Product")
    manufactured_at = models.DateField(verbose_name="Manufactured At")
    expiry_date = models.DateField(verbose_name="Expiry Date")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    sampled_quantity = models.PositiveIntegerField(verbose_name="Sampled Quantity")
    order_number = models.CharField(max_length=100, verbose_name="Order Number")
    batch_description = models.TextField(blank=True, null=True, verbose_name="Batch Description")
    
    serial_pool = models.ForeignKey(
        'SerialNumberPool.SerialNumberPool', 
        on_delete=models.PROTECT,
        related_name='batches_used_in',
        verbose_name="Serial Number Configuration Pool"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

auditlog.register(Batch)