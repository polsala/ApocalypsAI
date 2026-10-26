FROM ubuntu:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    stress-ng \
    iproute2 \
    procps \
    util-linux \
    && rm -rf /var/lib/apt/lists/*

COPY chaos-generator.sh /usr/local/bin/chaos-generator.sh
RUN chmod +x /usr/local/bin/chaos-generator.sh

ENTRYPOINT ["chaos-generator.sh"]
