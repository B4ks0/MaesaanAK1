from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from captcha.fields import CaptchaField

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ("nama_lengkap", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan email Anda'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan password Anda'})
    )
    captcha = CaptchaField()
