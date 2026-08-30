FROM python:3.11-slim\n\nWORKDIR /app\n\nCOPY src/ ./src/\n\nRUN pip install --no-cache-dir qrcode[pil] pillow\n\nENTRYPOINT ["python", "src/main.py"]
