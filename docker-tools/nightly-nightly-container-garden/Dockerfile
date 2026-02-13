FROM alpine:latest

WORKDIR /app

# Install bash and docker-cli
# docker-cli provides the 'docker' command, which includes 'docker compose' subcommand.
RUN apk add --no-cache bash docker-cli

COPY src/garden.sh /usr/local/bin/garden
RUN chmod +x /usr/local/bin/garden

ENTRYPOINT ["garden"]
CMD ["--help"]
