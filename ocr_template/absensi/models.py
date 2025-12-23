from django.db import models
from django.utils import timezone


class AbsensiTamu(models.Model):
    nama = models.CharField(max_length=100)
    instansi = models.CharField(max_length=200, blank=True, null=True)
    keperluan = models.TextField()
    tanggal_waktu = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-tanggal_waktu']
        verbose_name = 'Absensi Tamu'
        verbose_name_plural = 'Data Absensi Tamu'
    
    def __str__(self):
        return f"{self.nama} - {self.instansi or 'Tidak ada instansi'}"

