FROM python:3.11-slim\n\nWORKDIR /app\n\nCOPY src/ ./src/\nCOPY src/__init__.py ./src/__init__.py\n\n# No external dependencies required\n\nENTRYPOINT ["python", "src/app.py"]\n
