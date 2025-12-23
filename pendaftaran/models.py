from django.db import models
from accounts.models import User

class PendaftaranAK1(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('diverifikasi', 'Diverifikasi'),
        ('ditolak', 'Ditolak'),
    ]

    JK_CHOICES = [
        ('LAKI-LAKI', 'Laki-Laki'),
        ('PEREMPUAN', 'Perempuan'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('BELUM KAWIN', 'Belum Kawin'),
        ('KAWIN', 'Kawin'),
        ('CERAI HIDUP', 'Cerai Hidup'),
        ('CERAI MATI', 'Cerai Mati'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nik = models.CharField(max_length=16, unique=True)
    nama = models.CharField(max_length=255)
    ttl = models.CharField(max_length=255)  # Tempat Tanggal Lahir
    jk = models.CharField(max_length=10, choices=JK_CHOICES)
    status_perkawinan = models.CharField(max_length=15, choices=MARITAL_STATUS_CHOICES)
    pendidikan = models.CharField(max_length=50, blank=True, null=True)
    agama = models.CharField(max_length=50, blank=True, null=True)
    alamat = models.TextField()
    keahlian = models.CharField(max_length=255, blank=True, null=True)
    pengalaman = models.TextField(blank=True, null=True)
    ktp_data = models.TextField(blank=True, null=True)  # Base64 encoded KTP image
    photo_data = models.TextField(blank=True, null=True)  # Base64 encoded image
    ijazah_data = models.TextField(blank=True, null=True)  # Base64 encoded document
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    verified_at = models.DateTimeField(blank=True, null=True)
    # Review fields: reviewer, comment and review timestamp
    review_comment = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='pendaftaran_reviewed')
    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pendaftaran AK1 - {self.nama} ({self.nik})"
