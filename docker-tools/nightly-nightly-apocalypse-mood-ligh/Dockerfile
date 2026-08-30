FROM python:3.11-slim\nWORKDIR /app\nCOPY src/ ./src/\nRUN pip install --no-cache-dir Flask\nEXPOSE 5000\nCMD ["python", "src/app.py"]
