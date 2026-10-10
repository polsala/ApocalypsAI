FROM python:3.11-slim\n\n# Install Flask\nRUN pip install --no-cache-dir Flask==2.3.2\n\n# Copy application code\nWORKDIR /app\nCOPY src/ ./\n\nEXPOSE 5000\n\nCMD ["python", "app.py"]
