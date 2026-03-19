#!/bin/bash

# Test suite for nightly-container-compost

# --- Test Setup ---
# Create a temporary directory for mock docker and add it to PATH
MOCK_BIN_DIR=$(mktemp -d)
export PATH="$MOCK_BIN_DIR:$PATH"

# Mock rationale: We need to control the output of 'docker' commands
# to ensure deterministic tests without needing a real Docker daemon.
# This mock function simulates the expected output for 'docker ps -a',
# 'docker images', 'docker container prune -f', and 'docker image prune -f'.
mock_docker() {
  case "$1 $2 $3" in
    "ps -a --filter")
      if [[ "$4" == "status=exited" ]]; then
        echo -e "a1b2c3d4e5f6\told_web_server\tExited (0) 2 weeks ago\n" \
                "f6e5d4c3b2a1\tforgotten_db\tExited (137) 3 days ago"
      else
        echo "" # No running containers for this test
      fi
      ;;
    "images -f dangling=true")
      echo -e "1234567890ab\t<none>\t<none>\t150MB\n" \
              "abcdef123456\t<none>\t<none>\t50MB"
      ;;
    "container prune -f")
      # Mock rationale: Simulate the output of `docker container prune -f`
      # which typically lists the IDs and then a total reclaimed space.
      echo "Deleted Containers:"
      echo "a1b2c3d4e5f6"
      echo "f6e5d4c3b2a1"
      echo "Total reclaimed space: 100MB"
      ;;
    "image prune -f")
      # Mock rationale: Simulate the output of `docker image prune -f`
      # which typically lists the IDs and then a total reclaimed space.
      echo "Deleted Images:"
      echo "1234567890ab"
      echo "abcdef123456"
      echo "Total reclaimed space: 200MB"
      ;;
    *)
      echo "Mock Docker: Unknown command: $@" >&2
      exit 1
      ;;
  esac
}

# Create the mock docker executable
cat <<EOF > "$MOCK_BIN_DIR/docker"
#!/bin/bash
$(declare -f mock_docker)
mock_docker "\$@"
EOF
chmod +x "$MOCK_BIN_DIR/docker"

# Path to the script under test
SCRIPT_PATH="./src/compost.sh"

# --- Test Functions ---

test_dry_run_output() {
  local output
  output=$("$SCRIPT_PATH" --dry-run)

  echo "--- Test: Dry Run Output ---"
  echo "$output"

  # Check for expected dry run messages
  if ! echo "$output" | grep -q "Initiating Nightly Container Compost Cycle..."; then
    echo "FAIL: Missing initiation message."
    return 1
  fi
  if ! echo "$output" | grep -q "Found 2 stale containers ready for composting:"; then
    echo "FAIL: Missing stale containers count."
    return 1
  fi
  if ! echo "$output" | grep -q "Container ID: a1b2c3d4e5f6, Name: old_web_server, Status: Exited (0) 2 weeks ago"; then
    echo "FAIL: Missing specific stale container 1."
    return 1
  fi
  if ! echo "$output" | grep -q "Found 2 dangling images ready for composting:"; then
    echo "FAIL: Missing dangling images count."
    return 1
  fi
  if ! echo "$output" | grep -q "Image ID: 1234567890ab, Repository: <none>, Tag: <none> (Size: 150MB)"; then
    echo "FAIL: Missing specific dangling image 1."
    return 1
  fi
  if ! echo "$output" | grep -q "This was a dry run. No actual composting performed."; then
    echo "FAIL: Missing dry run confirmation."
    return 1
  fi
  if ! echo "$output" | grep -q "Total potential compost: 2 containers, 2 images."; then
    echo "FAIL: Missing total potential compost count."
    return 1
  fi

  echo "PASS: Dry Run Output is correct."
  return 0
}

test_prune_output() {
  local output
  output=$("$SCRIPT_PATH" --prune)

  echo "--- Test: Prune Output ---"
  echo "$output"

  # Check for expected prune messages
  if ! echo "$output" | grep -q "Proceeding with composting..."; then
    echo "FAIL: Missing composting initiation message."
    return 1
  fi
  if ! echo "$output" | grep -q "--- Container Prune Log ---"; then
    echo "FAIL: Missing container prune log header."
    return 1
  fi
  if ! echo "$output" | grep -q "Deleted Containers:"; then
    echo "FAIL: Missing mock container prune output."
    return 1
  fi
  if ! echo "$output" | grep -q "Total reclaimed space: 100MB"; then
    echo "FAIL: Missing mock container reclaimed space."
    return 1
  fi
  if ! echo "$output" | grep -q "--- Image Prune Log ---"; then
    echo "FAIL: Missing image prune log header."
    return 1
  fi
  if ! echo "$output" | grep -q "Deleted Images:"; then
    echo "FAIL: Missing mock image prune output."
    return 1
  fi
  if ! echo "$output" | grep -q "Total reclaimed space: 200MB"; then
    echo "FAIL: Missing mock image reclaimed space."
    return 1
  fi
  if ! echo "$output" | grep -q "Containers pruned: 2"; then
    echo "FAIL: Missing final report for containers."
    return 1
  fi
  if ! echo "$output" | grep -q "Images pruned: 2"; then
    echo "FAIL: Missing final report for images."
    return 1
  fi
  if ! echo "$output" | grep -q "Your Docker garden is now refreshed and ready for new growth!"; then
    echo "FAIL: Missing final whimsical message."
    return 1
  fi

  echo "PASS: Prune Output is correct."
  return 0
}

test_no_args_shows_usage() {
  local output
  output=$("$SCRIPT_PATH" 2>&1) # Capture stderr as well

  echo "--- Test: No Args Shows Usage ---"
  echo "$output"

  if ! echo "$output" | grep -q "Usage: ./src/compost.sh [--dry-run | --prune]"; then
    echo "FAIL: Missing usage message."
    return 1
  fi
  if ! echo "$output" | grep -q "  --dry-run: Show what would be composted without deleting anything (default)."; then
    echo "FAIL: Missing dry-run description."
    return 1
  fi
  if ! echo "$output" | grep -q "  --prune:   Actually prune stale containers and dangling images."; then
    echo "FAIL: Missing prune description."
    return 1
  fi

  echo "PASS: No args shows usage."
  return 0
}

test_unknown_arg_shows_error() {
  local output
  output=$("$SCRIPT_PATH" --invalid-arg 2>&1) # Capture stderr as well

  echo "--- Test: Unknown Arg Shows Error ---"
  echo "$output"

  if ! echo "$output" | grep -q "Unknown argument: --invalid-arg"; then
    echo "FAIL: Missing unknown argument error."
    return 1
  fi
  if ! echo "$output" | grep -q "Usage: ./src/compost.sh [--dry-run | --prune]"; then
    echo "FAIL: Missing usage message after error."
    return 1
  fi

  echo "PASS: Unknown arg shows error."
  return 0
}

# --- Run Tests ---
echo "Running tests for nightly-container-compost..."
echo ""

ALL_TESTS_PASSED=0

test_dry_run_output || ALL_TESTS_PASSED=1
echo ""
test_prune_output || ALL_TESTS_PASSED=1
echo ""
test_no_args_shows_usage || ALL_TESTS_PASSED=1
echo ""
test_unknown_arg_shows_error || ALL_TESTS_PASSED=1
echo ""

# --- Test Teardown ---
rm -rf "$MOCK_BIN_DIR"

if [[ "$ALL_TESTS_PASSED" -eq 0 ]]; then
  echo "All tests passed successfully!"
  exit 0
else
  echo "Some tests failed."
  exit 1
fi
