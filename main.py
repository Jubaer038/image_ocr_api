from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
import numpy as np
import cv2
import shutil
import os
import re
import requests
import io
from dotenv import load_dotenv

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()

# ✅ Create FastAPI app
app = FastAPI(
    title="Image Data Extract & Compare API",
    description="Extract temperature text from image and compare with OpenWeather API",
    version="1.0"
)

# -------------------------------
# Configure Tesseract Path
# -------------------------------
tesseract_path = shutil.which("tesseract")
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    win_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 
    if os.path.exists(win_path):
        pytesseract.pytesseract.tesseract_cmd = win_path
    else:
        raise RuntimeError("❌ Tesseract OCR not found! Please install it.")

# -------------------------------
# Helper Function: Extract Temperature
# -------------------------------
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

# -------------------------------
# Root Endpoint
# -------------------------------
@app.get("/")
def home():
    return {"message": "Welcome to Image Data Extract & Compare API"}

# -------------------------------
# Compare Endpoint
# -------------------------------
@app.post("/compare")
async def compare_temperature(
    file: UploadFile = File(...),
    city: str = Form("Dhaka")
):
    try:
        image_bytes = await file.read()
        extracted_text, extracted_temp = extract_temperature(image_bytes)

        if extracted_temp is None:
            return JSONResponse(
                content={"error": "No temperature value detected in image."},
                status_code=400
            )

        # 🌤 OpenWeather API
        api_key = os.getenv("OPENWEATHER_API_KEY", "22f9ea86b3c7d79c4a1df5b7a06da497")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if not data.get("main"):
            return JSONResponse(
                content={"error": "City not found or API error."},
                status_code=404
            )

        api_temp = round(data["main"]["temp"])

        result = {
            "city": city,
            "extracted_text": extracted_text.strip(),
            "extracted_temp": f"{extracted_temp}°C",
            "api_temp": f"{api_temp}°C",
            "match": extracted_temp == api_temp
        }

        return JSONResponse(content=result, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
