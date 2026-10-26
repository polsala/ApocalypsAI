#!/bin/bash

# Load bats helper functions
load 'test_helper'

# Mock the GitHub Actions environment variables
setup_root_dir
setup_mock_github_env

# Mock yamllint and jq commands to capture their output and exit codes
setup_mock_command "yamllint"
setup_mock_command "jq"

# --- Test Cases ---

@test "Linting success with no schema validation" {
  # Mock yamllint to succeed
  mock_command yamllint "echo 'YAML linting passed.' && exit 0"

  # Run the action script
  run "$BATS_TEST_DIR/../src/entrypoint.sh" "" "" "**/*.yml" ""

  # Assertions
  assert_output "::group::Starting YAML Linter and Validator"
  assert_output "::group::Running: yamllint **/*.yml"
  assert_output "YAML linting passed."
  assert_output "::endgroup::"
  assert_output "::group::YAML Linter and Validator finished successfully."
  assert_output "::endgroup::"
  assert_equal $status 0
}

@test "Linting failure" {
  # Mock yamllint to fail
  mock_command yamllint "echo 'YAML linting failed.' && exit 1"

  # Run the action script
  run "$BATS_TEST_DIR/../src/entrypoint.sh" "" "" "**/*.yml" ""

  # Assertions
  assert_output "::group::Starting YAML Linter and Validator"
  assert_output "::group::Running: yamllint **/*.yml"
  assert_output "YAML linting failed."
  assert_output "::error file=$BATS_TEST_DIR/../src/../N/A,line=0,col=0::YAML linting failed. Please fix the reported issues."
  assert_equal $status 1
}

@test "Linting with custom config and exclude glob" {
  # Mock yamllint to succeed
  mock_command yamllint "echo 'YAML linting passed with custom config.' && exit 0"

  # Create a dummy custom config file
  mkdir -p "$BATS_TEST_DIR/../src/"
  echo "rules: { line-length: disable }" > "$BATS_TEST_DIR/../src/.yamllint_custom"

  # Run the action script
  run "$BATS_TEST_DIR/../src/entrypoint.sh" "" "$BATS_TEST_DIR/../src/.yamllint_custom" "**/*.yml" "**/ignore_this.yml"

  # Assertions
  assert_output "::group::Starting YAML Linter and Validator"
  assert_output "::group::Running: yamllint -c $BATS_TEST_DIR/../src/.yamllint_custom **/*.yml --ignore-files **/ignore_this.yml"
  assert_output "YAML linting passed with custom config."
  assert_output "::endgroup::"
  assert_output "::group::YAML Linter and Validator finished successfully."
  assert_output "::endgroup::"
  assert_equal $status 0
}

@test "Schema validation with non-existent schema" {
  # Mock yamllint to succeed
  mock_command yamllint "echo 'YAML linting passed.' && exit 0"

  # Run the action script with a non-existent schema path
  run "$BATS_TEST_DIR/../src/entrypoint.sh" "non_existent_schema.json" "" "**/*.yml" ""

  # Assertions
  assert_output "::group::Starting YAML Linter and Validator"
  assert_output "::group::Running: yamllint **/*.yml"
  assert_output "YAML linting passed."
  assert_output "::endgroup::"
  assert_output "::group::Performing schema validation against non_existent_schema.json"
  assert_output "::error file=$BATS_TEST_DIR/../src/../N/A,line=0,col=0::Schema file not found at 'non_existent_schema.json'."
  assert_equal $status 1
}

# Mock rationale: The actual schema validation logic in entrypoint.sh is a placeholder. 
# A real implementation would require converting YAML to JSON and then using jq or a dedicated validator.
# These tests focus on the script's ability to handle the inputs and call the mock commands correctly.
# The 'jq' mock is included to show how it would be integrated if a full validation were implemented.
