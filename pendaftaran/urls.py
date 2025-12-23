from django.urls import path
from . import views

urlpatterns = [
    path('pendaftaran-ak1/', views.pendaftaran_ak1, name='pendaftaran'),
    path('status-pendaftaran/', views.status_pendaftaran, name='status_pendaftaran'),
    path('kartu-ak1/', views.kartu_ak1, name='kartu_ak1'),
    path('process-ktp-ocr/', views.process_ktp_ocr, name='process_ktp_ocr'),
    path('pendaftaran-list/', views.list_pendaftaran, name='list_pendaftaran'),
    path('pendaftaran/<int:pk>/review/', views.review_pendaftaran, name='review_pendaftaran'),
    path('pendaftaran/<int:pk>/download-pdf/', views.download_kartu_pdf, name='download_kartu_pdf'),
]
