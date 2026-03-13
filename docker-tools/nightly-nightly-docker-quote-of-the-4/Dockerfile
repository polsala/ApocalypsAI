FROM python:3.11-slim\n\nWORKDIR /app\n\nCOPY src/ .\n\nRUN pip install --no-cache-dir Flask\n\nEXPOSE 8080\n\nCMD ["python", "app.py"]
