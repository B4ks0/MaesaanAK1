import os
import sys
import django
from django.test import TestCase
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import io

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ak1.settings')
django.setup()

from pendaftaran.models import PendaftaranAK1

class OCRTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_ocr_without_tesseract(self):
        """Test OCR endpoint when Tesseract is not installed"""
        # Create a dummy image
        img = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Create a SimpleUploadedFile
        uploaded_file = SimpleUploadedFile(
            "test_ktp.png",
            img_byte_arr.getvalue(),
            content_type="image/png"
        )

        # Make POST request to OCR endpoint
        response = self.client.post(
            reverse('process_ktp_ocr'),
            {'ktp_image': uploaded_file},
            format='multipart'
        )

        # Check that response is JSON and contains error message
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json())
        print("OCR test passed: Error handled when OCR processing fails")

if __name__ == '__main__':
    import unittest
    unittest.main()
