#!/usr/bin/env python
import os
import sys
import django
import random
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ak1.settings')
django.setup()

from accounts.models import User
from pendaftaran.models import PendaftaranAK1

def create_dummy_data():
    try:
        # Dummy user data
        users_data = [
            {'nama_lengkap': 'Ahmad Surya', 'email': 'ahmad.surya@example.com'},
            {'nama_lengkap': 'Siti Nurhaliza', 'email': 'siti.nurhaliza@example.com'},
            {'nama_lengkap': 'Budi Santoso', 'email': 'budi.santoso@example.com'},
            {'nama_lengkap': 'Dewi Kartika', 'email': 'dewi.kartika@example.com'},
            {'nama_lengkap': 'Rudi Hartono', 'email': 'rudi.hartono@example.com'},
            {'nama_lengkap': 'Maya Sari', 'email': 'maya.sari@example.com'},
            {'nama_lengkap': 'Agus Prasetyo', 'email': 'agus.prasetyo@example.com'},
            {'nama_lengkap': 'Lina Marlina', 'email': 'lina.marlina@example.com'},
        ]

        # Create users
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'nama_lengkap': user_data['nama_lengkap'],
                    'password': 'password123'  # Set a default password
                }
            )
            if created:
                user.set_password('password123')  # Hash the password
                user.save()
            users.append(user)

        print(f"Created {len(users)} users.")

        # Dummy registration data
        statuses = ['pending', 'diverifikasi', 'ditolak']
        jk_choices = ['LAKI-LAKI', 'PEREMPUAN']
        marital_statuses = ['BELUM KAWIN', 'KAWIN', 'CERAI HIDUP', 'CERAI MATI']
        pendidikan_options = ['SMA', 'D3', 'S1', 'S2', None]
        keahlian_options = ['Komputer', 'Administrasi', 'Teknik Sipil', 'Akuntansi', None]
        pengalaman_options = ['2 tahun di bidang IT', '5 tahun sebagai admin', 'Pengalaman 3 tahun di konstruksi', None]

        # Indonesian addresses (focusing on Minahasa area)
        addresses = [
            'Jl. Raya Manado, Tomohon',
            'Jl. Sam Ratulangi, Tondano',
            'Jl. Wolter Monginsidi, Amurang',
            'Jl. Diponegoro, Bitung',
            'Jl. Sudirman, Kotamobagu',
        ]

        # Create registrations
        registrations_created = 0
        for user in users:
            num_registrations = random.randint(1, 2)  # 1 or 2 per user
            for _ in range(num_registrations):
                nik = ''.join([str(random.randint(0, 9)) for _ in range(16)])
                nama = user.nama_lengkap
                ttl = f"{random.choice(['Manado', 'Tomohon', 'Tondano', 'Amurang'])}, {random.randint(1, 31)}-{random.randint(1, 12)}-{random.randint(1980, 2000)}"
                jk = random.choice(jk_choices)
                status_perkawinan = random.choice(marital_statuses)
                pendidikan = random.choice(pendidikan_options)
                alamat = random.choice(addresses)
                keahlian = random.choice(keahlian_options)
                pengalaman = random.choice(pengalaman_options)
                status = random.choice(statuses)
                verified_at = None if status == 'pending' else datetime.now() - timedelta(days=random.randint(1, 30))

                PendaftaranAK1.objects.create(
                    user=user,
                    nik=nik,
                    nama=nama,
                    ttl=ttl,
                    jk=jk,
                    status_perkawinan=status_perkawinan,
                    pendidikan=pendidikan,
                    alamat=alamat,
                    keahlian=keahlian,
                    pengalaman=pengalaman,
                    status=status,
                    verified_at=verified_at,
                )
                registrations_created += 1

        print(f"Created {registrations_created} dummy registrations.")
        print("Dummy data population completed successfully!")

    except Exception as e:
        print(f"Error populating dummy data: {e}")

if __name__ == '__main__':
    create_dummy_data()
