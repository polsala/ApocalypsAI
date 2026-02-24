FROM alpine/git:latest

# Install Docker client
RUN apk add --no-cache docker

WORKDIR /app

COPY src/sweep.sh .

RUN chmod +x sweep.sh

ENTRYPOINT ["./sweep.sh"]
