FROM python:3.11-slim\n\nWORKDIR /app\n\nCOPY src/ ./\n\n# Install any runtime dependencies (none needed beyond the stdlib)\nRUN pip install --no-cache-dir --quiet \\
    # No external packages required\n    \\
    && rm -rf /root/.cache/pip\n\nENTRYPOINT ["python", "main.py"]\n
