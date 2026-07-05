FROM python:3.11-slim\n\nWORKDIR /app\n\nCOPY app.py .\n\nRUN pip install --no-cache-dir flask\n\nEXPOSE 8080\n\nCMD ["python","app.py"]\n
