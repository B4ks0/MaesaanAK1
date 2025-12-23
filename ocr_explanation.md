As I cannot run the commands myself due to security restrictions, I will guide you on how to use the `test_ktp_ocr_ai.py` script that is already in your project directory. This script appears to be designed to extract information from a KTP image, which aligns with your goal.

### 1. What the Script Does

The `test_ktp_ocr_ai.py` script performs two main tasks:
1.  **OCR with Tesseract:** It uses `pytesseract` to scan the image (`ktp_test.jpg`) and extract any visible text.
2.  **AI-powered Data Extraction:** It sends the extracted text to a Google Gemini AI model, which then intelligently pulls out specific details like NIK, name, address, etc., and formats them into a clean, structured JSON format.

The final output is printed to your console and also saved in a file named `ktp_ocr_ai_results.json`.

### 2. Prerequisites

Before you can run the script, you need to set up a few things:

*   **Tesseract OCR Engine:**
    *   You have the installer: `tesseract-ocr-w64-setup-5.5.0.20241111.exe`. You will need to run it.
    *   **Crucially, you must select the "Indonesian" language pack during installation**, as the script needs it to recognize the text on the KTP.
    *   After installation, you must add Tesseract to your system's `PATH` so that Python can find it. The installer usually places it at `C:\Program Files\Tesseract-OCR`.

*   **Python Dependencies:**
    *   Your project has a `requirements.txt` file, which lists most of the necessary Python libraries.
    *   The script also imports `google-generativeai`, which is not in your `requirements.txt` file, so you will need to install it separately.

*   **Gemini AI API Key:**
    *   The script requires a valid API key to use the Google Gemini model. The one in the script is a placeholder.
    *   You can get a free API key from [Google AI Studio](https://aistudio.google.com/).

### 3. Step-by-Step Instructions

Here is how you can run the script:

1.  **Install Tesseract-OCR:**
    *   Double-click and run `tesseract-ocr-w64-setup-5.5.0.20241111.exe`.
    *   Follow the on-screen instructions. **Remember to check the box for the Indonesian language data.**
    *   Once installed, add it to your system's PATH as described in the prerequisites section above.

2.  **Set up a Python Virtual Environment (Recommended):**
    *   Open a command prompt (cmd) or PowerShell in your project folder (`c:\laragon\www\ak1`).
    *   Create a virtual environment:
        ```
        python -m venv venv
        ```
    *   Activate it:
        ```
        .\venv\Scripts\activate
        ```

3.  **Install Python Libraries:**
    *   With your virtual environment active, run the following commands:
        ```
        pip install -r requirements.txt
        pip install google-generativeai
        ```

4.  **Update the API Key:**
    *   Open `test_ktp_ocr_ai.py` in a code editor.
    *   Find this line: `genai.configure(api_key='AIzaSyDUMMY_KEY')`
    *   Replace the `'AIzaSyDUMMY_KEY'` with your actual key from Google AI Studio.

5.  **Run the Script:**
    *   In your command prompt, simply run:
        ```
        python test_ktp_ocr_ai.py
        ```

After running, you will see the extracted data in your terminal, and a new file, `ktp_ocr_ai_results.json`, will appear in your directory with the same results.
