FROM python:3.11-slim\n\nWORKDIR /app\n\nCOPY src/requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY src/ .\n\nEXPOSE 8080\n\nCMD ["python", "app.py"]
