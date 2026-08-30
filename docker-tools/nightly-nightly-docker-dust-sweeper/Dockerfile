FROM alpine:3.18

LABEL maintainer="ApocalypsAI Nightly Integrator Agent"
LABEL description="A whimsical containerized utility to sweep away unused Docker images, containers, volumes, and networks."

WORKDIR /app

COPY src/sweep.sh /usr/local/bin/sweep.sh

RUN chmod +x /usr/local/bin/sweep.sh

ENTRYPOINT ["/usr/local/bin/sweep.sh"]
