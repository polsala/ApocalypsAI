FROM alpine/git:latest

RUN apk add --no-cache bash

WORKDIR /app

COPY src/quibble.sh /usr/local/bin/quibble.sh

RUN chmod +x /usr/local/bin/quibble.sh

ENTRYPOINT ["/usr/local/bin/quibble.sh"]

CMD ["--help"]
