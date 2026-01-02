# Python 3.11 Development Environment
FROM python:3.11-slim

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python development tools
RUN pip install --no-cache-dir \
    pipenv \
    poetry \
    virtualenv \
    ipython \
    jupyter \
    black \
    flake8 \
    mypy \
    pytest \
    tox

# Set working directory
WORKDIR /app

# Create a default requirements.txt
RUN echo "# Add your Python dependencies here" > requirements.txt

# Expose default port
EXPOSE 8000

# Default command
CMD ["python", "-m", "ipython"]
