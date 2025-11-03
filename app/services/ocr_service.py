import pytesseract
from PIL import Image
import numpy as np
import cv2
import io
import re
import shutil
import os

tesseract_path = shutil.which("tesseract")
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    win_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(win_path):
        pytesseract.pytesseract.tesseract_cmd = win_path
    else:
        raise RuntimeError("❌ Tesseract OCR not found! Please install it.")

def extract_temperature(image_bytes: bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(image)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        extracted_text = pytesseract.image_to_string(gray)

        temp_matches = re.findall(r'(\d+)\s*(?:°|°C|degree|degrees)', extracted_text, flags=re.IGNORECASE)
        extracted_temp = int(temp_matches[0]) if temp_matches else None

        return extracted_text, extracted_temp
    except Exception as e:
        raise ValueError(f"Image processing failed: {e}")
