FROM alpine:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="Base image for the Ephemeral Dev Oasis"

# Install essential tools
RUN apk add --no-cache \
    bash \
    git \
    vim \
    curl \
    openssh-client # Useful for cloning private repos

WORKDIR /app

# Set default command to bash for interactive sessions
CMD ["bash"]
