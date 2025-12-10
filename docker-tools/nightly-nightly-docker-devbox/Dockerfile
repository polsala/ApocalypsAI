FROM ubuntu:22.04

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    tmux \
    make \
    jq \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common \
    build-essential \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update && apt-get install -y docker-ce-cli

# Install Python 3.11 and packages
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3
RUN pip3 install --no-cache-dir \
    requests \
    rich \
    pytest \
    pyyaml

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Go
ENV GO_VERSION=1.21.0
RUN wget -qO- "https://golang.org/dl/go${GO_VERSION}.linux-amd64.tar.gz" | \
    tar -C /usr/local -xzf -
ENV PATH="/usr/local/go/bin:${PATH}"

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

# Create workspace directory
WORKDIR /workspace

# Set up shell environment
RUN echo 'export PS1="\[\033[01;32m\]\u@devbox:\[\033[00m\]\[\033[01;34m\]\w\[\033[00m\]\$ "' >> ~/.bashrc
RUN echo 'alias ll="ls -alF"' >> ~/.bashrc
RUN echo 'alias la="ls -A"' >> ~/.bashrc
RUN echo 'alias l="ls -CF"' >> ~/.bashrc

# Default command
CMD ["bash"]
