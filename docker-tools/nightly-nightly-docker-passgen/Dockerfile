FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ .

EXPOSE 8080

CMD ["python", "app.py"]

