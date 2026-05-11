FROM alpine:latest
LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A containerized CLI toolbox for post-apocalyptic scenarios."

# Install essential tools
RUN apk add --no-cache \
    bash \
    curl \
    wget \
    jq \
    grep \
    sed \
    awk \
    openssl \
    netcat-openbsd \
    git \
    vim \
    tree

# Set up a custom entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
