from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Product Name"))
    description = models.TextField(verbose_name=_("Description"))
    code = models.CharField(max_length=100, unique=True, verbose_name=_("Product Code"))
    primary_gtin = models.CharField(max_length=14, unique=True, verbose_name=_("Primary GTIN"))
    secondary_gtin = models.CharField(max_length=14, blank=True, null=True, verbose_name=_("Secondary GTIN"))
    tertiary_gtin = models.CharField(max_length=14, blank=True, null=True, verbose_name=_("Tertiary GTIN"))
    equipment = models.ForeignKey("Equipment.Equipment", on_delete=models.CASCADE, verbose_name=_("Equipment"), related_name="products", null=True, blank=True)
    manufactured_at = models.DateField(verbose_name=_("Manufactured At")) 
    shelf_life_days = models.PositiveIntegerField()
    unit = models.CharField(max_length=50, verbose_name=_("Unit of Measurement"),choices=[
        ("y", _("Year")),
        ("m", _("Month")),
        ("d", _("Day"))
    ])
    status = models.BooleanField(default=False, verbose_name=_("Status"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

auditlog.register(Product)
