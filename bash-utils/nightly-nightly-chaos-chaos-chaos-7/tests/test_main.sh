#!/bin/bash

# Test suite for Nightly Chaos Chaos Chaos 7
# Uses mocks to ensure deterministic, offline tests

set -euo pipefail

# Mock rationale: Replace external commands with controlled mocks
mock_setup() {
  # Create temporary directory for mocks
  MOCK_DIR=$(mktemp -d)
  export PATH="$MOCK_DIR:$PATH"
  
  # Mock tc
  cat > "$MOCK_DIR/tc" << 'EOF'
#!/bin/bash
# Mock tc that records calls
echo "tc $@" >> /tmp/tc_calls.log
EOF
  chmod +x "$MOCK_DIR/tc"
  
  # Mock stress
  cat > "$MOCK_DIR/stress" << 'EOF'
#!/bin/bash
# Mock stress that records calls
echo "stress $@" >> /tmp/stress_calls.log
EOF
  chmod +x "$MOCK_DIR/stress"
  
  # Mock systemctl
  cat > "$MOCK_DIR/systemctl" << 'EOF'
#!/bin/bash
# Mock systemctl that records calls
echo "systemctl $@" >> /tmp/systemctl_calls.log
EOF
  chmod +x "$MOCK_DIR/systemctl"
  
  # Mock date
  cat > "$MOCK_DIR/date" << 'EOF'
#!/bin/bash
# Mock date that records calls and returns fixed time
if [[ "$1" == "-s" ]]; then
  echo "date -s $2" >> /tmp/date_calls.log
else
  echo "2023-01-01 12:00:00"
fi
EOF
  chmod +x "$MOCK_DIR/date"
  
  # Mock pkill
  cat > "$MOCK_DIR/pkill" << 'EOF'
#!/bin/bash
# Mock pkill that records calls
echo "pkill $@" >> /tmp/pkill_calls.log
EOF
  chmod +x "$MOCK_DIR/pkill"
}

mock_cleanup() {
  rm -rf "$MOCK_DIR"
  rm -f /tmp/tc_calls.log /tmp/stress_calls.log /tmp/systemctl_calls.log /tmp/date_calls.log /tmp/pkill_calls.log
}

# Test network chaos
test_network_chaos() {
  log "Testing network chaos..."
  ./src/main.sh --scenario network
  
  if grep -q "tc qdisc add dev eth0 root netem delay 100ms" /tmp/tc_calls.log; then
    log "✓ Network latency applied"
  else
    error "✗ Network latency not applied"
    exit 1
  fi
  
  if grep -q "tc qdisc add dev eth0 root netem loss 10%" /tmp/tc_calls.log; then
    log "✓ Network packet loss applied"
  else
    error "✗ Network packet loss not applied"
    exit 1
  fi
}

# Test resource chaos
test_resource_chaos() {
  log "Testing resource chaos..."
  ./src/main.sh --scenario resource
  
  if grep -q "stress --cpu 4 --timeout 60s" /tmp/stress_calls.log; then
    log "✓ CPU stress applied"
  else
    error "✗ CPU stress not applied"
    exit 1
  fi
  
  if grep -q "stress --vm 2 --vm-bytes 128M --timeout 60s" /tmp/stress_calls.log; then
    log "✓ Memory stress applied"
  else
    error "✗ Memory stress not applied"
    exit 1
  fi
}

# Test time chaos
test_time_chaos() {
  log "Testing time chaos..."
  ./src/main.sh --scenario time
  
  if grep -q "date -s -1 hour" /tmp/date_calls.log; then
    log "✓ Time adjustment applied"
  else
    error "✗ Time adjustment not applied"
    exit 1
  fi
  
  if [[ -f /tmp/chaos_time_backup ]]; then
    log "✓ Time backup created"
  else
    error "✗ Time backup not created"
    exit 1
  fi
}

# Test service chaos
test_service_chaos() {
  log "Testing service chaos..."
  ./src/main.sh --scenario service
  
  if grep -q "systemctl stop ssh" /tmp/systemctl_calls.log; then
    log "✓ Service stop applied"
  else
    error "✗ Service stop not applied"
    exit 1
  fi
}

# Test cleanup
test_cleanup() {
  log "Testing cleanup..."
  ./src/main.sh --cleanup
  
  if grep -q "tc qdisc del dev eth0 root" /tmp/tc_calls.log; then
    log "✓ Network cleanup applied"
  else
    error "✗ Network cleanup not applied"
    exit 1
  fi
  
  if grep -q "systemctl start ssh" /tmp/systemctl_calls.log; then
    log "✓ Service cleanup applied"
  else
    error "✗ Service cleanup not applied"
    exit 1
  fi
  
  if grep -q "pkill -f stress" /tmp/pkill_calls.log; then
    log "✓ Resource cleanup applied"
  else
    error "✗ Resource cleanup not applied"
    exit 1
  fi
}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
  echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
  echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Run tests
main() {
  log "Setting up mocks..."
  mock_setup
  
  log "Running tests..."
  test_network_chaos
  test_resource_chaos
  test_time_chaos
  test_service_chaos
  test_cleanup
  
  log "Cleaning up mocks..."
  mock_cleanup
  
  log "All tests passed!"
}

main
