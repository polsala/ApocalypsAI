#!/bin/bash

# Test log fairy tale transformation
# Mock rationale: Verifies pattern matching and color codes without external dependencies

source ../src/main.sh

function test_transform() {
  input="$1"
  expected="$2"

  actual=$(echo "$input" | bash ../src/main.sh)
  [[ "$actual" == "$expected" ]]
}

# Test error transformation
test_transform "ERROR: Disk full" "🔥 DRAGON ATTACK! ERROR: Disk full"

# Test warning transformation
test_transform "WARN: Low memory" "🧙‍♀️ MISCHIEVOUS GNOME DETECTED: WARN: Low memory"

# Test info transformation
test_transform "INFO: System boot" "🛷 ELF DELIVERY CONFIRMED: INFO: System boot"

# Test unknown line
test_transform "Random log" "✨ MYSTERIOUS WHISPER: Random log"

# Exit with test status
echo "Log fairy tale tests: $([ $? -eq 0 ] && echo "🧙‍♂️ MAGIC WORKS!" || echo "💥 DRAGON DESTROYED TESTS")"
exit $?
