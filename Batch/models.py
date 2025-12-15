from auditlog.registry import auditlog
from django.db import models
from django.urls import reverse

# Create your models here.
class Batch(models.Model):
    batch_number = models.CharField(max_length=100, unique=True, verbose_name="Batch Number")
    product = models.ForeignKey('Product.Product', on_delete=models.CASCADE, related_name='batches', verbose_name="Product")
    manufactured_at = models.DateField(verbose_name="Manufactured At")
    expiry_date = models.DateField(verbose_name="Expiry Date")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    sampled_quantity = models.PositiveIntegerField(verbose_name="Sampled Quantity")
    order_number = models.CharField(max_length=100, verbose_name="Order Number")
    batch_description = models.TextField(blank=True, null=True, verbose_name="Batch Description")
    serial_numbers = models.TextField(blank=True, null=True, verbose_name="Serial Numbers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Batch"
        verbose_name_plural = "Batches"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.sampled_quantity > self.quantity:
            raise ValidationError("Sampled quantity cannot be greater than total quantity.")

    def __str__(self):
        return f"Batch {self.batch_number} of {self.product.name}"

    def get_absolute_url(self):
        return reverse("batch_detail", kwargs={"pk": self.pk})


auditlog.register(Batch)
