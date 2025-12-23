# TODO: Replace EasyOCR with Tesseract (pytesseract)

## Tasks
- [x] Update imports in pendaftaran/views.py: remove easyocr, add pytesseract
- [x] Replace EasyOCR reader initialization and OCR call with pytesseract.image_to_string in process_ktp_ocr function
- [x] Handle image processing to work with pytesseract (use PIL image directly)
- [x] Ensure Tesseract binary is installed (provide download/install instructions)
- [x] Test the OCR functionality with sample images (requires Tesseract installation)
- [x] Update requirements.txt to include pytesseract if not already there
