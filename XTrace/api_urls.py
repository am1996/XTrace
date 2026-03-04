from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Product.api_views import ProductViewSet
from Batch.api_views import BatchViewSet
from Equipment.api_views import EquipmentViewSet
from SerialNumber.api_views import SerialNumberViewSet
from SerialNumberPool.api_views import SerialNumberPoolViewSet
from StorageLocation.api_views import StorageLocationViewSet
from EPCISEvent.api_views import EPCISEventViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'batches', BatchViewSet, basename='batch')
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'serial-numbers', SerialNumberViewSet, basename='serialnumber')
router.register(r'serial-number-pools', SerialNumberPoolViewSet, basename='serialnumberpool')
router.register(r'storage-locations', StorageLocationViewSet, basename='storagelocation')
router.register(r'epcis-events', EPCISEventViewSet, basename='epcisevent')

urlpatterns = [
    path('', include(router.urls)),
]
