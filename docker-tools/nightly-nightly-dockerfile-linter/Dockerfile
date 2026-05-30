FROM alpine:3.18
RUN apk add --no-cache bash
COPY src/lint.sh /usr/local/bin/lint.sh
ENTRYPOINT ["/usr/local/bin/lint.sh"]
