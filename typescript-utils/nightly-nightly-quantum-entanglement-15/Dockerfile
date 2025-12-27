FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY dist/ ./dist/

# Create config directory
RUN mkdir -p /app/config

# Expose port (for potential web interface in future)
EXPOSE 3000

# Set entry point
ENTRYPOINT ["node", "dist/main.js"]

# Default command
CMD ["--help"]
