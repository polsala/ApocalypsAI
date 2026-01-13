#!/bin/bash

# Mock rationale: We test sourcing and function existence instead of actual chaotic behavior
source ../src/nightly-chaos-monkey-bash.sh > /dev/null 2>&1

if declare -f _chaos_prompt_hook > /dev/null; then
  echo "✅ Chaos hook function exists"
else
  echo "❌ Chaos hook function missing"
  exit 1
fi

if declare -f chaos_monkey_disable > /dev/null; then
  echo "✅ Disable function exists"
else
  echo "❌ Disable function missing"
  exit 1
fi

chaos_monkey_disable > /dev/null
if [[ $CHAOS_ENABLED -eq 0 ]]; then
  echo "✅ Chaos monkey can be disabled"
else
  echo "❌ Chaos monkey disable failed"
  exit 1
fi

echo "✅ All chaos monkey tests passed"
