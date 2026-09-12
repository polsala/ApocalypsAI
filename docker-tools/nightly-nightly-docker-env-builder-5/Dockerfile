FROM ubuntu:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash-completion \
    curl \
    git \
    jq \
    python3 \
    python3-pip \
    yaml-cpp \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
