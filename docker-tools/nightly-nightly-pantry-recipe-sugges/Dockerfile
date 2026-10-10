FROM python:3.11-slim\n\nWORKDIR /app\n\nCOPY src/ ./src/\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\nENV PYTHONPATH=/app/src\n\nCMD ["python", "-m", "src.app"]
