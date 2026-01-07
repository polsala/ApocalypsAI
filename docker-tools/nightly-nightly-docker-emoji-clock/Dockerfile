FROM alpine:3.18

RUN apk add --no-cache bash

COPY src/emoji_clock.sh /usr/local/bin/emoji_clock.sh

RUN chmod +x /usr/local/bin/emoji_clock.sh

ENTRYPOINT ["/usr/local/bin/emoji_clock.sh"]
