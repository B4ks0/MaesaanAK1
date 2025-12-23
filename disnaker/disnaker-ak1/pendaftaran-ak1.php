<?php
require_once 'config/init.php';
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form Kartu AK1 - OCR Scanner</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tesseract.js/4.1.1/tesseract.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        /* Override navbar padding when present */
        body.has-navbar {
            padding-top: 0;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            backdrop-filter: blur(10px);
        }

        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h2 {
            font-size: 2.2em;
            margin-bottom: 10px;
            font-weight: 300;
        }

        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }

        .form-container {
            padding: 40px;
        }

        .ocr-section {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 25px rgba(250, 112, 154, 0.3);
        }

        .ocr-section h3 {
            margin-bottom: 15px;
            font-size: 1.5em;
            font-weight: 400;
        }

        .camera-section {
            display: none;
            margin: 20px 0;
        }

        #video {
            width: 100%;
            max-width: 400px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            margin: 5px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }

        .btn-scan {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        }

        .btn-upload {
            background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .form-group {
            margin-bottom: 25px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
            font-size: 1em;
        }

        .form-group input,
        .form-group textarea,
        .form-group select {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            transition: all 0.3s ease;
            background: white;
        }

        .form-group input:focus,
        .form-group textarea:focus,
        .form-group select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            transform: translateY(-1px);
        }

        .form-group textarea {
            resize: vertical;
            min-height: 100px;
        }

        .btn-submit {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1.2em;
            width: 100%;
            margin-top: 20px;
            transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(17, 153, 142, 0.3);
        }

        .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(17, 153, 142, 0.4);
        }

        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .error {
            color: #e74c3c;
            text-align: center;
            margin: 10px 0;
            padding: 10px;
            background: rgba(231, 76, 60, 0.1);
            border-radius: 5px;
        }

        .success {
            color: #27ae60;
            text-align: center;
            margin: 10px 0;
            padding: 10px;
            background: rgba(39, 174, 96, 0.1);
            border-radius: 5px;
        }

        .canvas-container {
            display: none;
            margin: 20px 0;
            text-align: center;
        }

        #canvas {
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        #fileInput {
            display: none;
        }

        .file-upload-area {
            border: 2px dashed #ccc;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 15px 0;
        }

        .file-upload-area:hover {
            border-color: #667eea;
            background: rgba(102, 126, 234, 0.05);
        }

        .file-upload-area.dragover {
            border-color: #667eea;
            background: rgba(102, 126, 234, 0.1);
        }

        .photo-section {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            text-align: center;
            color: #333;
            box-shadow: 0 10px 25px rgba(168, 237, 234, 0.3);
        }

        .photo-section h3 {
            margin-bottom: 15px;
            font-size: 1.5em;
            font-weight: 400;
        }

        .photo-upload-container {
            margin: 20px 0;
        }

        .photo-upload-area {
            border: 2px dashed #ccc;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 15px 0;
            min-height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .photo-upload-area:hover {
            border-color: #667eea;
            background: rgba(102, 126, 234, 0.05);
        }

        .photo-upload-area.dragover {
            border-color: #667eea;
            background: rgba(102, 126, 234, 0.1);
        }

        .photo-preview-img {
            max-width: 150px;
            max-height: 200px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            object-fit: cover;
        }

        #photoInput {
            display: none;
        }

        .document-section {
            background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            text-align: center;
            color: #333;
            box-shadow: 0 10px 25px rgba(129, 199, 132, 0.3);
        }

        .document-section h3 {
            margin-bottom: 15px;
            font-size: 1.5em;
            font-weight: 400;
        }

        .document-upload-container {
            margin: 20px 0;
        }

        .document-upload-area {
            border: 2px dashed #81c784;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 15px 0;
            min-height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .document-upload-area:hover {
            border-color: #4caf50;
            background: rgba(76, 175, 80, 0.05);
        }

        .document-upload-area.dragover {
            border-color: #4caf50;
            background: rgba(76, 175, 80, 0.1);
        }

        .document-preview {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }

        .document-preview-img {
            max-width: 200px;
            max-height: 150px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            object-fit: cover;
        }

        .pdf-preview {
            width: 80px;
            height: 80px;
            background: #e74c3c;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5em;
            font-weight: bold;
        }

        .document-info {
            background: rgba(255, 255, 255, 0.9);
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 0.9em;
            color: #333;
            margin-top: 10px;
        }

        #ijazahInput {
            display: none;
        }

        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 15px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h2 {
                font-size: 1.8em;
            }
            
            .form-container {
                padding: 20px;
            }
            
            .form-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <?php 
    // Include navbar if files exist
    if (file_exists('includes/navbar.php')) {
        include 'includes/navbar.php'; 
        echo '<script>document.body.classList.add("has-navbar");</script>';
    }
    
    if (file_exists('includes/breadcrumb.php')) {
        include 'includes/breadcrumb.php'; 
    }
    ?>
    
    <div class="container">
        <div class="header">
            <h2>📋 Formulir Kartu AK1</h2>
            <p>Sistem Pendaftaran dengan Teknologi OCR Scanner</p>
        </div>

        <div class="form-container">
            <div class="ocr-section">
                <h3>🔍 Scan KTP Otomatis</h3>
                <p>Gunakan kamera atau upload foto KTP untuk mengisi form secara otomatis</p>
                
                <div style="margin: 20px 0;">
                    <button class="btn btn-scan" onclick="startCamera()">📷 Buka Kamera</button>
                    <button class="btn btn-upload" onclick="document.getElementById('fileInput').click()">📁 Upload Foto KTP</button>
                </div>

                <input type="file" id="fileInput" accept="image/*" onchange="handleFileSelect(event)">
                
                <div class="file-upload-area" onclick="document.getElementById('fileInput').click()" ondrop="handleDrop(event)" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)">
                    <p>🖼️ Drag & Drop foto KTP di sini atau klik untuk memilih file</p>
                </div>

                <div class="camera-section" id="cameraSection">
                    <video id="video" autoplay></video><br>
                    <button class="btn" onclick="captureImage()">📸 Ambil Foto</button>
                    <button class="btn" onclick="stopCamera()">❌ Tutup Kamera</button>
                </div>

                <div class="canvas-container" id="canvasContainer">
                    <canvas id="canvas"></canvas><br>
                    <button class="btn" onclick="processImage()">🔍 Proses OCR</button>
                    <button class="btn" onclick="retakePhoto()">🔄 Foto Ulang</button>
                </div>

                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Sedang memproses gambar...</p>
                </div>

                <div id="ocrResult"></div>
            </div>

            <!-- Pas Foto Section -->
            <div class="photo-section">
                <h3>📷 Upload Pas Foto 3x4</h3>
                <p>Upload pas foto dengan ukuran 3x4 cm (maksimal 2MB)</p>
                
                <div class="photo-upload-container">
                    <input type="file" id="photoInput" accept="image/*" onchange="handlePhotoSelect(event)">
                    
                    <div class="photo-upload-area" onclick="document.getElementById('photoInput').click()" ondrop="handlePhotoDrop(event)" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)">
                        <div id="photoPreview">
                            <p>📸 Drag & Drop pas foto di sini atau klik untuk memilih file</p>
                            <small>Format: JPG, PNG, JPEG | Maksimal: 2MB</small>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Ijazah Section -->
            <div class="document-section">
                <h3>📜 Upload Ijazah / Sertifikat</h3>
                <p>Upload ijazah atau sertifikat pendidikan terakhir (maksimal 5MB)</p>
                
                <div class="document-upload-container">
                    <input type="file" id="ijazahInput" accept="image/*,application/pdf" onchange="handleIjazahSelect(event)">
                    
                    <div class="document-upload-area" onclick="document.getElementById('ijazahInput').click()" ondrop="handleIjazahDrop(event)" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)">
                        <div id="ijazahPreview">
                            <p>📄 Drag & Drop ijazah di sini atau klik untuk memilih file</p>
                            <small>Format: JPG, PNG, JPEG, PDF | Maksimal: 5MB</small>
                        </div>
                    </div>
                </div>
            </div>

            <form action="process_form.php" method="POST" id="ak1Form" enctype="multipart/form-data">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="nik">📄 NIK</label>
                        <input type="text" id="nik" name="nik" placeholder="Nomor Induk Kependudukan" maxlength="16" required>
                    </div>

                    <div class="form-group">
                        <label for="nama">👤 Nama Lengkap</label>
                        <input type="text" id="nama" name="nama" placeholder="Nama sesuai KTP" required>
                    </div>

                    <div class="form-group">
                        <label for="ttl">📅 Tempat, Tanggal Lahir</label>
                        <input type="text" id="ttl" name="ttl" placeholder="Kota, DD-MM-YYYY" required>
                    </div>

                    <div class="form-group">
                        <label for="jk">⚥ Jenis Kelamin</label>
                        <select id="jk" name="jk" required>
                            <option value="">Pilih Jenis Kelamin</option>
                            <option value="LAKI-LAKI">Laki-laki</option>
                            <option value="PEREMPUAN">Perempuan</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="status">💍 Status Perkawinan</label>
                        <select id="status" name="status">
                            <option value="">Pilih Status</option>
                            <option value="BELUM KAWIN">Belum Kawin</option>
                            <option value="KAWIN">Kawin</option>
                            <option value="CERAI HIDUP">Cerai Hidup</option>
                            <option value="CERAI MATI">Cerai Mati</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="pendidikan">🎓 Pendidikan Terakhir</label>
                        <select id="pendidikan" name="pendidikan">
                            <option value="">Pilih Pendidikan</option>
                            <option value="SD">SD / Sederajat</option>
                            <option value="SMP">SMP / Sederajat</option>
                            <option value="SMA">SMA / Sederajat</option>
                            <option value="D3">Diploma III</option>
                            <option value="S1">Sarjana (S1)</option>
                            <option value="S2">Magister (S2)</option>
                            <option value="S3">Doktor (S3)</option>
                        </select>
                    </div>
                </div>

                <div class="form-group">
                    <label for="alamat">🏠 Alamat Lengkap</label>
                    <textarea id="alamat" name="alamat" placeholder="Alamat sesuai KTP" rows="3" required></textarea>
                </div>

                <div class="form-group">
                    <label for="keahlian">🛠️ Keahlian / Skill</label>
                    <input type="text" id="keahlian" name="keahlian" placeholder="Masukkan keahlian yang dimiliki">
                </div>

                <div class="form-group">
                    <label for="pengalaman">💼 Pengalaman Kerja</label>
                    <textarea id="pengalaman" name="pengalaman" placeholder="Jelaskan pengalaman kerja" rows="3"></textarea>
                </div>

                <!-- Hidden input for photo and ijazah -->
                <input type="hidden" id="photoData" name="photo_data" value="">
                <input type="hidden" id="ijazahData" name="ijazah_data" value="">

                <button type="submit" class="btn-submit">✅ Buat Kartu AK1</button>
            </form>
        </div>
    </div>

    <script>
        let stream = null;
        let capturedImage = null;

        // Fungsi untuk memulai kamera
        async function startCamera() {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { 
                        width: { ideal: 1280 },
                        height: { ideal: 720 },
                        facingMode: 'environment' 
                    } 
                });
                document.getElementById('video').srcObject = stream;
                document.getElementById('cameraSection').style.display = 'block';
            } catch (err) {
                showError('Error mengakses kamera: ' + err.message);
            }
        }

        // Fungsi untuk menghentikan kamera
        function stopCamera() {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                stream = null;
            }
            document.getElementById('cameraSection').style.display = 'none';
        }

        // Fungsi untuk mengambil gambar dari kamera
        function captureImage() {
            const video = document.getElementById('video');
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            ctx.drawImage(video, 0, 0);
            capturedImage = canvas.toDataURL('image/png');

            document.getElementById('canvasContainer').style.display = 'block';
            stopCamera();
        }

        // Fungsi untuk foto ulang
        function retakePhoto() {
            document.getElementById('canvasContainer').style.display = 'none';
            capturedImage = null;
            startCamera();
        }

        // Fungsi untuk menangani upload ijazah
        function handleIjazahSelect(event) {
            const file = event.target.files[0];
            if (file) {
                // Validasi ukuran file (maksimal 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    showError('Ukuran file terlalu besar! Maksimal 5MB.');
                    return;
                }

                // Validasi tipe file
                if (!file.type.startsWith('image/') && file.type !== 'application/pdf') {
                    showError('File harus berupa gambar (JPG, PNG, JPEG) atau PDF!');
                    return;
                }

                const reader = new FileReader();
                reader.onload = function(e) {
                    displayIjazahPreview(e.target.result, file);
                    // Simpan data ijazah ke hidden input
                    document.getElementById('ijazahData').value = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        }

        // Fungsi untuk menampilkan preview ijazah
        function displayIjazahPreview(fileSrc, file) {
            const previewContainer = document.getElementById('ijazahPreview');
            const isPDF = file.type === 'application/pdf';
            
            if (isPDF) {
                previewContainer.innerHTML = `
                    <div class="document-preview">
                        <div class="pdf-preview">📄</div>
                        <div class="document-info">
                            <strong>${file.name}</strong><br>
                            <small>PDF Document - ${(file.size / (1024 * 1024)).toFixed(2)} MB</small>
                        </div>
                        <button type="button" class="btn" onclick="removeIjazah()" style="background: #e74c3c; margin-top: 10px;">🗑️ Hapus Ijazah</button>
                    </div>
                `;
            } else {
                previewContainer.innerHTML = `
                    <div class="document-preview">
                        <img src="${fileSrc}" alt="Ijazah Preview" class="document-preview-img">
                        <div class="document-info">
                            <strong>${file.name}</strong><br>
                            <small>${(file.size / (1024 * 1024)).toFixed(2)} MB</small>
                        </div>
                        <button type="button" class="btn" onclick="removeIjazah()" style="background: #e74c3c; margin-top: 10px;">🗑️ Hapus Ijazah</button>
                    </div>
                `;
            }
            showSuccess('Ijazah berhasil diupload!');
        }

        // Fungsi untuk menghapus ijazah
        function removeIjazah() {
            document.getElementById('ijazahPreview').innerHTML = `
                <p>📄 Drag & Drop ijazah di sini atau klik untuk memilih file</p>
                <small>Format: JPG, PNG, JPEG, PDF | Maksimal: 5MB</small>
            `;
            document.getElementById('ijazahInput').value = '';
            document.getElementById('ijazahData').value = '';
        }

        // Fungsi untuk drag and drop ijazah
        function handleIjazahDrop(event) {
            event.preventDefault();
            event.currentTarget.classList.remove('dragover');
            
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                const fileEvent = { target: { files: files } };
                handleIjazahSelect(fileEvent);
            }
        }

        // Fungsi untuk menangani upload pas foto
        function handlePhotoSelect(event) {
            const file = event.target.files[0];
            if (file) {
                // Validasi ukuran file (maksimal 2MB)
                if (file.size > 2 * 1024 * 1024) {
                    showError('Ukuran file terlalu besar! Maksimal 2MB.');
                    return;
                }

                // Validasi tipe file
                if (!file.type.startsWith('image/')) {
                    showError('File harus berupa gambar!');
                    return;
                }

                const reader = new FileReader();
                reader.onload = function(e) {
                    displayPhotoPreview(e.target.result);
                    // Simpan data foto ke hidden input
                    document.getElementById('photoData').value = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        }

        // Fungsi untuk menampilkan preview pas foto
        function displayPhotoPreview(imageSrc) {
            const previewContainer = document.getElementById('photoPreview');
            previewContainer.innerHTML = `
                <img src="${imageSrc}" alt="Pas Foto Preview" class="photo-preview-img">
                <br><br>
                <button type="button" class="btn" onclick="removePhoto()" style="background: #e74c3c;">🗑️ Hapus Foto</button>
            `;
            showSuccess('Pas foto berhasil diupload!');
        }

        // Fungsi untuk menghapus pas foto
        function removePhoto() {
            document.getElementById('photoPreview').innerHTML = `
                <p>📸 Drag & Drop pas foto di sini atau klik untuk memilih file</p>
                <small>Format: JPG, PNG, JPEG | Maksimal: 2MB</small>
            `;
            document.getElementById('photoInput').value = '';
            document.getElementById('photoData').value = '';
        }

        // Fungsi untuk drag and drop pas foto
        function handlePhotoDrop(event) {
            event.preventDefault();
            event.currentTarget.classList.remove('dragover');
            
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                const fileEvent = { target: { files: files } };
                handlePhotoSelect(fileEvent);
            }
        }

        // Fungsi untuk menangani file upload
        function handleFileSelect(event) {
            const file = event.target.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const img = new Image();
                    img.onload = function() {
                        const canvas = document.getElementById('canvas');
                        const ctx = canvas.getContext('2d');
                        
                        canvas.width = img.width;
                        canvas.height = img.height;
                        ctx.drawImage(img, 0, 0);
                        
                        capturedImage = canvas.toDataURL('image/png');
                        document.getElementById('canvasContainer').style.display = 'block';
                    };
                    img.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        }

        // Fungsi untuk drag and drop
        function handleDragOver(event) {
            event.preventDefault();
            event.currentTarget.classList.add('dragover');
        }

        function handleDragLeave(event) {
            event.currentTarget.classList.remove('dragover');
        }

        function handleDrop(event) {
            event.preventDefault();
            event.currentTarget.classList.remove('dragover');
            
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                const fileEvent = { target: { files: files } };
                handleFileSelect(fileEvent);
            }
        }

        // Fungsi untuk memproses gambar dengan OCR
        async function processImage() {
            if (!capturedImage) {
                showError('Tidak ada gambar yang akan diproses');
                return;
            }

            document.getElementById('loading').style.display = 'block';
            
            try {
                const result = await Tesseract.recognize(
                    capturedImage,
                    'ind',
                    {
                        logger: m => console.log(m)
                    }
                );

                const extractedText = result.data.text;
                console.log('OCR Result:', extractedText);
                
                // Parsing hasil OCR untuk mengisi form
                const extractedData = parseKTPData(extractedText);
                const filledFields = fillFormWithData(extractedData);
                
                document.getElementById('loading').style.display = 'none';
                
                if (filledFields > 0) {
                    showSuccess(`Data berhasil diproses! ${filledFields} field telah diisi otomatis.`);
                } else {
                    showError('Data tidak dapat diekstrak dengan baik. Silakan isi form secara manual.');
                }
                
            } catch (error) {
                console.error('OCR Error:', error);
                document.getElementById('loading').style.display = 'none';
                showError('Gagal memproses gambar. Pastikan foto KTP jelas dan coba lagi.');
            }
        }

        // Fungsi untuk parsing data KTP
        function parseKTPData(text) {
            console.log('Raw OCR Text:', text);
            
            const lines = text.split('\n').map(line => line.trim()).filter(line => line);
            console.log('Processed lines:', lines);
            
            let extractedData = {};

            // Pattern yang lebih fleksibel untuk NIK
            for (let line of lines) {
                // NIK biasanya 16 digit
                const nikMatch = line.match(/(\d{16})/);
                if (nikMatch) {
                    extractedData.nik = nikMatch[1];
                    console.log('Found NIK:', extractedData.nik);
                }
                
                // Nama - cari setelah kata "Nama" atau baris yang berisi huruf saja
                if (line.toLowerCase().includes('nama')) {
                    const namaMatch = line.match(/nama\s*[:\-]?\s*(.+)/i);
                    if (namaMatch && namaMatch[1].trim()) {
                        extractedData.nama = namaMatch[1].trim();
                        console.log('Found Nama:', extractedData.nama);
                    }
                }
                
                // Tempat Tanggal Lahir
                if (line.toLowerCase().includes('tempat') || line.toLowerCase().includes('lahir')) {
                    const ttlMatch = line.match(/(?:tempat.*lahir|lahir)\s*[:\-]?\s*(.+)/i);
                    if (ttlMatch && ttlMatch[1].trim()) {
                        extractedData.ttl = ttlMatch[1].trim();
                        console.log('Found TTL:', extractedData.ttl);
                    }
                }
                
                // Jenis Kelamin
                if (line.toLowerCase().includes('kelamin') || line.includes('LAKI-LAKI') || line.includes('PEREMPUAN')) {
                    if (line.includes('LAKI-LAKI')) {
                        extractedData.jk = 'LAKI-LAKI';
                    } else if (line.includes('PEREMPUAN')) {
                        extractedData.jk = 'PEREMPUAN';
                    }
                    console.log('Found JK:', extractedData.jk);
                }
                
                // Alamat
                if (line.toLowerCase().includes('alamat')) {
                    const alamatMatch = line.match(/alamat\s*[:\-]?\s*(.+)/i);
                    if (alamatMatch && alamatMatch[1].trim()) {
                        extractedData.alamat = alamatMatch[1].trim();
                        console.log('Found Alamat:', extractedData.alamat);
                    }
                }
                
                // Status Perkawinan
                if (line.toLowerCase().includes('kawin') || line.toLowerCase().includes('status')) {
                    const statusKeywords = ['BELUM KAWIN', 'KAWIN', 'CERAI HIDUP', 'CERAI MATI'];
                    for (let status of statusKeywords) {
                        if (line.includes(status)) {
                            extractedData.status = status;
                            console.log('Found Status:', extractedData.status);
                            break;
                        }
                    }
                }
            }

            // Fallback untuk nama jika tidak ditemukan dengan pattern di atas
            if (!extractedData.nama) {
                for (let line of lines) {
                    // Cari baris yang kemungkinan adalah nama (hanya huruf dan spasi, panjang wajar)
                    if (/^[A-Z\s]{3,50}$/.test(line) && 
                        !line.includes('REPUBLIK') && 
                        !line.includes('INDONESIA') && 
                        !line.includes('PROVINSI') &&
                        !line.includes('KOTA') &&
                        !line.includes('KABUPATEN')) {
                        extractedData.nama = line;
                        console.log('Fallback Nama:', extractedData.nama);
                        break;
                    }
                }
            }

            console.log('Final extracted data:', extractedData);
            return extractedData;
        }

        // Fungsi untuk mengisi form dengan data hasil OCR
        function fillFormWithData(data) {
            console.log('Filling form with data:', data);
            
            // Fungsi helper untuk mengisi field
            function fillField(fieldId, value) {
                if (value && value.trim()) {
                    const element = document.getElementById(fieldId);
                    if (element) {
                        element.value = value.trim();
                        // Animasi highlight
                        element.style.background = 'rgba(39, 174, 96, 0.1)';
                        element.style.borderColor = '#27ae60';
                        console.log(`Filled ${fieldId} with: ${value}`);
                        return true;
                    }
                }
                return false;
            }

            let filledCount = 0;
            
            // Isi semua field yang tersedia
            if (fillField('nik', data.nik)) filledCount++;
            if (fillField('nama', data.nama)) filledCount++;
            if (fillField('ttl', data.ttl)) filledCount++;
            if (fillField('alamat', data.alamat)) filledCount++;
            
            // Untuk dropdown, perlu penanganan khusus
            if (data.jk) {
                const jkElement = document.getElementById('jk');
                if (jkElement) {
                    jkElement.value = data.jk;
                    jkElement.style.background = 'rgba(39, 174, 96, 0.1)';
                    jkElement.style.borderColor = '#27ae60';
                    filledCount++;
                }
            }
            
            if (data.status) {
                const statusElement = document.getElementById('status');
                if (statusElement) {
                    statusElement.value = data.status;
                    statusElement.style.background = 'rgba(39, 174, 96, 0.1)';
                    statusElement.style.borderColor = '#27ae60';
                    filledCount++;
                }
            }

            // Reset highlight setelah 3 detik
            setTimeout(() => {
                const highlightedElements = document.querySelectorAll('#nik, #nama, #ttl, #jk, #status, #alamat');
                highlightedElements.forEach(element => {
                    element.style.background = 'white';
                    element.style.borderColor = '#e0e0e0';
                });
            }, 3000);

            console.log(`Successfully filled ${filledCount} fields`);
            return filledCount;
        }

        // Fungsi untuk menampilkan error
        function showError(message) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error';
            errorDiv.textContent = message;
            
            const existing = document.querySelector('.error');
            if (existing) existing.remove();
            
            document.getElementById('ocrResult').appendChild(errorDiv);
            
            setTimeout(() => {
                if (errorDiv.parentNode) {
                    errorDiv.parentNode.removeChild(errorDiv);
                }
            }, 5000);
        }

        // Fungsi untuk menampilkan success message
        function showSuccess(message) {
            const successDiv = document.createElement('div');
            successDiv.className = 'success';
            successDiv.textContent = message;
            
            const existing = document.querySelector('.success');
            if (existing) existing.remove();
            
            document.getElementById('ocrResult').appendChild(successDiv);
            
            setTimeout(() => {
                if (successDiv.parentNode) {
                    successDiv.parentNode.removeChild(successDiv);
                }
            }, 5000);
        }

        // Validasi form sebelum submit
        document.getElementById('ak1Form').addEventListener('submit', function(e) {
            const requiredFields = ['nik', 'nama', 'ttl', 'jk', 'alamat'];
            let isValid = true;
            
            requiredFields.forEach(field => {
                const element = document.getElementById(field);
                if (!element.value.trim()) {
                    element.style.borderColor = '#e74c3c';
                    isValid = false;
                } else {
                    element.style.borderColor = '#e0e0e0';
                }
            });
            
            // Validasi NIK (harus 16 digit)
            const nikValue = document.getElementById('nik').value;
            if (nikValue && !/^\d{16}$/.test(nikValue)) {
                document.getElementById('nik').style.borderColor = '#e74c3c';
                showError('NIK harus berisi 16 digit angka');
                isValid = false;
            }

            // Validasi pas foto dan ijazah (opsional, tapi berikan peringatan jika tidak ada)
            const photoData = document.getElementById('photoData').value;
            const ijazahData = document.getElementById('ijazahData').value;
            
            let missingDocs = [];
            if (!photoData) missingDocs.push('pas foto');
            if (!ijazahData) missingDocs.push('ijazah');
            
            if (missingDocs.length > 0) {
                const confirmSubmit = confirm(`Anda belum mengupload ${missingDocs.join(' dan ')}. Lanjutkan tanpa dokumen tersebut?`);
                if (!confirmSubmit) {
                    e.preventDefault();
                    return;
                }
            }
            
            if (!isValid) {
                e.preventDefault();
                showError('Mohon lengkapi semua field yang wajib diisi');
            } else {
                let successMessage = 'Form lengkap! Siap disubmit.';
                if (photoData && ijazahData) {
                    successMessage = 'Form lengkap dengan pas foto dan ijazah! Siap disubmit.';
                } else if (photoData) {
                    successMessage = 'Form lengkap dengan pas foto! Siap disubmit.';
                } else if (ijazahData) {
                    successMessage = 'Form lengkap dengan ijazah! Siap disubmit.';
                }
                showSuccess(successMessage);
            }
        });

        // Cleanup saat halaman ditutup
        window.addEventListener('beforeunload', function() {
            stopCamera();
        });
    </script>
</body>
</html>