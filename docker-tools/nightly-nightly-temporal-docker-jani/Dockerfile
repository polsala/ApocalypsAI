FROM docker:latest-alpine

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A containerized utility for temporal Docker resource cleanup."

WORKDIR /app

COPY src/janitor.sh /app/janitor.sh

RUN chmod +x /app/janitor.sh

ENTRYPOINT ["/app/janitor.sh"]
