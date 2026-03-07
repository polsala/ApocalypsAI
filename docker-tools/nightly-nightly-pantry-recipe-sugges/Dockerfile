FROM python:3.11-slim\n\nWORKDIR /app\n\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY src/ ./src/\n\nENTRYPOINT ["python", "-m", "src.app"]
