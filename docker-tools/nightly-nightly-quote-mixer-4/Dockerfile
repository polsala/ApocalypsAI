FROM python:3.11-slim\nWORKDIR /app\nCOPY src/requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY src/app.py .\nEXPOSE 8080\nCMD ["python", "app.py"]
