FROM alpine:3.18

LABEL maintainer="ApocalypsAI Integrator Agent"

RUN apk add --no-cache bash jq

WORKDIR /app

COPY src/echo-cli.sh /usr/local/bin/echo-cli
COPY src/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/echo-cli /usr/local/bin/entrypoint.sh

VOLUME /app/echoes

ENTRYPOINT ["entrypoint.sh"]
CMD ["--help"]
