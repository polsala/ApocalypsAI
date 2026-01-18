#!/usr/bin/env bats

# Mock rationale: Avoid actual network calls or email sending by mocking sendmail/mail.

@test "fails when --to or --results are missing" {
  run ./src/chaos_report_mailer.sh
  [ "$status" -ne 0 ]
}

@test "fails when results file does not exist" {
  run ./src/chaos_report_mailer.sh --to test@example.com --results nonexistent.json
  [ "$status" -ne 0 ]
  [[ "$output" == *"not found"* ]]
}

@test "generates and sends email successfully with mock sendmail" {
  # Create mock results file
  cat > /tmp/mock_results.json <<EOF
{
  "scenarios": [
    {"name": "Network Glitch", "status": "PASSED"},
    {"name": "CPU Burn", "status": "FAILED"}
  ]
}
EOF

  # Mock sendmail
  function sendmail() { cat; }
  export -f sendmail

  run ./src/chaos_report_mailer.sh --to test@example.com --results /tmp/mock_results.json

  [ "$status" -eq 0 ]
  [[ "$output" == *"Chaos report sent"* ]]

  rm -f /tmp/mock_results.json
}
