FROM python:3.9-slim-buster

WORKDIR /app

COPY critter.py .

# Initialize the critter's mood file
RUN echo "Content" > mood.txt

CMD ["python", "critter.py"]
