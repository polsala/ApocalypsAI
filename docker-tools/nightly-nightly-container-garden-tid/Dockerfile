FROM docker:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A Docker utility to prune unused images, stopped containers, and dangling volumes."

WORKDIR /app

COPY src/tidy_garden.sh /usr/local/bin/tidy_garden.sh

RUN chmod +x /usr/local/bin/tidy_garden.sh

ENTRYPOINT ["/usr/local/bin/tidy_garden.sh"]
