FROM alpine:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A containerized CLI toolkit for post-apocalyptic data analysis and system monitoring."

# Install essential tools
RUN apk add --no-cache \
    bash \
    jq \
    curl \
    grep \
    tldr \
    htop \
    bat \
    fzf

# Set the entrypoint to a custom script
COPY src/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"] # Default to dropping into a bash shell
