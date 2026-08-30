FROM python:3.11-slim\nWORKDIR /app\nCOPY src/ /app/\nRUN pip install --no-cache-dir Flask\nEXPOSE 5000\nCMD ["python", "app.py"]
