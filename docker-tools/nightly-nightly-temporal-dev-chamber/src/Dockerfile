ARG OS_VERSION=ubuntu:22.04
FROM ${OS_VERSION}

LABEL maintainer="ApocalypsAI Nightly Integrator Agent"
LABEL description="Temporal Development Chamber Base Image"

# Set environment variables to prevent interactive prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive

# Install common build tools and utilities
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    wget \
    vim \
    nano \
    locales \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Configure locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# --- Language-specific installations (examples, extend as needed) ---

# Python installation (example: using deadsnakes PPA for older versions)
ARG PYTHON_VERSION=""
RUN if [ -n "${PYTHON_VERSION}" ]; then \
    apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python3-pip && \
    update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_VERSION} 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1 && \
    rm -rf /var/lib/apt/lists/*; \
    fi

# Node.js installation (example: using nvm or specific apt repo)
ARG NODE_VERSION=""
RUN if [ -n "${NODE_VERSION}" ]; then \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash && \
    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm use ${NODE_VERSION} && \
    nvm alias default ${NODE_VERSION}; \
    fi

# --- End of language-specific installations ---

WORKDIR /app

# Default command when entering the container
CMD ["bash"]
