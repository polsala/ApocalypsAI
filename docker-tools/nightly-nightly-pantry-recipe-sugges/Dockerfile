FROM alpine:3.18

# install bash and coreutils
RUN apk add --no-cache bash

WORKDIR /app
COPY src/suggest.sh /app/suggest.sh
RUN chmod +x /app/suggest.sh

ENTRYPOINT ["/app/suggest.sh"]
