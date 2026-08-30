FROM python:3.11-slim\n\nWORKDIR /app\n\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY src/ ./src/\n\nEXPOSE 8080\n\nCMD ["python", "src/app.py"]
