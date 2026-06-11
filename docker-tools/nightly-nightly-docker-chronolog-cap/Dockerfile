FROM alpine:latest

LABEL maintainer="ApocalypsAI Nightly Integrator"

# Install bash and tar, which are required for the script
RUN apk add --no-cache bash tar

WORKDIR /app

# Copy the main script into the image
COPY src/chronolog_capsule.sh /usr/local/bin/chronolog_capsule

# Make the script executable
RUN chmod +x /usr/local/bin/chronolog_capsule

# Set the entrypoint to the script
ENTRYPOINT ["/usr/local/bin/chronolog_capsule"]
