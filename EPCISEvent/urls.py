from django.urls import path
from EPCISEvent.views import *

app_name = "epcis_event"

urlpatterns = [
    path('', EPCISEventIndex.as_view(), name='epcis_event_list'),
    path('create/', EPCISEventCreate.as_view(), name='epcis_event_create'),
    path('<int:pk>/', EPCISEventDetails.as_view(), name='epcis_event_details'),
    path('<int:pk>/update/', EPCISEventUpdate.as_view(), name='epcis_event_update'),
    path('<int:pk>/delete/', EPCISEventDelete.as_view(), name='epcis_event_delete'),
]
