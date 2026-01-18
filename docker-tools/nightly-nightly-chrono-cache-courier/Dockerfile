FROM alpine:latest
LABEL maintainer="ApocalypsAI Nightly Integrator"

# Install bash for better scripting capabilities and git (optional, but useful for dev environments)
RUN apk add --no-cache bash git

WORKDIR /app

COPY src/app.sh /usr/local/bin/chrono-cache-courier
RUN chmod +x /usr/local/bin/chrono-cache-courier

# Create a volume for notes to persist data outside the container filesystem
VOLUME /cache/notes

ENTRYPOINT ["/usr/local/bin/chrono-cache-courier"]
CMD ["help"]
