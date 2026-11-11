FROM alpine:3.18
RUN apk add --no-cache bash
COPY src/affirmations.sh /usr/local/bin/affirmations.sh
RUN chmod +x /usr/local/bin/affirmations.sh
ENTRYPOINT ["/usr/local/bin/affirmations.sh"]
