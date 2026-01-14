#!/bin/bash

# Mock rationale: We test the script's output with various inputs to ensure correct calculations

SCRIPT_PATH="../src/chaos_budget.sh"

# Test default values
echo "Testing default values..."
output=$("$SCRIPT_PATH")
expected="Daily Chaos Budget: 1 units"
if echo "$output" | grep -q "$expected"; then
  echo "PASS: Default values test"
else
  echo "FAIL: Default values test"
  echo "Expected: $expected"
  echo "Got:"
  echo "$output"
fi

echo ""

# Test high survival level with more resources and days
echo "Testing high survival level..."
output=$("$SCRIPT_PATH" -s 8 -r 200 -d 14)
expected="Daily Chaos Budget: 0 units"
if echo "$output" | grep -q "$expected"; then
  echo "PASS: High survival level test"
else
  echo "FAIL: High survival level test"
  echo "Expected: $expected"
  echo "Got:"
  echo "$output"
fi

echo ""

# Test low survival level
echo "Testing low survival level..."
output=$("$SCRIPT_PATH" -s 2 -r 300 -d 5)
expected="Daily Chaos Budget: 5 units"
if echo "$output" | grep -q "$expected"; then
  echo "PASS: Low survival level test"
else
  echo "FAIL: Low survival level test"
  echo "Expected: $expected"
  echo "Got:"
  echo "$output"
fi

echo ""

# Test help option
echo "Testing help option..."
output=$("$SCRIPT_PATH" --help)
if echo "$output" | grep -q "Usage:"; then
  echo "PASS: Help option test"
else
  echo "FAIL: Help option test"
fi

echo ""

# Test invalid survival level
echo "Testing invalid survival level..."
output=$("$SCRIPT_PATH" -s 15 2>&1)
if echo "$output" | grep -q "Error: Survival level must be an integer between 1 and 10."; then
  echo "PASS: Invalid survival level test"
else
  echo "FAIL: Invalid survival level test"
  echo "Got:"
  echo "$output"
fi
