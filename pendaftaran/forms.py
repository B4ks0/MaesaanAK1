from django import forms
from .models import PendaftaranAK1

class PendaftaranAK1Form(forms.ModelForm):
    ktp = forms.FileField(required=False, label="KTP")
    photo = forms.FileField(required=False, label="Foto")
    ijazah = forms.FileField(required=False, label="Ijazah")

    class Meta:
        model = PendaftaranAK1
        fields = [
            'nik', 'nama', 'ttl', 'jk', 'status_perkawinan',
            'pendidikan', 'agama', 'alamat', 'keahlian', 'pengalaman'
        ]
        widgets = {
            'ttl': forms.DateInput(attrs={'type': 'date'}),
            'alamat': forms.Textarea(attrs={'rows': 3}),
            'keahlian': forms.Textarea(attrs={'rows': 2}),
            'pengalaman': forms.Textarea(attrs={'rows': 3}),
        }
