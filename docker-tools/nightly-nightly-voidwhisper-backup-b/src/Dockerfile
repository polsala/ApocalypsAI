FROM alpine:latest

RUN apk add --no-cache tar openssl

WORKDIR /app
COPY backup_buddy.sh /app/
RUN chmod +x /app/backup_buddy.sh

ENTRYPOINT ["./backup_buddy.sh"]
