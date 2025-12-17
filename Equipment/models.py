import datetime
from auditlog.registry import auditlog
from django.db import models

# Create your models here.

class Equipment(models.Model):
    name = models.CharField(max_length=255, verbose_name="Equipment Name")
    model_number = models.CharField(max_length=100, unique=True, verbose_name="Model Number")
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Serial Number")
    manufacturer = models.CharField(max_length=255, verbose_name="Manufacturer")
    mac_address = models.CharField(max_length=17, unique=True, verbose_name="MAC Address")
    ip_address = models.GenericIPAddressField(unique=True, verbose_name="IP Address")
    plant_name = models.CharField(max_length=255, verbose_name="Plant Name")
    plant_gln = models.CharField(max_length=13, unique=True, verbose_name="Plant GLN")
    location = models.CharField(max_length=255, verbose_name="Location")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"

    def delete(self, **kwargs):
        self.deleted_at = datetime.datetime.now()
        self.save()
        return True
    
    def __str__(self):
        return self.name
    
auditlog.register(Equipment)    