from django.contrib import admin
from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path('dashboard/', UserDashboard.as_view(), name='dashboard'),
    path('<int:pk>/', UserDetails.as_view(), name='details'),
    path('<int:pk>/edit', UserUpdate.as_view(), name='update'),
    path('<int:pk>/delete', UserDelete.as_view(), name='delete'),
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
]
