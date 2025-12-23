from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .forms import CustomUserCreationForm, LoginForm
import random
from django.core.mail import send_mail
from django.conf import settings
from .models import User


def index(request):
    return render(request, 'index.html')



def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Selamat datang, {user.nama_lengkap}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Email atau password salah")
        else:
            # Check for captcha errors specifically
            if 'captcha' in form.errors:
                 messages.error(request, "Kode Captcha salah")
            
            # Check for other errors
            if 'email' in form.errors or 'password' in form.errors:
                 messages.error(request, "Format email atau password tidak valid")

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            
            # Save data to session (don't save to DB yet)
            # We save the form instance temporarily using commit=False to get the model with hashed password
            user = form.save(commit=False)
            
            # Store essential data in session
            request.session['register_data'] = {
                'nama_lengkap': user.nama_lengkap,
                'email': user.email,
                'password': user.password, # This is already hashed by UserCreationForm
            }
            request.session['otp'] = otp
            
            # Send Email
            subject = 'Kode Verifikasi Registrasi MaesaanAK1'
            message = f'Halo {user.nama_lengkap},\n\nKode verifikasi (OTP) Anda adalah: {otp}\n\nJangan berikan kode ini kepada siapapun.'
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@maesaan.com',
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, f"Kode OTP telah dikirim ke {user.email}. Silakan cek inbox/spam.")
                return redirect('verify_otp')
            except Exception as e:
                messages.error(request, f"Gagal mengirim email: {e}")
                # For development fallback/debugging
                print(f"DEV OTP: {otp}") 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def verify_otp(request):
    if 'register_data' not in request.session:
        messages.error(request, "Sesi registrasi berakhir. Silakan daftar ulang.")
        return redirect('register')
    
    if request.method == 'POST':
        input_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        
        if input_otp == session_otp:
            # OTP Valid, Create User
            data = request.session['register_data']
            
            # Create user object
            user = User(
                nama_lengkap=data['nama_lengkap'],
                email=data['email'],
                password=data['password'],
                is_active=True
            )
            user.save()
            
            # Login
            login(request, user)
            
            # Clear session
            del request.session['register_data']
            del request.session['otp']
            
            messages.success(request, "Registrasi Berhasil! Selamat datang.")
            return redirect('dashboard')
        else:
            messages.error(request, "Kode OTP salah! Silakan coba lagi.")
    
    return render(request, 'accounts/verify_otp.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah logout dari sistem.")
    return redirect('index')

@login_required
def dashboard(request):
    # Get user's AK1 registration status
    try:
        pendaftaran = request.user.pendaftaranak1_set.first()
        status = pendaftaran.status if pendaftaran else None
    except:
        status = None

    context = {
        'user': request.user,
        'status': status,
        'pendaftaran': pendaftaran if 'pendaftaran' in locals() else None
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profil(request):
    if request.method == 'POST':
        # Handle profile update
        nama_lengkap = request.POST.get('nama_lengkap')
        email = request.POST.get('email')

        if nama_lengkap and email:
            request.user.nama_lengkap = nama_lengkap
            request.user.email = email
            request.user.save()
            messages.success(request, "Profil berhasil diperbarui!")
        else:
            messages.error(request, "Semua field harus diisi!")

    return render(request, 'accounts/profil.html')
