from django.urls import path
from . import views

app_name = 'pencaker'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-ktp/', views.upload_ktp, name='upload_ktp'),
    path('review-ktp/', views.review_ktp, name='review_ktp'),
    path('isi-data-diri/', views.isi_data_diri, name='isi_data_diri'),
    
    # AJAX endpoints
    path('api/preview-ktp/', views.preview_ktp_ajax, name='preview_ktp_ajax'),
    path('api/extract-ktp/', views.extract_ktp_ajax, name='extract_ktp_ajax'),
    
    # Debug
    path('test-ocr/', views.test_ocr, name='test_ocr'),
]
