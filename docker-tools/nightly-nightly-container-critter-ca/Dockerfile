FROM python:3.9-slim-buster
WORKDIR /app
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/critter_caretaker.py .
CMD ["python", "critter_caretaker.py"]
