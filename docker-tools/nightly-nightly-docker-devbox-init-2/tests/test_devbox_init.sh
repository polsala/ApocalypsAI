#!/bin/bash

# Mock rationale: Tests file generation logic without requiring Docker or language runtimes.

set -e

./src/devbox-init.sh python test_python_proj

if [ ! -f "test_python_proj/Dockerfile" ]; then
  echo "❌ Python Dockerfile not created"
  exit 1
fi

if [ ! -f "test_python_proj/docker-compose.yml" ]; then
  echo "❌ Python docker-compose not created"
  exit 1
fi

rm -rf test_python_proj

./src/devbox-init.sh node test_node_proj

if [ ! -f "test_node_proj/index.js" ]; then
  echo "❌ Node index.js not created"
  exit 1
fi

rm -rf test_node_proj

echo "✅ All devbox init tests passed"
