# Implementation Summary: Admin Review & PDF Download

## Changes Made

### 1. Model Update (`pendaftaran/models.py`)
- Added `agama` field (max_length=50, optional)
- Added `review_comment` field (TextField for admin comments during rejection/approval)
- Added `reviewed_by` ForeignKey pointing to User (staff who reviewed)
- Added `reviewed_at` DateTimeField (when the review was done)

### 2. Form Update (`pendaftaran/forms.py`)
- Added `agama` to the form fields so users can input religion during registration

### 3. URLs Added (`pendaftaran/urls.py`)
- `pendaftaran-list/` → `list_pendaftaran` (admin view all registrations)
- `pendaftaran/<id>/review/` → `review_pendaftaran` (admin review & approve/reject)
- `pendaftaran/<id>/download-pdf/` → `download_kartu_pdf` (generate PDF card)

### 4. New Views (`pendaftaran/views.py`)

#### `list_pendaftaran(request)` - Admin Only
- Lists all registrations with NIK, nama, status, and action links
- Permission check: `if not request.user.is_staff` returns 403

#### `review_pendaftaran(request, pk)` - Admin Only
- Shows registration details with KTP preview
- Form with "Setujui" (Approve) and "Tolak" (Reject) buttons
- Optional comment field (for rejection reasons or notes)
- On approval: status → 'diverifikasi', sets verified_at, reviewed_at, reviewed_by
- On rejection: status → 'ditolak', records reviewer and comment
- Permission check: admin/staff only

#### `download_kartu_pdf(request, pk)` - User or Admin
- Generates PDF "Kartu Tanda Bukti Pendaftaran Pencari Kerja"
- Shows: NIK, nama, TTL, jenis kelamin, status perkawinan, agama, alamat
- Only available if status == 'diverifikasi'
- Permission: owner (user who registered) or staff
- Returns PDF as downloadable attachment

### 5. Templates Created

#### `list_pendaftaran.html`
- Admin table: NIK, Nama, Status, Waktu Daftar
- Review button for each row
- Download PDF button (only if approved)

#### `review_pendaftaran.html`
- Shows all registration details
- KTP image preview (if uploaded)
- Comment textarea for admin notes
- Approve & Reject buttons
- Download PDF button (if already approved)

#### Updated `status_pendaftaran.html`
- Added "Unduh PDF Kartu" button for approved users
- Links to download their PDF card

### 6. Dependencies Installed
- `reportlab` - for PDF generation (Canvas, A4 page size)

## How to Use

### Admin Workflow
1. Go to `/pendaftaran-list/` (admin only)
2. Click "Review" on any registration
3. Examine the data and KTP preview
4. Enter optional comment
5. Click "Setujui" to approve or "Tolak" to reject
6. If approved, download button appears for the PDF

### User Workflow
1. User registers at `/pendaftaran-ak1/` with form (including agama field now)
2. User checks status at `/status-pendaftaran/`
3. If admin approves, user sees "Unduh PDF Kartu" button
4. User clicks to download PDF with their registration data

### PDF Content
The PDF card automatically includes:
- NIK (16 digits)
- Nama Lengkap (full name)
- Tempat Tanggal Lahir (place/date of birth)
- Jenis Kelamin (gender)
- Status Perkawinan (marital status)
- Agama (religion)
- Alamat (address)
- Tanggal Diterbitkan (issued date from verified_at)

## Database Changes
Run these to apply changes:
```bash
python manage.py makemigrations pendaftaran
python manage.py migrate pendaftaran
```
✓ Already executed above - migration applied successfully.

## Installation Note
`reportlab` was already installed. If needed in the future, install with:
```bash
pip install reportlab
```

## Next Steps (Optional Enhancements)
- Add email notifications when status changes (approved/rejected)
- Add file size limits and validation on PDF generation
- Add pagination to the admin list for large number of registrations
- Add filters (by status, date range) to admin list
- Add digital signature field on PDF (placeholder for admin signature)
- Add watermark or QR code to PDF for verification
