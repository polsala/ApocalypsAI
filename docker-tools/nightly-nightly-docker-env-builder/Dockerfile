FROM ubuntu:latest

LABEL maintainer="ApocalypsAI Integrator <integrator@apoc.ai>"

# Define build arguments for tools to install. Default to a common set.
ARG TOOLS_TO_INSTALL="git node python docker-cli kubectl aws-cli"

# Install essential packages and the specified development tools.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    vim \
    bash-completion \
    $TOOLS_TO_INSTALL \
    && rm -rf /var/lib/apt/lists/*

# Set a default command to run bash when the container starts.
CMD ["bash"]
