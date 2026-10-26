FROM docker:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A whimsical Docker utility to identify and prune stale containers, images, and volumes."

WORKDIR /app

COPY src/compost_collector.sh /usr/local/bin/compost_collector

RUN chmod +x /usr/local/bin/compost_collector

ENTRYPOINT ["/usr/local/bin/compost_collector"]
