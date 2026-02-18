from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    # web
    path('web/', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
    path('', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
    path('web/batch/', include('Batch.urls', namespace='batch')),
    path('web/equipment/', include('Equipment.urls', namespace='equipment')),
    path('web/user/', include('User.urls', namespace='user')),
    path('web/serialnumber/', include('SerialNumber.urls', namespace='serialnumber')),
    path('web/storage_location/', include('StorageLocation.urls', namespace='storage_location')),
    path('web/serialnumberpool/', include('SerialNumberPool.urls', namespace='serialnumberpool')),
    path('web/epcis-events/', include('EPCISEvent.urls', namespace='epcis_event')),
    # API
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) if hasattr(settings, 'MEDIA_URL') else []
