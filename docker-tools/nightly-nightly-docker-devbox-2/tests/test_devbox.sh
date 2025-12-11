#!/bin/bash

# Test script for nightly-docker-devbox
# Run this inside the container to verify all tools are installed

set -e

echo "🧪 Testing Nightly Docker DevBox..."

# Test git
echo "📦 Testing git..."
git --version
echo "✅ Git installed"

# Test curl
echo "📦 Testing curl..."
curl --version
echo "✅ Curl installed"

# Test jq
echo "📦 Testing jq..."
jq --version
echo "✅ JQ installed"

# Test make
echo "📦 Testing make..."
make --version
echo "✅ Make installed"

# Test Python
echo "📦 Testing Python..."
python3 --version
python3 -c "import requests, yaml, rich; print('Python packages OK')"
echo "✅ Python installed"

# Test Rust
echo "📦 Testing Rust..."
rustc --version
cargo --version
echo "✅ Rust installed"

# Test Node.js
echo "📦 Testing Node.js..."
node --version
npm --version
ts-node --version
echo "✅ Node.js installed"

# Test Docker CLI
echo "📦 Testing Docker CLI..."
docker --version
echo "✅ Docker CLI installed"

# Test SSH server
echo "📦 Testing SSH server..."
if pgrep sshd > /dev/null; then
    echo "✅ SSH server running"
else
    echo "❌ SSH server not running"
    exit 1
fi

echo "🎉 All tests passed! DevBox is ready to use."
