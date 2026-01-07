#!/bin/bash
# Setup script for Nightly Docker Chaos Monkey

set -e

echo "🚀 Setting up Nightly Docker Chaos Monkey..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build the chaos monkey image
echo "🔨 Building chaos monkey image..."
docker build -t nightly-docker-chaos-monkey:latest .

# Create a test container with chaos monkey label
echo "🐳 Creating test container..."
docker run -d \
    --name test-chaos-target \
    --label "chaos.monkey=true" \
    nginx:latest

# Run the chaos monkey in dry-run mode for testing
echo "🧪 Running chaos monkey in dry-run mode..."
docker run --rm \
    --name chaos-monkey-test \
    --network host \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    nightly-docker-chaos-monkey:latest \
    --duration 30 \
    --intensity low \
    --interval 5 \
    --dry-run

# Clean up test container
echo "🧹 Cleaning up test container..."
docker stop test-chaos-target
docker rm test-chaos-target

echo "✅ Setup complete!"
echo ""
echo "Usage examples:"
echo "  # Run chaos monkey with default settings"
echo "  docker run --rm --name chaos-monkey \\"necho "    --network host \\"necho "    --volume /var/run/docker.sock:/var/run/docker.sock \\"necho "    nightly-docker-chaos-monkey:latest"
echo ""
echo "  # Run with custom settings"
echo "  docker run --rm --name chaos-monkey \\"necho "    --network host \\"necho "    --volume /var/run/docker.sock:/var/run/docker.sock \\"necho "    nightly-docker-chaos-monkey:latest \\"necho "    --duration 600 \\"necho "    --intensity high \\"necho "    --interval 30"
echo ""
echo "  # Use Docker Compose"
echo "  docker-compose up -d"
