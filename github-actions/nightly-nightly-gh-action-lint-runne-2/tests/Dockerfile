FROM alpine:latest

RUN apk update && apk add --no-cache bash curl jq

# Install actionlint
RUN curl -sSL "https://github.com/rhysd/actionlint/releases/download/v1.6.10/actionlint_1.6.10_linux_amd64.tar.gz" | tar xz -C /usr/local/bin/

# Copy the entrypoint script into the container
COPY src/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
