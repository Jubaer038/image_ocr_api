#  Navigate to Project Folder
cd C:\image-ocr-api

# Activate Virtual Environment
# Temporarily allow script execution in PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

# Activate the virtual environment
.venv\Scripts\Activate.ps1

3️⃣ Install Required Python Packages (if not already installed)
pip install fastapi uvicorn pytesseract pillow opencv-python-headless requests numpy python-dotenv python-multipart

# Run FastAPI Server
python -m uvicorn main:app --reload

# Open FastAPI Documentation
# Open in your browser:
# http://127.0.0.1:8000/docs
