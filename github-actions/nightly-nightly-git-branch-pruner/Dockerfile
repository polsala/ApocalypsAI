FROM alpine:latest

# Install required packages
RUN apk add --no-cache \
    bash \
    curl \
    jq \
    git

# Create working directory
WORKDIR /action

# Copy action files
COPY action.yml /action/
COPY scripts/ /action/scripts/
COPY tests/ /action/tests/

# Make scripts executable
RUN chmod +x /action/scripts/*.sh
RUN chmod +x /action/tests/*.sh

# Set entry point
ENTRYPOINT ["/bin/bash", "/action/scripts/prune_branches.sh"]
