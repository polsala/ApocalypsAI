FROM python:3.9-slim-buster

WORKDIR /app

COPY src/ration_roulette.py .
COPY src/rations_template.json .

# Create a default rations.json if it doesn't exist, for first run
# Users are expected to mount their own custom rations.json
RUN cp rations_template.json rations.json

ENTRYPOINT ["python", "ration_roulette.py"]
CMD ["standard"]
