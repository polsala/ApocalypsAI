#!/bin/bash

# Test suite for Nightly Ephemeral Runner Ghostbuster
# Uses mock functions and fixtures to test without real cloud APIs

set -euo pipefail

# Test configuration
TEST_DIR="/tmp/ghostbuster_test_$$"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/src/ghostbuster.sh"

# Mock functions
mock_aws_sts() {
    echo "Mock AWS authentication successful"
}

mock_aws_describe_instances() {
    # Mock AWS response with test instances
    cat << 'EOF'
{
  "Reservations": [
    {
      "Instances": [
        {
          "InstanceId": "i-test123",
          "State": {"Name": "running"},
          "Tags": [
            {"Key": "Name", "Value": "test-runner-001"}
          ],
          "LaunchTime": "2024-12-01T10:00:00.000Z"
        },
        {
          "InstanceId": "i-test456",
          "State": {"Name": "running"},
          "Tags": [
            {"Key": "Name", "Value": "test-runner-002"}
          ],
          "LaunchTime": "2024-12-01T08:00:00.000Z"
        }
      ]
    }
  ]
}
EOF
}

mock_az_account_show() {
    echo "Mock Azure authentication successful"
}

mock_az_vm_list() {
    # Mock Azure response
    cat << 'EOF'
[
  {
    "vmId": "vm-test-123",
    "name": "test-azure-runner-001",
    "timeCreated": "2024-12-01T09:00:00.000Z"
  }
]
EOF
}

mock_gcloud_compute_instances_list() {
    # Mock GCP response
    cat << 'EOF'
[
  {
    "name": "test-gcp-runner-001",
    "id": "gcp-test-123",
    "creationTimestamp": "2024-12-01T07:00:00.000-07:00"
  }
]
EOF
}

mock_gh_api() {
    local endpoint="$1"
    
    case "$endpoint" in
        "/orgs/test-org/actions/runners")
            cat << 'EOF'
{
  "total_count": 2,
  "runners": [
    {
      "name": "test-runner-001",
      "status": "online"
    },
    {
      "name": "active-runner-001",
      "status": "online"
    }
  ]
}
EOF
            ;;
        *)
            echo "{}"
            ;;
    esac
}

mock_gh_auth_status() {
    echo "Mock GitHub authentication successful"
}

# Test functions
setup_test() {
    mkdir -p "$TEST_DIR"
    cd "$TEST_DIR"
    
    # Backup original functions
    export ORIGINAL_AWS_STS="$AWS_STS"
    export ORIGINAL_AWS_DESCRIBE="$AWS_DESCRIBE"
    export ORIGINAL_AZ_ACCOUNT="$AZ_ACCOUNT"
    export ORIGINAL_AZ_VM="$AZ_VM"
    export ORIGINAL_GCLOUD="$GCLOUD"
    export ORIGINAL_GH_API="$GH_API"
    export ORIGINAL_GH_AUTH="$GH_AUTH"
    
    # Set up mocks
    export AWS_STS="mock_aws_sts"
    export AWS_DESCRIBE="mock_aws_describe_instances"
    export AZ_ACCOUNT="mock_az_account_show"
    export AZ_VM="mock_az_vm_list"
    export GCLOUD="mock_gcloud_compute_instances_list"
    export GH_API="mock_gh_api"
    export GH_AUTH="mock_gh_auth_status"
    
    # Set test environment variables
    export GITHUB_ORG="test-org"
    export GITHUB_REPO=""
    export AGE_THRESHOLD=3600  # 1 hour
    export CLOUD_PROVIDERS="aws,azure,gcp"
}

tear_down_test() {
    cd - > /dev/null
    rm -rf "$TEST_DIR"
    
    # Restore original functions
    export AWS_STS="$ORIGINAL_AWS_STS"
    export AWS_DESCRIBE="$ORIGINAL_AWS_DESCRIBE"
    export AZ_ACCOUNT="$ORIGINAL_AZ_ACCOUNT"
    export AZ_VM="$ORIGINAL_AZ_VM"
    export GCLOUD="$ORIGINAL_GCLOUD"
    export GH_API="$ORIGINAL_GH_API"
    export GH_AUTH="$ORIGINAL_GH_AUTH"
}

test_help() {
    echo "Testing help output..."
    
    if ! "$SCRIPT_PATH" --help > /dev/null 2>&1; then
        echo "❌ Help command failed"
        return 1
    fi
    
    echo "✅ Help test passed"
}

test_dependency_check() {
    echo "Testing dependency check..."
    
    # Mock missing dependencies
    local original_aws
    original_aws=$(which aws 2>/dev/null || echo "")
    
    # Temporarily hide aws command
    export PATH="/nonexistent:$PATH"
    
    if "$SCRIPT_PATH" --dry-run 2>&1 | grep -q "Missing required dependencies"; then
        echo "✅ Dependency check test passed"
    else
        echo "❌ Dependency check test failed"
        return 1
    fi
    
    # Restore aws command
    if [[ -n "$original_aws" ]]; then
        export PATH="$original_aws:$PATH"
    fi
}

