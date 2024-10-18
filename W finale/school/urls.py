from django.urls import path
from .views import register_user, success, check_permissions

urlpatterns = [
    path('register/', register_user, name='register'),
    path('success/', success, name='success'),
    path('check-permissions/', check_permissions, name='check_permissions'),
]
