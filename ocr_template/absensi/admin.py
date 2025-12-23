from django.contrib import admin
from .models import AbsensiTamu


@admin.register(AbsensiTamu)
class AbsensiTamuAdmin(admin.ModelAdmin):
    list_display = ['nama', 'instansi', 'keperluan', 'tanggal_waktu']
    list_filter = ['tanggal_waktu']
    search_fields = ['nama', 'instansi', 'keperluan']
    readonly_fields = ['tanggal_waktu']

