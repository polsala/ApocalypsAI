FROM python:3.9-slim-buster

LABEL maintainer="ApocalypsAI Nightly Integrator"

WORKDIR /app

# Copy the application source code
COPY src/ /app/src/

# Set the default command to run the Python application
CMD ["python", "src/app.py"]
