FROM docker/compose:latest

WORKDIR /app

# Copy the entrypoint script and the default docker-compose.yml
COPY src/entrypoint.sh .
COPY src/docker-compose.yml .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Set the entrypoint for the container
ENTRYPOINT ["./entrypoint.sh"]
CMD ["status"] # Default command if none provided
