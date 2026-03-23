# Use the official Docker CLI image as a base
FROM docker:cli

# Copy the janitor script
COPY src/janitor.sh /usr/local/bin/janitor.sh

# Make the script executable
RUN chmod +x /usr/local/bin/janitor.sh

# Set the entrypoint to the janitor script
ENTRYPOINT ["/usr/local/bin/janitor.sh"]
