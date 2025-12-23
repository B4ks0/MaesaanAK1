from django import forms
from pendaftaran.models import PendaftaranAK1


class KTPUploadForm(forms.Form):
    """Form untuk upload KTP dan auto-fill data"""
    ktp_image = forms.ImageField(
        label="Unggah Foto KTP",
        help_text="Format: JPG, PNG (Ukuran maksimal: 5MB)",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
        })
    )


class PendaftaranAK1KTPForm(forms.ModelForm):
    """Extended form untuk Pendaftaran AK1 dengan field auto-fill dari KTP"""
    ktp = forms.FileField(required=False, label="KTP")
    photo = forms.FileField(required=False, label="Foto")
    ijazah = forms.FileField(required=False, label="Ijazah")

    class Meta:
        model = PendaftaranAK1
        fields = [
            'nik', 'nama', 'ttl', 'jk', 'status_perkawinan',
            'pendidikan', 'alamat', 'keahlian', 'pengalaman'
        ]
        widgets = {
            'nik': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nomor NIK 16 digit',
                'readonly': 'readonly'
            }),
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Lengkap',
                'readonly': 'readonly'
            }),
            'ttl': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tempat, DD-MM-YYYY',
                'readonly': 'readonly'
            }),
            'jk': forms.Select(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'status_perkawinan': forms.Select(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'pendidikan': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pendidikan terakhir (opsional)',
            }),
            'alamat': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Alamat lengkap',
                'readonly': 'readonly'
            }),
            'keahlian': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Keahlian/Skills',
            }),
            'pengalaman': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Pengalaman kerja',
            }),
        }
