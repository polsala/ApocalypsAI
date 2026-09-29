FROM ubuntu:20.04

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A containerized environment to run commands in a simulated past system state."

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    bash \
    curl \
    git \
    python3 \
    python3-pip \
    procps \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY src/entrypoint.sh /usr/local/bin/chronal-entrypoint.sh
RUN chmod +x /usr/local/bin/chronal-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/chronal-entrypoint.sh"]

CMD ["bash"]
