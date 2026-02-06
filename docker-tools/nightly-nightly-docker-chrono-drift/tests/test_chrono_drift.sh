#!/bin/bash

set -e

UTIL_NAME="nightly-docker-chrono-drift"
IMAGE_TAG="$UTIL_NAME:test"
CONTAINER_ID="test-container-123" # A dummy ID for the script to report

echo "--- Building Docker image for $UTIL_NAME ---"
docker build -t "$IMAGE_TAG" .

echo "--- Creating mock data files ---"

# Mock rationale: These JSON files simulate the output of 'docker inspect'
# for an image and a container, allowing deterministic testing without a live Docker daemon.

# Mock Image Inspect JSON
cat <<EOF > tests/mock_image_inspect.json
[
  {
    "Id": "sha256:imageid1234567890",
    "Config": {
      "Env": [
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "LANG=C.UTF-8",
        "MY_BASE_VAR=base_value"
      ],
      "ExposedPorts": {
        "80/tcp": {}
      }
    }
  }
]
EOF

# Mock Container Inspect JSON (NO DRIFT)
cat <<EOF > tests/mock_container_inspect_no_drift.json
[
  {
    "Id": "abcdef1234567890",
    "Name": "/test-container-no-drift",
    "Image": "sha256:imageid1234567890",
    "Config": {
      "Env": [
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "LANG=C.UTF-8",
        "MY_BASE_VAR=base_value"
      ]
    },
    "NetworkSettings": {
      "Ports": {
        "80/tcp": [
          {
            "HostIp": "0.0.0.0",
            "HostPort": "8080"
          }
        ]
      }
    }
  }
]
EOF

# Mock Container Inspect JSON (WITH DRIFT)
cat <<EOF > tests/mock_container_inspect_with_drift.json
[
  {
    "Id": "abcdef1234567890",
    "Name": "/test-container-with-drift",
    "Image": "sha256:imageid1234567890",
    "Config": {
      "Env": [
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/new/path",
        "LANG=C.UTF-8",
        "MY_BASE_VAR=changed_value",
        "MY_NEW_VAR=some_value"
      ]
    },
    "NetworkSettings": {
      "Ports": {
        "80/tcp": [
          {
            "HostIp": "0.0.0.0",
            "HostPort": "8080"
          }
        ],
        "8080/tcp": [
          {
            "HostIp": "0.0.0.0",
            "HostPort": "8081"
          }
        ]
      }
    }
  }
]
EOF

# Mock container ls -R / output (NO DRIFT MARKER)
# Mock rationale: This simulates 'docker exec <container_id> ls -R /'
# It's used to check for the presence of a specific "drift marker" file.
cat <<EOF > tests/mock_container_ls_no_drift.txt
/app:
chrono_drift.py
entrypoint.sh

/tmp:
some_temp_file.log
EOF

# Mock container ls -R / output (WITH DRIFT MARKER)
cat <<EOF > tests/mock_container_ls_with_drift.txt
/app:
chrono_drift.py
entrypoint.sh

/tmp:
some_temp_file.log
chrono_drift_marker.txt
EOF

echo "--- Running tests ---"

# Test Case 1: No Drift
echo "Test Case 1: Container with NO DRIFT"
OUTPUT_NO_DRIFT=$(docker run --rm \
    -v "$(pwd)/tests/mock_image_inspect.json:/app/mock_image_inspect.json" \
    -v "$(pwd)/tests/mock_container_inspect_no_drift.json:/app/mock_container_inspect.json" \
    -v "$(pwd)/tests/mock_container_ls_no_drift.txt:/app/mock_container_ls.txt" \
    "$IMAGE_TAG" "$CONTAINER_ID")

echo "$OUTPUT_NO_DRIFT"
if echo "$OUTPUT_NO_DRIFT" | grep -q "NO DRIFT DETECTED"; then
    echo "PASS: No drift detected as expected."
else
    echo "FAIL: Drift detected when none was expected."
    exit 1
fi

echo ""

# Test Case 2: With Drift
echo "Test Case 2: Container WITH DRIFT"
OUTPUT_WITH_DRIFT=$(docker run --rm \
    -v "$(pwd)/tests/mock_image_inspect.json:/app/mock_image_inspect.json" \
    -v "$(pwd)/tests/mock_container_inspect_with_drift.json:/app/mock_container_inspect.json" \
    -v "$(pwd)/tests/mock_container_ls_with_drift.txt:/app/mock_container_ls.txt" \
    "$IMAGE_TAG" "$CONTAINER_ID")

echo "$OUTPUT_WITH_DRIFT"
if echo "$OUTPUT_WITH_DRIFT" | grep -q "DRIFT DETECTED" && \
   echo "$OUTPUT_WITH_DRIFT" | grep -q "Environment Variable Drift:" && \
   echo "$OUTPUT_WITH_DRIFT" | grep -q "Added: MY_NEW_VAR=some_value" && \
   echo "$OUTPUT_WITH_DRIFT" | grep -q "Changed: MY_BASE_VAR=changed_value (was: base_value)" && \
   echo "$OUTPUT_WITH_DRIFT" | grep -q "Exposed Port Anomalies:" && \
   echo "$OUTPUT_WITH_DRIFT" | grep -q "New Port Exposed: 8080/tcp" && \
   echo "$OUTPUT_WITH_DRIFT" | grep -q "Temporal Marker File Detected:"; then
    echo "PASS: Drift detected as expected."
else
    echo "FAIL: Drift not detected or incorrect drift reported."
    exit 1
fi

echo ""
echo "All tests passed for $UTIL_NAME!"

# Clean up mock files
rm tests/mock_image_inspect.json \
   tests/mock_container_inspect_no_drift.json \
   tests/mock_container_inspect_with_drift.json \
   tests/mock_container_ls_no_drift.txt \
   tests/mock_container_ls_with_drift.txt
