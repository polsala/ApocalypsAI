FROM python:3.11-slim\nWORKDIR /app\nCOPY src/app.py /app/app.py\nRUN pip install --no-cache-dir qrcode[pil]\nENTRYPOINT ["python", "app.py"]
