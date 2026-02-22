FROM alpine:latest

# Install bash, which is required for the run_courier.sh script
RUN apk add --no-cache bash

WORKDIR /app

# Copy the main script into the container
COPY src/run_courier.sh .

# Set the entrypoint to execute the courier script
ENTRYPOINT ["bash", "./run_courier.sh"]
