FROM python:3.9-slim-buster

WORKDIR /app

COPY src/survival_kit_dockerizer.py .

# Set the entrypoint to run the Python script
# The script expects the input file path as an argument
ENTRYPOINT ["python", "survival_kit_dockerizer.py"]
