from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.ocr_service import extract_temperature
from app.utils.weather_api import get_weather_data

router = APIRouter(tags=["Compare Temperature"])

@router.post("/compare")
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

        data = get_weather_data(city)
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
