FROM python:3.11-slim\n\nWORKDIR /app\n\nCOPY src/ ./src/\nCOPY requirements.txt .\n\nRUN pip install --no-cache-dir -r requirements.txt\n\nEXPOSE 8080\n\nCMD [\"python\", \"src/app.py\"]
