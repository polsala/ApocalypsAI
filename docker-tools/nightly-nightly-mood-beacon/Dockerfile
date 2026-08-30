FROM python:3.9-slim-buster

WORKDIR /app

RUN pip install Flask gunicorn

COPY src/ .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
