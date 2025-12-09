FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY dist/ ./dist/

# Create CLI symlink
RUN ln -s /app/dist/main.js /usr/local/bin/nightly-quantum-entanglement-checker

# Set executable permissions
RUN chmod +x /usr/local/bin/nightly-quantum-entanglement-checker

# Expose port for potential web interface
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD nightly-quantum-entanglement-checker --help

# Default command
CMD ["nightly-quantum-entanglement-checker", "--help"]