test_github_auth() {
    echo "Testing GitHub authentication check..."
    
    # Mock gh auth status to fail
    export GH_AUTH_FAIL="true"
    
    if ! "$SCRIPT_PATH" --dry-run 2>&1 | grep -q "GitHub CLI is not authenticated"; then
        echo "❌ GitHub auth test failed"
        return 1
    fi
    
    echo "✅ GitHub auth test passed"
}

test_cloud_auth() {
    echo "Testing cloud authentication check..."
    
    # Mock cloud auth to fail
    export CLOUD_AUTH_FAIL="true"
    
    if ! "$SCRIPT_PATH" --dry-run 2>&1 | grep -q "authentication"; then
        echo "❌ Cloud auth test failed"
        return 1
    fi
    
    echo "✅ Cloud auth test passed"
}

test_orphan_detection() {
    echo "Testing orphan detection logic..."
    
    # This is a complex test that would require mocking the entire flow
    # For now, we'll test that the script can parse our mock data
    
    if ! "$SCRIPT_PATH" --dry-run --provider aws 2>&1 | grep -q "test-runner"; then
        echo "❌ Orphan detection test failed"
        return 1
    fi
    
    echo "✅ Orphan detection test passed"
}

test_age_threshold() {
    echo "Testing age threshold logic..."
    
    # Test with very old threshold to catch all instances
    if ! "$SCRIPT_PATH" --dry-run --provider aws --age-threshold 86400 2>&1 | grep -q "test-runner"; then
        echo "❌ Age threshold test failed"
        return 1
    fi
    
    echo "✅ Age threshold test passed"
}

test_dry_run_mode() {
    echo "Testing dry run mode..."
    
    if ! "$SCRIPT_PATH" --dry-run --provider aws 2>&1 | grep -q "DRY RUN"; then
        echo "❌ Dry run mode test failed"
        return 1
    fi
    
    echo "✅ Dry run mode test passed"
}

test_cleanup_mode() {
    echo "Testing cleanup mode..."
    
    # Test that cleanup mode requires confirmation (when not using --yes)
    if ! echo "no" | "$SCRIPT_PATH" --cleanup --provider aws 2>&1 | grep -q "cancelled"; then
        echo "❌ Cleanup mode test failed"
        return 1
    fi
    
    echo "✅ Cleanup mode test passed"
}

test_report_generation() {
    echo "Testing report generation..."
    
    local test_report="$TEST_DIR/test_report.txt"
    
    if ! "$SCRIPT_PATH" --dry-run --provider aws --report "$test_report" 2>&1; then
        echo "❌ Report generation test failed"
        return 1
    fi
    
    if [[ ! -f "$test_report" ]]; then
        echo "❌ Report file was not created"
        return 1
    fi
    
    if ! grep -q "Ephemeral Runner Ghostbuster Report" "$test_report"; then
        echo "❌ Report content is invalid"
        return 1
    fi
    
    echo "✅ Report generation test passed"
}

test_verbose_mode() {
    echo "Testing verbose mode..."
    
    if ! "$SCRIPT_PATH" --dry-run --provider aws --verbose 2>&1 | grep -q "DEBUG"; then
        echo "❌ Verbose mode test failed"
        return 1
    fi
    
    echo "✅ Verbose mode test passed"
}

test_error_handling() {
    echo "Testing error handling..."
    
    # Test with invalid provider
    if ! "$SCRIPT_PATH" --dry-run --provider invalid 2>&1 | grep -q "Unknown provider"; then
        echo "❌ Error handling test failed"
        return 1
    fi
    
    echo "✅ Error handling test passed"
}

# Main test runner
run_tests() {
    echo "=== Ghostbuster Test Suite ==="
    echo
    
    setup_test
    
    local tests=(
        test_help
        test_dependency_check
        test_github_auth
        test_cloud_auth
        test_orphan_detection
        test_age_threshold
        test_dry_run_mode
        test_cleanup_mode
        test_report_generation
        test_verbose_mode
        test_error_handling
    )
    
    local passed=0
    local failed=0
    
    for test in "${tests[@]}"; do
        echo "Running $test..."
        if $test; then
            ((passed++))
        else
            ((failed++))
            echo "❌ $test FAILED"
        fi
        echo
    done
    
    tear_down_test
    
    echo "=== Test Results ==="
    echo "Passed: $passed"
    echo "Failed: $failed"
    echo "Total: $((passed + failed))"
    
    if [[ $failed -eq 0 ]]; then
        echo "🎉 All tests passed!"
        return 0
    else
        echo "❌ Some tests failed"
        return 1
    fi
}

# Run tests if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    run_tests
fi
