FROM alpine:3.18

RUN apk add --no-cache bash

WORKDIR /app

COPY src/ ./src/

ENTRYPOINT ["bash", "/app/src/quote_mixer.sh"]
