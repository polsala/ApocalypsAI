#!/usr/bin/env bats

@test "runs with default settings" {
  run bash -c 'MODE=random DURATION=1s ./simulate.sh'
  [ "$status" -eq 0 ]
}

@test "injects network delay" {
  run bash -c 'MODE=network-delay DURATION=1s ./simulate.sh'
  [ "$status" -eq 0 ]
  [[ "$output" =~ "tc qdisc del dev eth0 root" ]]
}

@test "triggers CPU stress" {
  run bash -c 'MODE=cpu-stress DURATION=1s ./simulate.sh'
  [ "$status" -eq 0 ]
  [[ "$output" =~ "stress --cpu 4" ]]
}

@test "kills named service" {
  run bash -c 'MODE=kill-service TARGET_SERVICE=myapp DURATION=1s ./simulate.sh'
  [ "$status" -eq 0 ]
  [[ "$output" =~ "pkill -f myapp" ]]
}

# Mock rationale: We mock actual system commands like tc/stress/pkill to avoid side effects,
# ensuring deterministic results without real disruptions.
