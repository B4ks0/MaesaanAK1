from django import forms
from .models import AbsensiTamu


class AbsensiForm(forms.ModelForm):
    class Meta:
        model = AbsensiTamu
        fields = ['nama', 'instansi', 'keperluan']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama lengkap',
                'required': True
            }),
            'instansi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan instansi/perusahaan'
            }),
            'keperluan': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan keperluan kunjungan',
                'rows': 3,
                'required': True
            }),
        }
        labels = {
            'nama': 'Nama Lengkap',
            'instansi': 'Instansi/Perusahaan',
            'keperluan': 'Keperluan',
        }


class DateRangeForm(forms.Form):
    tanggal_mulai = forms.DateField(
        label='Tanggal Mulai',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'required': True
        })
    )
    tanggal_akhir = forms.DateField(
        label='Tanggal Akhir',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'required': True
        })
    )
