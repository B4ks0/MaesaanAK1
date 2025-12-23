# Admin Review & PDF Download Guide

## Admin Workflow

### Step 1: View All Pending Registrations
1. Go to `/pendaftaran-list/` (Admin only)
2. See all registrations sorted by newest first
3. Status indicators show:
   - **Menunggu** (yellow) - Pending approval
   - **Disetujui** (green) - Approved
   - **Ditolak** (red) - Rejected

### Step 2: Review Individual Registration
1. Click **Review** button on any registration
2. View complete registrant information:
   - NIK, Nama Lengkap, TTL, Jenis Kelamin
   - Status Perkawinan, Agama, Alamat
   - Keahlian, Pengalaman, Pendidikan
3. See KTP image preview
4. See photo preview (if uploaded)

### Step 3: Make Decision
Choose one of three actions:

#### Option A: SETUJUI (Approve)
1. Click **SETUJUI / APPROVE** button
2. (Optional) Add comment in the text area
3. System automatically:
   - Changes status to "Diverifikasi" (Approved)
   - Records approval timestamp
   - Stores reviewer name
   - Generates AK1 card data
4. Confirmation message shows

#### Option B: TOLAK (Reject)
1. Click **TOLAK / REJECT** button
2. **MUST** add reason/comment in text area
3. System automatically:
   - Changes status to "Ditolak" (Rejected)
   - Records rejection timestamp
   - Stores reviewer name and comment
4. User sees rejection reason

#### Option C: Kembali (Back)
- Go back to list without making changes

### Step 4: Download AK1 Card (After Approval)
**Only available for approved registrations**

1. After approving, click **Download Kartu AK1** button
2. File downloads as: `AK1_Kartu_Kuning_{NIK}.pdf`
3. PDF shows:
   - Official "Kartu Tanda Bukti Pendaftaran Pencari Kerja"
   - Yellow background (Kartu Kuning)
   - All registrant data
   - Signature area for official stamp
   - Issue date
   - Footer: "Berlaku tanpa batas waktu"

## AK1 Card Format (PDF)

The generated PDF card (Kartu Kuning) includes:

```
KEMENTERIAN KETENAGAKERJAAN
KARTU TANDA BUKTI PENDAFTARAN PENCARI KERJA
                    AK.1

NIK                    : 3170395928750031
Nama Lengkap          : Ahmad Surya
Tempat / Tanggal Lahir : Jakarta, 15-05-1990
Jenis Kelamin         : LAKI-LAKI
Status Perkawinan     : KAWIN
Agama                 : ISLAM
Alamat                : Jl. Merdeka No. 123, Jakarta

Tanggal Terbit: 21-11-2025
Petugas: ________________

Kartu ini adalah bukti resmi pendaftaran pencari kerja
- Berlaku tanpa batas waktu
```

## User Access After Approval

Once approved, users can:
1. See "Approved" status in their dashboard
2. Click "Unduh PDF Kartu" button to download AK1 card
3. Download can be done multiple times
4. Card always shows current verified data

## Review Statistics

Admin list shows real-time counts:
- **Pending**: How many awaiting review
- **Diverifikasi**: How many approved
- **Ditolak**: How many rejected

## Features

✓ Automatic status tracking
✓ Timestamp recording (who, when)
✓ Comment storage for rejections
✓ Professional PDF card generation
✓ Yellow "Kartu Kuning" styling
✓ Permission-based access
✓ Downloadable for both admin and user (after approval)

## Troubleshooting

**Problem**: Cannot see Approve/Reject buttons
- Solution: Make sure you're logged in as admin/staff user

**Problem**: PDF download doesn't work
- Solution: Only available after status is "Diverifikasi"
- Verify verified_at field is populated in database

**Problem**: PDF looks wrong
- Solution: Ensure registrant has all data filled in
- Empty fields show as "-" in PDF

## Database Fields

When reviewing, these fields are automatically updated:

- `status` → Set to 'diverifikasi' or 'ditolak'
- `reviewed_at` → Current timestamp
- `reviewed_by` → Current admin user
- `review_comment` → Admin's comment
- `verified_at` → Approval timestamp (if approved)

## Direct Admin URL

Access admin review page directly:
```
/pendaftaran-list/              → All registrations
/pendaftaran/{id}/review/       → Review specific registration
/pendaftaran/{id}/download-pdf/ → Download AK1 PDF
```

## Tips for Admins

1. **Always add comments when rejecting** - Users need to know why
2. **Review KTP image carefully** - Verify data matches documents
3. **Check for duplicate NIKs** - System allows multiple registrations per person
4. **Use comments for other notes** - Even for approvals (notes for record)
5. **Download PDF for records** - Keep copies for your files
6. **Review photo closely** - Ensure proper ID photo quality if required

## Keyboard Shortcuts (HTML Form)

- `Tab` → Move between fields
- `Ctrl+Enter` → Submit form (if javascript enabled)
- Standard browser shortcuts for copying/pasting comments
