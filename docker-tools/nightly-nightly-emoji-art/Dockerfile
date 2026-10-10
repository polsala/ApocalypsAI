FROM python:3.11-slim\nWORKDIR /app\nCOPY src/ /app/\nCOPY requirements.txt /app/\nRUN pip install --no-cache-dir -r requirements.txt\nENTRYPOINT ["python","app.py"]\n
