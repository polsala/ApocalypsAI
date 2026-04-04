#!/usr/bin/env bats

@test "should pass when failure_rate is 0" {
  export INPUT_FAILURE_RATE="0"
  export INPUT_DELAY_MAX_SECONDS="1"
  run bash -c 'source src/action.yml && echo "Success"'
  [ "$status" -eq 0 ]
}

@test "should fail sometimes based on failure_rate" {
  export INPUT_FAILURE_RATE="1"
  export INPUT_DELAY_MAX_SECONDS="1"
  run bash -c 'source src/action.yml || true'
  [ "$status" -eq 1 ]
}

@test "should apply delay within bounds" {
  export INPUT_FAILURE_RATE="0"
  export INPUT_DELAY_MAX_SECONDS="2"
  start_time=$(date +%s)
  run bash -c 'source src/action.yml'
  end_time=$(date +%s)
  duration=$((end_time - start_time))
  [ "$duration" -le 2 ]
}

# Mock rationale: We mock environment variables and simulate execution flow without actual GitHub Actions runner context.
