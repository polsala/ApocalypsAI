ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}-slim-buster

WORKDIR /app

# Install some basic tools that might be useful in any "era"
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy any local scripts or files into the container
# This ensures README and src scripts are available inside the container if needed
COPY README.md /app/README.md
COPY src/ /app/src/

CMD ["bash"]
