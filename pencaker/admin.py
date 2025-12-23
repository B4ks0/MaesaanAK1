from django.contrib import admin
from pendaftaran.models import PendaftaranAK1


@admin.register(PendaftaranAK1)
class PendaftaranAK1Admin(admin.ModelAdmin):
    list_display = ('nik', 'nama', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('nik', 'nama', 'user__email')
    readonly_fields = ('created_at', 'verified_at')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Data KTP', {
            'fields': ('nik', 'nama', 'ttl', 'jk', 'status_perkawinan', 'alamat', 'agama'),
            'classes': ('collapse',)
        }),
        ('Data Tambahan', {
            'fields': ('pendidikan', 'keahlian', 'pengalaman'),
            'classes': ('collapse',)
        }),
        ('Documents', {
            'fields': ('ktp_data', 'photo_data', 'ijazah_data'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'verified_at'),
        }),
    )
