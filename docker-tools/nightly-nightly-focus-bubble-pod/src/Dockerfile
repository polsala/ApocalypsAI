FROM alpine:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="An ephemeral, isolated environment for focused work."

# Install necessary tools
RUN apk add --no-cache bash nano cowsay

# Set working directory inside the container
WORKDIR /app

# Default command to run when the container starts
# This will be overridden by the 'start' script to provide a welcome message and then a bash shell
CMD ["bash"]
