    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-lg-6 mb-4 mb-lg-0">
                    <h5 class="mb-3">
                        <i class="fas fa-building me-2"></i>Dinas Tenaga Kerja
                    </h5>
                    <p class="mb-2">Sistem Kartu Pencari Kerja Digital (AK1)</p>
                    <p class="mb-0 text-light opacity-75">Memudahkan pencarian kerja untuk semua masyarakat</p>
                </div>
                <div class="col-lg-6 text-lg-end">
                    <h5 class="mb-3">Kontak</h5>
                    <p class="mb-2">
                        <i class="fas fa-phone me-2"></i>(021) 123-4567
                    </p>
                    <p class="mb-2">
                        <i class="fas fa-envelope me-2"></i>info@disnaker.go.id
                    </p>
                    <p class="mb-0">
                        <i class="fas fa-map-marker-alt me-2"></i>Jl. Contoh Alamat No. 123
                    </p>
                </div>
            </div>
            <hr class="my-4 bg-light opacity-25">
            <div class="text-center">
                <p class="mb-0 text-light opacity-75">
                    &copy; 2024 Disnaker AK1. All rights reserved. | Powered by Digital Innovation
                </p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JS -->
    <script>
        // Smooth scrolling untuk anchor links
        document.addEventListener('DOMContentLoaded', function() {
            const links = document.querySelectorAll('a[href^="#"]');
            links.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
        });
    </script>
</body>
</html>