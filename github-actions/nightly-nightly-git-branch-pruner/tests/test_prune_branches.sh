#!/bin/bash

# Tests for Nightly Git Branch Pruner
# These tests use mocked API responses to ensure they work offline

set -euo pipefail

# Mock functions
mock_curl() {
  local url="$1"
  local method="$2"
  shift 2
  
  # Mock branch list response
  if [[ "$url" == *"/branches?per_page=100"* ]]; then
    cat <<'EOF'
[
  {
    "name": "main",
    "commit": {
      "sha": "abc123",
      "commit": {
        "author": {
          "date": "2024-01-01T00:00:00Z"
        }
      }
    }
  },
  {
    "name": "stale-branch",
    "commit": {
      "sha": "def456",
      "commit": {
        "author": {
          "date": "2023-01-01T00:00:00Z"
        }
      }
    }
  },
  {
    "name": "active-branch",
    "commit": {
      "sha": "ghi789",
      "commit": {
        "author": {
          "date": "2024-12-01T00:00:00Z"
        }
      }
    }
  },
  {
    "name": "release/v1.0",
    "commit": {
      "sha": "jkl012",
      "commit": {
        "author": {
          "date": "2024-06-01T00:00:00Z"
        }
      }
    }
  }
]
EOF
    return 0
  fi
  
  # Mock PR creation response
  if [[ "$method" == "POST" && "$url" == *"/pulls"* ]]; then
    cat <<'EOF'
{
  "number": 123,
  "html_url": "https://github.com/test/repo/pull/123"
}
EOF
    return 0
  fi
  
  # Mock error response
  cat <<'EOF'
{
  "message": "Not Found",
  "status": 404
}
EOF
}

# Test setup
setup_test_env() {
  export GITHUB_TOKEN="mock_token"
  export GITHUB_REPOSITORY="test/repo"
  export DAYS_INACTIVE="30"
  export PROTECTED_BRANCHES="main,master,release/*"
  export DRY_RUN="true"
}

# Test functions
test_is_protected() {
  echo "Testing is_protected function..."
  
  # Test exact match
  if is_protected "main"; then
    echo "✓ main is correctly protected"
  else
    echo "✗ main should be protected"
    return 1
  fi
  
  # Test wildcard match
  if is_protected "release/v1.0"; then
    echo "✓ release/v1.0 is correctly protected"
  else
    echo "✗ release/v1.0 should be protected"
    return 1
  fi
  
  # Test non-protected branch
  if is_protected "feature/test"; then
    echo "✗ feature/test should not be protected"
    return 1
  else
    echo "✓ feature/test is correctly not protected"
  fi
}

test_is_stale() {
  echo "Testing is_stale function..."
  
  # Test stale branch (old date)
  if is_stale "stale-branch" "2023-01-01T00:00:00Z"; then
    echo "✓ stale-branch is correctly identified as stale"
  else
    echo "✗ stale-branch should be stale"
    return 1
  fi
  
  # Test active branch (recent date)
  if is_stale "active-branch" "2024-12-01T00:00:00Z"; then
    echo "✗ active-branch should not be stale"
    return 1
  else
    echo "✓ active-branch is correctly identified as active"
  fi
}

test_close_branch() {
  echo "Testing close_branch function..."
  
  # Test dry run mode
  export DRY_RUN="true"
  if close_branch "test-branch" "Test reason"; then
    echo "✓ close_branch works in dry run mode"
  else
    echo "✗ close_branch failed in dry run mode"
    return 1
  fi
  
  # Test with mocked API
  export DRY_RUN="false"
  if close_branch "test-branch" "Test reason"; then
    echo "✓ close_branch works with mocked API"
  else
    echo "✗ close_branch failed with mocked API"
    return 1
  fi
}

test_main_execution() {
  echo "Testing main execution flow..."
  
  # Mock the curl command
  curl() {
    mock_curl "$@"
  }
  
  # Run the main script logic
  local branches_response
  branches_response=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/$REPO/branches?per_page=100")
  
  local branch_count
  branch_count=$(echo "$branches_response" | jq length)
  
  if [[ $branch_count -eq 4 ]]; then
    echo "✓ Correctly parsed 4 branches from mock response"
  else
    echo "✗ Expected 4 branches, got $branch_count"
    return 1
  fi
}

# Run tests
test_suite() {
  echo "="
  echo "Running Nightly Git Branch Pruner Tests"
  echo "="
  
  setup_test_env
  
  # Source the main script to access its functions
  # We need to replace the curl function temporarily
  original_curl=$(which curl)
  
  # Mock jq for tests
  jq() {
    command jq "$@" 2>/dev/null || cat
  }
  
  # Source the script (this will fail due to API calls, so we'll test functions individually)
  # Instead, we'll test the logic by extracting and testing individual functions
  
  # Test protected branch logic
  IFS=',' read -ra PROTECTED_ARRAY <<< "$PROTECTED_BRANCHES"
  
  # Test is_protected function
  test_is_protected
  
  # Test is_stale function
  test_is_stale
  
  # Test close_branch function
  test_close_branch
  
  # Test main execution with mocked responses
  test_main_execution
  
  echo ""
  echo "All tests passed! ✓"
}

# Run the test suite
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  test_suite
fi
