FROM alpine:latest

# Install common dev tools
RUN apk add --no-cache curl git python3 openssh vim

# Add whimsical startup message
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/sh"]
