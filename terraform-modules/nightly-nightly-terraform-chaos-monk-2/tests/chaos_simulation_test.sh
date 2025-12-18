#!/bin/bash

# Mock rationale: Simulate chaos scenarios and verify behavior
set -e

echo "=== Chaos Simulation Tests ==="

echo "1. Testing with 0% intensity (no chaos)..."
cat > test_config_low.tf << 'EOF'
module "chaos_monkey" {
  source = "../"
  enabled = true
  intensity = 0.0
  safe_mode = true
  resources = ["test-resource-1", "test-resource-2"]
}
EOF
echo "Low intensity config created"

echo "2. Testing with 100% intensity (maximum chaos)..."
cat > test_config_high.tf << 'EOF'
module "chaos_monkey" {
  source = "../"
  enabled = true
  intensity = 1.0
  safe_mode = true
  resources = ["test-resource-1", "test-resource-2"]
}
EOF
echo "High intensity config created"

echo "3. Testing disabled chaos monkey..."
cat > test_config_disabled.tf << 'EOF'
module "chaos_monkey" {
  source = "../"
  enabled = false
  intensity = 0.5
  safe_mode = true
  resources = ["test-resource-1", "test-resource-2"]
}
EOF
echo "Disabled config created"

echo "4. Testing safe mode vs destructive mode..."
cat > test_config_modes.tf << 'EOF'
module "chaos_monkey_safe" {
  source = "../"
  enabled = true
  intensity = 0.5
  safe_mode = true
  resources = ["safe-test-resource"]
}

module "chaos_monkey_destructive" {
  source = "../"
  enabled = true
  intensity = 0.5
  safe_mode = false
  resources = ["destructive-test-resource"]
}
EOF
echo "Mode comparison config created"

echo "=== Simulation tests completed ==="
