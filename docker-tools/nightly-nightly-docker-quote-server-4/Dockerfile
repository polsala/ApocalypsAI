FROM python:3.11-slim\nWORKDIR /app\nCOPY quotes.json .\nEXPOSE 8000\nCMD ["python", "-m", "http.server", "8000"]
