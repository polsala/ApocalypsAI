FROM alpine:latest

# Install bash and docker-cli
RUN apk add --no-cache bash docker-cli

WORKDIR /app

COPY src/chrono_compressor.sh .

# Make the script executable
RUN chmod +x chrono_compressor.sh

ENTRYPOINT ["./chrono_compressor.sh"]
CMD ["--help"]
