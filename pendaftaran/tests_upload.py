from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from pendaftaran.models import PendaftaranAK1

User = get_user_model()


class PendaftaranFileUploadTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='upload@test.com', nama_lengkap='Upload User', password='testpass')

    def test_file_uploads_saved_base64(self):
        # Login
        self.client.login(email='upload@test.com', password='testpass')

        url = '/pendaftaran/pendaftaran-ak1/'

        # Minimal required form data
        data = {
            'nik': '1234567890123456',
            'nama': 'Upload Test',
            'ttl': 'Jakarta, 01-01-1990',
            'jk': 'LAKI-LAKI',
            'status_perkawinan': 'BELUM KAWIN',
            'alamat': 'Jl. Test No.1',
        }

        # Create small dummy files
        ktp_file = SimpleUploadedFile('ktp.jpg', b'testktpdata', content_type='image/jpeg')
        photo_file = SimpleUploadedFile('photo.png', b'testphotodata', content_type='image/png')
        ijazah_file = SimpleUploadedFile('ijazah.pdf', b'%PDF-1.4 testpdf', content_type='application/pdf')

        post_data = {**data, 'ktp': ktp_file, 'photo': photo_file, 'ijazah': ijazah_file}
        response = self.client.post(url, data=post_data, follow=True)

        # After successful submission the view should redirect and we follow it
        self.assertIn(response.status_code, (200, 302))

        # Check that the PendaftaranAK1 object was created
        obj = PendaftaranAK1.objects.filter(nik='1234567890123456').first()
        self.assertIsNotNone(obj, msg=f"Pendaftaran object not created. Response content:\n{response.content.decode('utf-8')}")

        # Base64 fields should be populated (not None)
        self.assertIsNotNone(obj.ktp_data, msg=f"ktp_data missing. Response: {response.content[:200]}")
        self.assertIsNotNone(obj.photo_data, msg=f"photo_data missing. Response: {response.content[:200]}")
        self.assertIsNotNone(obj.ijazah_data, msg=f"ijazah_data missing. Response: {response.content[:200]}")

        # Basic length checks
        self.assertTrue(len(obj.ktp_data) > 10)
        self.assertTrue(len(obj.photo_data) > 10)
        self.assertTrue(len(obj.ijazah_data) > 10)
