FROM alpine:latest
WORKDIR /app
COPY src/compost_bin.sh .
RUN chmod +x compost_bin.sh
# Install docker client
RUN apk add --no-cache docker-cli
ENTRYPOINT ["/app/compost_bin.sh"]
