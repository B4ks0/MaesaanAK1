from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from pendaftaran.models import PendaftaranAK1
from django.utils import timezone

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    registrations = PendaftaranAK1.objects.all().order_by('-created_at')
    context = {
        'registrations': registrations,
    }
    return render(request, 'adminpanel/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def verify_registration(request, registration_id):
    registration = get_object_or_404(PendaftaranAK1, id=registration_id)

    if request.method == 'POST':
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"POST data received: {dict(request.POST)}")
        
        action = request.POST.get('action', '').strip()
        comment = request.POST.get('comment', '').strip()
        
        logger.info(f"Adminpanel verify action: '{action}' (length: {len(action)}) for registration {registration_id} by {request.user}")
        
        try:
            if action == 'approve':
                registration.status = 'diverifikasi'
                registration.verified_at = timezone.now()
                registration.reviewed_at = timezone.now()
                registration.reviewed_by = request.user
                registration.review_comment = comment if comment else 'Disetujui'
                registration.save()
                messages.success(request, f"✓ Pendaftaran {registration.nama} telah DISETUJUI. Kartu AK1 dapat diunduh.")
                logger.info(f"Approval completed for registration {registration_id}")
            elif action == 'reject':
                registration.status = 'ditolak'
                registration.reviewed_at = timezone.now()
                registration.reviewed_by = request.user
                registration.review_comment = comment if comment else 'Ditolak oleh petugas'
                registration.save()
                messages.success(request, f"✓ Pendaftaran {registration.nama} telah DITOLAK.")
                logger.info(f"Rejection completed for registration {registration_id}")
            else:
                messages.error(request, f"Aksi tidak valid: {action}")
                logger.warning(f"Invalid action received: {action}")
                return render(request, 'adminpanel/verify_registration.html', {'registration': registration})
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {str(e)}")
            logger.error(f"Error processing verification: {str(e)}", exc_info=True)
            return render(request, 'adminpanel/verify_registration.html', {'registration': registration})

        return redirect('admin_dashboard')

    context = {
        'registration': registration,
    }
    return render(request, 'adminpanel/verify_registration.html', context)
