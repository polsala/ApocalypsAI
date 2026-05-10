FROM alpine:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="Ephemeral scratchpad environment for quick dev tasks"

# Install common development tools
RUN apk add --no-cache \
    bash \
    vim \
    git \
    curl \
    jq \
    yq \
    nano \
    build-base # For compiling simple things if needed

WORKDIR /scratchpad

# Default command if none is specified
CMD ["bash"]
