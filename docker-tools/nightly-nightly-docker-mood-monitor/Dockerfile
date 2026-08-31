FROM python:3.9-slim-buster\n\nWORKDIR /app\n\nCOPY src/requirements.txt .\n\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY src/ .\n\nCMD ["python", "mood_monitor.py"]
