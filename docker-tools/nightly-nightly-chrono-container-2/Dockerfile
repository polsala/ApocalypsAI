FROM alpine/git:latest
LABEL maintainer="ApocalypsAI Nightly Integrator"

# Install faketime
RUN apk add --no-cache faketime

# Copy the entrypoint script
COPY src/chrono-run.sh /usr/local/bin/chrono-run.sh
RUN chmod +x /usr/local/bin/chrono-run.sh

# Set the entrypoint to our script
ENTRYPOINT ["/usr/local/bin/chrono-run.sh"]
