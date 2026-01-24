FROM alpine:latest

COPY affirmations.txt /affirmations.txt
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
