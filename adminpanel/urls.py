from django.urls import path
from . import views

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/verify/<int:registration_id>/', views.verify_registration, name='verify_registration'),
]
