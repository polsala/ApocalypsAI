FROM alpine:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A whimsical utility to gracefully stop or pause Docker containers."

# Install bash as alpine uses ash by default, and our script is bash-specific.
RUN apk add --no-cache bash

WORKDIR /app

COPY src/lullaby.sh .

RUN chmod +x lullaby.sh

# The entrypoint will be bash, and the script will be passed as an argument.
# This allows passing arguments directly to lullaby.sh when running the container.
ENTRYPOINT ["bash", "/app/lullaby.sh"]
# No default CMD, as the script handles argument validation and usage output.
CMD []
