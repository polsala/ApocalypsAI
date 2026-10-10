#!/bin/bash
set -e

echo "--- Running Chronosync Capsule Tests ---"

IMAGE_NAME="chronosync-capsule-test"
TEST_DIR="test_data"
CAPSULE_DIR="capsules"
UNLOCKED_DIR="unlocked_data"
PASSWORD="test_password_123"

# Cleanup function
cleanup() {
  echo "Cleaning up test artifacts..."
  docker rmi "$IMAGE_NAME" || true # Ignore error if image doesn't exist
  rm -rf "$TEST_DIR" "$CAPSULE_DIR" "$UNLOCKED_DIR"
}

# Register cleanup function to run on exit
trap cleanup EXIT

# 1. Build the Docker image
echo "Building Docker image..."
docker build -t "$IMAGE_NAME" .
echo "Docker image built successfully."

# 2. Prepare test data
echo "Preparing test data..."
mkdir -p "$TEST_DIR/subdir"
echo "Hello from the past!" > "$TEST_DIR/file1.txt"
echo "Secret message for the future." > "$TEST_DIR/subdir/secret.txt"
echo "More data" > "$TEST_DIR/another_file.log"
ls -R "$TEST_DIR"
echo "Test data prepared."

# 3. Create a capsule
echo "Creating time capsule..."
mkdir -p "$CAPSULE_DIR"
CAPSULE_BASE_NAME="my_test_capsule"
UNLOCK_DATE="20300101"

docker run --rm \
  -v "$(pwd)/$CAPSULE_DIR:/capsules" \
  -v "$(pwd)/$TEST_DIR:/data" \
  -e CHRONOSYNC_PASSWORD="$PASSWORD" \
  "$IMAGE_NAME" create /data "$CAPSULE_BASE_NAME" --unlock-date "$UNLOCK_DATE"

# Find the created capsule file (it will have a timestamp)
CAPSULE_FILE=$(find "$CAPSULE_DIR" -name "${CAPSULE_BASE_NAME}_*${UNLOCK_DATE}.tar.enc" | head -n 1)

if [ -z "$CAPSULE_FILE" ]; then
  echo "Error: Capsule file not found!"
  exit 1
fi
echo "Capsule created: $CAPSULE_FILE"
ls -l "$CAPSULE_DIR"

# 4. Attempt to unlock with wrong password (should fail)
echo "Attempting to unlock with wrong password (expected to fail)..."
if docker run --rm \
  -v "$(pwd)/$CAPSULE_DIR:/capsules" \
  -e CHRONOSYNC_PASSWORD="wrong_password" \
  "$IMAGE_NAME" unlock "/capsules/$(basename "$CAPSULE_FILE")" "/output" 2>&1 | grep -q "bad decrypt"; then
  echo "Failed as expected with wrong password."
else
  echo "Error: Unlocked with wrong password or failed differently than expected."
  exit 1
fi

# 5. Unlock the capsule
echo "Unlocking time capsule..."
mkdir -p "$UNLOCKED_DIR"
docker run --rm \
  -v "$(pwd)/$CAPSULE_DIR:/capsules" \
  -v "$(pwd)/$UNLOCKED_DIR:/output" \
  -e CHRONOSYNC_PASSWORD="$PASSWORD" \
  "$IMAGE_NAME" unlock "/capsules/$(basename "$CAPSULE_FILE")" /output

echo "Capsule unlocked. Contents:"
ls -R "$UNLOCKED_DIR"

# 6. Verify contents
echo "Verifying unlocked contents..."
if [ ! -f "$UNLOCKED_DIR/$TEST_DIR/file1.txt" ]; then
  echo "Error: file1.txt not found in unlocked data."
  exit 1
fi
if [ ! -f "$UNLOCKED_DIR/$TEST_DIR/subdir/secret.txt" ]; then
  echo "Error: secret.txt not found in unlocked data."
  exit 1
fi
if ! cmp -s "$TEST_DIR/file1.txt" "$UNLOCKED_DIR/$TEST_DIR/file1.txt"; then
  echo "Error: file1.txt content mismatch."
  exit 1
fi
if ! cmp -s "$TEST_DIR/subdir/secret.txt" "$UNLOCKED_DIR/$TEST_DIR/subdir/secret.txt"; then
  echo "Error: secret.txt content mismatch."
  exit 1
fi
echo "Contents verified successfully."

echo "--- All Chronosync Capsule Tests Passed! ---"

# Mock rationale:
# The tests are deterministic and offline because they operate on local files
# and a self-contained Docker image. The 'docker run' commands simulate
# user interaction with the container. There are no external network calls
# or dependencies on external services. The 'cmp -s' command is used to
# deterministically compare file contents. The 'grep -q "bad decrypt"'
# checks for a specific error message from openssl, which is a deterministic
# output for incorrect passwords when using AES-256-CBC decryption.
