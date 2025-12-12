FROM python:3.11-slim\n\nWORKDIR /app\n\nCOPY src/forecast.py .\n\n# No external packages needed, but keep the layer for future extensions\nRUN pip install --no-cache-dir --quiet \\
    # (placeholder for future deps)\n    \\
    && true\n\nENTRYPOINT ["python", "forecast.py"]\n
