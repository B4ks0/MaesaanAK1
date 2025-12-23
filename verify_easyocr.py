try:
    import easyocr
    print("easyocr is successfully installed and imported.")
    reader = easyocr.Reader(['en'])
    print("easyocr reader initialized successfully.")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Other error: {e}")
