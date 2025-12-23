from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from pendaftaran.models import PendaftaranAK1

User = get_user_model()


class PencakerViewsTestCase(TestCase):
    """Test cases untuk pencaker views"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_dashboard_requires_login(self):
        """Test dashboard requires login"""
        response = self.client.get(reverse('pencaker:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_dashboard_authenticated(self):
        """Test dashboard for authenticated user"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('pencaker:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pencaker/dashboard.html')
    
    def test_upload_ktp_requires_login(self):
        """Test upload KTP requires login"""
        response = self.client.get(reverse('pencaker:upload_ktp'))
        self.assertEqual(response.status_code, 302)
    
    def test_upload_ktp_get(self):
        """Test upload KTP GET request"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('pencaker:upload_ktp'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pencaker/upload_ktp.html')
    
    def test_isi_data_diri_requires_pendaftaran(self):
        """Test isi_data_diri requires existing pendaftaran"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('pencaker:isi_data_diri'))
        self.assertEqual(response.status_code, 302)  # Redirect to upload_ktp
    
    def test_isi_data_diri_with_pendaftaran(self):
        """Test isi_data_diri with existing pendaftaran"""
        # Create pendaftaran
        PendaftaranAK1.objects.create(
            user=self.user,
            nik='1234567890123456',
            nama='Test User',
            ttl='Jakarta, 01-01-1990',
            jk='LAKI-LAKI',
            status_perkawinan='BELUM KAWIN',
            alamat='Jl. Test No. 123'
        )
        
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('pencaker:isi_data_diri'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pencaker/isi_data_diri.html')


class OCRUtilsTestCase(TestCase):
    """Test cases untuk OCR utilities"""
    
    def test_imports(self):
        """Test that OCR utils can be imported"""
        from pencaker.ocr_utils import (
            preprocess_and_ocr,
            analyze_ktp_with_gemini,
            process_ktp_image
        )
        self.assertIsNotNone(preprocess_and_ocr)
        self.assertIsNotNone(analyze_ktp_with_gemini)
        self.assertIsNotNone(process_ktp_image)
