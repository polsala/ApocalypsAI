FROM alpine/git:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A temporal janitor for your Docker resources."

# Install docker client and bash (alpine/git has bash, but docker-cli is separate)
RUN apk add --no-cache docker-cli bash

WORKDIR /app

COPY src/cleanup.sh .

RUN chmod +x cleanup.sh

ENTRYPOINT ["./cleanup.sh"]
