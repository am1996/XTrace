from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _

class StorageLocation(models.Model):
    LOCATION_TYPES = [
        ('physical', _('Physical Warehouse/Facility')),
        ('logic', _('Logical Location (e.g., Virtual Stock)')),
        ('transit', _('In Transit')),
    ]

    name = models.CharField(max_length=255, verbose_name=_("Location Name"))
    
    # EPCIS Requirement: Global Location Number (13 digits)
    gln = models.CharField(
        max_length=13, 
        unique=True, 
        verbose_name=_("GLN"),
        help_text=_("Global Location Number (13 digits)")
    )
    
    # Specific sub-location (e.g., Bin, Shelf, or Dock Door)
    sub_location = models.CharField(max_length=100, blank=True, verbose_name=_("Sub-Location/Extension"))
    
    location_type = models.CharField(
        max_length=20, 
        choices=LOCATION_TYPES, 
        default='physical'
    )
    
    address = models.TextField(blank=True, verbose_name=_("Physical Address"))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Storage Location")
        verbose_name_plural = _("Storage Locations")

    def __str__(self):
        return f"{self.name} ({self.gln})"

    @property
    def epcis_uri(self):
        """Returns the location in EPCIS URI format."""
        return f"urn:epc:id:sgln:{self.gln}.{self.sub_location or '0'}"