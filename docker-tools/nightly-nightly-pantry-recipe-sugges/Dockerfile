FROM python:3.11-slim\nWORKDIR /app\nCOPY src/ ./src/\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nENTRYPOINT ["python", "-m", "src.app"]\n
