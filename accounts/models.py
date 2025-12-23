from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, nama_lengkap, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, nama_lengkap=nama_lengkap, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nama_lengkap, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nama_lengkap, password, **extra_fields)

class User(AbstractUser):
    nama_lengkap = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    # Override the username field to use email as username
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nama_lengkap']

    def __str__(self):
        return self.nama_lengkap
