FROM alpine:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A whimsical Docker utility to prune old containers, images, volumes, and networks."

# Install bash as alpine uses ash by default, and our script uses bash-specific features
RUN apk add --no-cache bash

WORKDIR /app

COPY src/cleanup.sh .

RUN chmod +x cleanup.sh

ENTRYPOINT ["./cleanup.sh"]
