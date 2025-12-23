from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .forms import CustomUserCreationForm

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Email dan password harus diisi")
            return render(request, 'accounts/login.html')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Selamat datang, {user.nama_lengkap}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Email atau password salah")

    return render(request, 'accounts/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Akun berhasil dibuat! Selamat datang di MAESAAN.")
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

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
