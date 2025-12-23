#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ak1.settings')
django.setup()

from accounts.models import User

def create_superuser():
    try:
        # Check if superuser already exists
        if User.objects.filter(email='admin@maesaan.com').exists():
            print("Superuser already exists!")
            return

        # Create superuser
        user = User.objects.create_superuser(
            email='admin@maesaan.com',
            nama_lengkap='Administrator',
            password='admin123'
        )

        print("Superuser created successfully!")
        print(f"Email: {user.email}")
        print(f"Name: {user.nama_lengkap}")
        print("Password: admin123")

    except Exception as e:
        print(f"Error creating superuser: {e}")

if __name__ == '__main__':
    create_superuser()
