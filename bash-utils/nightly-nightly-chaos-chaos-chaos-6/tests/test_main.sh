#!/bin/bash

# Tests for Nightly Chaos Chaos Chaos
# Uses mocked commands to ensure deterministic, offline testing

set -euo pipefail

# Test directory
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_DIR="$TEST_DIR/../src"
SCRIPT="$SCRIPT_DIR/main.sh"

# Mock functions
mock_tc() {
  # Mock tc command for network chaos
  echo "tc: command mocked"
}

mock_systemctl() {
  # Mock systemctl command for service chaos
  echo "systemctl: command mocked"
}

mock_docker() {
  # Mock Docker commands for resource chaos
  case $1 in
    ps)
      echo "CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES"
      ;;
    run)
      echo "Container created"
      ;;
    stop)
      echo "Container stopped"
      ;;
    rm)
      echo "Container removed"
      ;;
  esac
}

mock_kubectl() {
  # Mock kubectl commands for Kubernetes chaos
  case $1 in
    run)
      echo "pod/chaos-pod created"
      ;;
    delete)
      echo "pod "chaos-pod" deleted"
      ;;
  esac
}

# Test helper: run script with mocked commands
run_with_mocks() {
  # Backup original commands
  if command -v tc &> /dev/null; then
    TC_EXISTS=true
    TC_PATH=$(which tc)
  else
    TC_EXISTS=false
  fi
  
  if command -v systemctl &> /dev/null; then
    SYSTEMCTL_EXISTS=true
    SYSTEMCTL_PATH=$(which systemctl)
  else
    SYSTEMCTL_EXISTS=false
  fi
  
  if command -v docker &> /dev/null; then
    DOCKER_EXISTS=true
    DOCKER_PATH=$(which docker)
  else
    DOCKER_EXISTS=false
  fi
  
  if command -v kubectl &> /dev/null; then
    KUBECTL_EXISTS=true
    KUBECTL_PATH=$(which kubectl)
  else
    KUBECTL_EXISTS=false
  fi
  
  # Create mock binaries
  mkdir -p /tmp/mock_bin
  
  if [[ "$TC_EXISTS" == "true" ]]; then
    sudo mv "$TC_PATH" "$TC_PATH.bak"
    sudo ln -s /tmp/mock_bin/tc "$TC_PATH"
  fi
  
  if [[ "$SYSTEMCTL_EXISTS" == "true" ]]; then
    sudo mv "$SYSTEMCTL_PATH" "$SYSTEMCTL_PATH.bak"
    sudo ln -s /tmp/mock_bin/systemctl "$SYSTEMCTL_PATH"
  fi
  
  if [[ "$DOCKER_EXISTS" == "true" ]]; then
    sudo mv "$DOCKER_PATH" "$DOCKER_PATH.bak"
    sudo ln -s /tmp/mock_bin/docker "$DOCKER_PATH"
  fi
  
  if [[ "$KUBECTL_EXISTS" == "true" ]]; then
    sudo mv "$KUBECTL_PATH" "$KUBECTL_PATH.bak"
    sudo ln -s /tmp/mock_bin/kubectl "$KUBECTL_PATH"
  fi
  
  # Create mock scripts
  cat > /tmp/mock_bin/tc << 'EOF'
#!/bin/bash
mock_tc "$@"
EOF
  chmod +x /tmp/mock_bin/tc
  
  cat > /tmp/mock_bin/systemctl << 'EOF'
#!/bin/bash
mock_systemctl "$@"
EOF
  chmod +x /tmp/mock_bin/systemctl
  
  cat > /tmp/mock_bin/docker << 'EOF'
#!/bin/bash
mock_docker "$@"
EOF
  chmod +x /tmp/mock_bin/docker
  
  cat > /tmp/mock_bin/kubectl << 'EOF'
#!/bin/bash
mock_kubectl "$@"
EOF
  chmod +x /tmp/mock_bin/kubectl
  
  # Run the script
  "$SCRIPT" "$@"
  
  # Restore original commands
  if [[ "$TC_EXISTS" == "true" ]]; then
    sudo rm "$TC_PATH"
    sudo mv "$TC_PATH.bak" "$TC_PATH"
  fi
  
  if [[ "$SYSTEMCTL_EXISTS" == "true" ]]; then
    sudo rm "$SYSTEMCTL_PATH"
    sudo mv "$SYSTEMCTL_PATH.bak" "$SYSTEMCTL_PATH"
  fi
  
  if [[ "$DOCKER_EXISTS" == "true" ]]; then
    sudo rm "$DOCKER_PATH"
    sudo mv "$DOCKER_PATH.bak" "$DOCKER_PATH"
  fi
  
  if [[ "$KUBECTL_EXISTS" == "true" ]]; then
    sudo rm "$KUBECTL_PATH"
    sudo mv "$KUBECTL_PATH.bak" "$KUBECTL_PATH"
  fi
  
  # Clean up mock binaries
  rm -rf /tmp/mock_bin
}

# Test: Run all scenarios
test_all_scenarios() {
  echo "Testing all scenarios..."
  run_with_mocks
  echo "✓ All scenarios executed successfully"
}

# Test: Run specific scenarios
test_specific_scenarios() {
  echo "Testing specific scenarios..."
  run_with_mocks --scenarios network,resource
  echo "✓ Specific scenarios executed successfully"
}

# Test: Cleanup
test_cleanup() {
  echo "Testing cleanup..."
  run_with_mocks --cleanup
  echo "✓ Cleanup executed successfully"
}

# Run tests
main() {
  echo "Running tests for Nightly Chaos Chaos Chaos..."
  test_all_scenarios
  test_specific_scenarios
  test_cleanup
  echo "All tests passed!"
}

main
