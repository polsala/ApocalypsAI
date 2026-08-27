FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY src/ ./src/\nEXPOSE 5000\nCMD [\"python\",\"src/app.py\"]
