#!/usr/bin/env bash
set -e

# Build the Docker image (quietly)
docker build -t pantry-suggester-test -f Dockerfile . > /dev/null

# Prepare sample input
cat > sample.csv <<'EOF'
rice,1
beans,2
tomato,3
EOF

# Run container with sample input
output=$(cat sample.csv | docker run -i --rm pantry-suggester-test)

# Expected lines (mock rationale: deterministic output based on hardcoded recipes)
expected1="Suggested recipes:"
expected2="- Rice and Beans Bowl"
expected3="- Tomato Rice Soup"

if echo "$output" | grep -q "$expected1" && \
   echo "$output" | grep -q "$expected2" && \
   echo "$output" | grep -q "$expected3"; then
  echo "TEST PASSED"
  exit 0
else
  echo "TEST FAILED"
  echo "Got output:"
  echo "$output"
  exit 1
fi
