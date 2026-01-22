FROM python:3.9-slim-buster

WORKDIR /app

# No external Python dependencies are required for this simple version.
# If more complex parsing or libraries were needed, a requirements.txt would be added here.

COPY scrubber.py .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
