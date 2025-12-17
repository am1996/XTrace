from django.contrib import admin
from django.urls import include, path
urlpatterns = [
    path('admin/', admin.site.urls),
    # web
    path('web/batch/', include('Batch.urls', namespace='batch')),
    path('web/equipment/', include('Equipment.urls', namespace='equipment')),
    # API
]
