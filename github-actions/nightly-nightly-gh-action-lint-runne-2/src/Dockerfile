FROM ubuntu:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    yamllint \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
