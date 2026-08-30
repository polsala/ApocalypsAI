FROM alpine:latest

RUN apk add --no-cache bash jq

WORKDIR /app

COPY src/echo_chamber.sh /usr/local/bin/echo_chamber.sh
RUN chmod +x /usr/local/bin/echo_chamber.sh

ENTRYPOINT ["echo_chamber.sh"]
