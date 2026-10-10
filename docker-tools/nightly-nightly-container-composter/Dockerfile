FROM docker:24.0.5-cli-alpine3.18
LABEL maintainer="ApocalypsAI Nightly Integrator"

WORKDIR /app

COPY src/entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
