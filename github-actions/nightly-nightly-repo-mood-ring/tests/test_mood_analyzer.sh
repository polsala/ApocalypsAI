#!/bin/bash

# Test script for src/mood_analyzer.sh

# --- Test Helper Functions ---

# Function to run the analyzer and capture outputs
run_analyzer() {
    local commit_count="$1"
    local expected_mood="$2"
    local expected_summary_part="$3"
    local mock_git_func_name="$4" # Name of the mock git function to use

    # Reset outputs for each test
    unset GITHUB_OUTPUT_MOOD
    unset GITHUB_OUTPUT_SUMMARY

    # Mock rationale: Capture GitHub Action outputs by redirecting `echo "::set-output..."`
    # to variables. This allows deterministic testing without a real GitHub Actions runner.
    local output_file=$(mktemp)
    
    # Temporarily override the 'git' command with the specified mock function
    # This ensures that `src/mood_analyzer.sh` calls the correct mock.
    # We use a subshell to contain the `git` function override.
    (
        # Define the mock git function for this subshell
        eval "git() { $mock_git_func_name \"\$@\"; }"

        # Override echo to capture ::set-output lines
        echo() {
            if [[ "$1" == "::set-output" ]]; then
                local name_value=$(echo "$2" | cut -d':' -f2-)
                local name=$(echo "$name_value" | cut -d'=' -f1)
                local value=$(echo "$name_value" | cut -d'=' -f2-)
                if [[ "$name" == "repo-mood" ]]; then
                    GITHUB_OUTPUT_MOOD="$value"
                elif [[ "$name" == "mood-summary" ]]; then
                    GITHUB_OUTPUT_SUMMARY="$value"
                fi
            fi
            builtin echo "$@" # Call the original echo
        }
        # Run the script
        bash ../src/mood_analyzer.sh "$commit_count"
    ) > "$output_file" 2>&1

    # Read the captured outputs
    local actual_mood="$GITHUB_OUTPUT_MOOD"
    local actual_summary="$GITHUB_OUTPUT_SUMMARY"

    echo "--- Test Case: Commit Count $commit_count (Mock: $mock_git_func_name) ---"
    echo "Expected Mood: $expected_mood"
    echo "Actual Mood:   $actual_mood"
    echo "Expected Summary Part: '$expected_summary_part'"
    echo "Actual Summary:        '$actual_summary'"
    echo "-----------------------------------"

    if [[ "$actual_mood" == "$expected_mood" ]] && [[ "$actual_summary" == *"$expected_summary_part"* ]]; then
        echo "✅ Test Passed"
        return 0
    else
        echo "❌ Test Failed"
        cat "$output_file" # Print full output for debugging
        return 1
    fi
}

# --- Mock Git Functions ---

mock_git_joyful() {
  case "$@" in
    "log -n 5 --pretty=format:%s")
      echo "feat: Add a new joyful feature"
      echo "fix: Resolve a minor bug"
      echo "docs: Update README"
      echo "chore: Clean up dependencies"
      echo "refactor: Improve performance"
      ;;
    *)
      echo "Mock git log (joyful) received unexpected arguments: $@" >&2
      exit 1
      ;;
  esac
}

mock_git_stressed() {
  case "$@" in
    "log -n 3 --pretty=format:%s")
      echo "fix: Critical bug found and fixed, phew!" # Positive + Negative
      echo "bug: Another issue causing stress" # Negative
      echo "feat: Small improvement" # Positive
      ;;
    *)
      echo "Mock git log (stressed) received unexpected arguments: $@" >&2
      exit 1
      ;;
  esac
}

mock_git_neutral() {
  case "$@" in
    "log -n 1 --pretty=format:%s")
      echo "test: Add more tests"
      ;;
    *)
      echo "Mock git log (neutral) received unexpected arguments: $@" >&2
      exit 1
      ;;
  esac
}

mock_git_no_commits() {
  case "$@" in
    "log -n 0 --pretty=format:%s")
      # No output
      ;;
    *)
      echo "Mock git log (no commits) received unexpected arguments: $@" >&2
      exit 1
      ;;
  esac
}

# --- Test Cases ---

# Test 1: Joyful mood
run_analyzer 5 "Joyful" "The repository is feeling particularly cheerful and productive!" "mock_git_joyful" || exit 1

# Test 2: Stressed mood
run_analyzer 3 "Stressed" "There might be some critical issues or frustrations brewing." "mock_git_stressed" || exit 1

# Test 3: Neutral mood (single neutral commit)
run_analyzer 1 "Neutral" "A calm and steady pace, business as usual." "mock_git_neutral" || exit 1

# Test 4: No commits
run_analyzer 0 "Unknown" "No commit messages found to analyze." "mock_git_no_commits" || exit 1

echo "All tests passed!"
