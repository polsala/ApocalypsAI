#!/usr/bin/env bats

# Mock rationale: Simulating git commands to avoid actual repository operations and ensure deterministic tests.
git() {
  case "$@" in
    "ls-remote --heads origin")
      echo "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0\trefs/heads/main"
      echo "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1\trefs/heads/feature/active-feature"
      echo "c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2\trefs/heads/bugfix/stale-bug"
      echo "d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3\trefs/heads/feature/stale-pr-feature"
      echo "e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4\trefs/heads/feature/protected-feature"
      echo "f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5\trefs/heads/release/v1.0.0"
      ;;
    "log -1 --format=%ct origin/main")
      echo "$((CURRENT_DATE_EPOCH - 86400 * 10))" # 10 days ago
      ;;
    "log -1 --format=%ct origin/feature/active-feature")
      echo "$((CURRENT_DATE_EPOCH - 86400 * 5))" # 5 days ago
      ;;
    "log -1 --format=%ct origin/bugfix/stale-bug")
      echo "$((CURRENT_DATE_EPOCH - 86400 * 40))" # 40 days ago (stale)
      ;;
    "log -1 --format=%ct origin/feature/stale-pr-feature")
      echo "$((CURRENT_DATE_EPOCH - 86400 * 70))" # 70 days ago (stale)
      ;;
    "log -1 --format=%ct origin/feature/protected-feature")
      echo "$((CURRENT_DATE_EPOCH - 86400 * 100))" # 100 days ago (stale, but protected)
      ;;
    "log -1 --format=%ct origin/release/v1.0.0")
      echo "$((CURRENT_DATE_EPOCH - 86400 * 120))" # 120 days ago (stale, but protected by pattern)
      ;;
    "log -1 --format=%an origin/bugfix/stale-bug")
      echo "stale-bug-fixer"
      ;;
    "log -1 --format=%an origin/feature/stale-pr-feature")
      echo "stale-pr-dev"
      ;;
    "log -1 --format=%an origin/feature/protected-feature")
      echo "protected-dev"
      ;;
    "log -1 --format=%an origin/release/v1.0.0")
      echo "release-manager"
      ;;
    *)
      echo "Mocked git command not found: $@" >&2
      return 1
      ;;
  esac
}

# Mock rationale: Simulating GitHub CLI interactions to avoid actual API calls and ensure deterministic tests.
gh() {
  case "$@" in
    "pr list --head bugfix/stale-bug --state open --json number,url")
      echo "[]" # No open PR for stale-bug
      ;;
    "pr list --head feature/stale-pr-feature --state open --json number,url")
      echo "[{\"number\": 123, \"url\": \"https://github.com/test/repo/pull/123\"}]" # Open PR for stale-pr-feature
      ;;
    "pr list --head feature/protected-feature --state open --json number,url")
      echo "[]" # No open PR for protected-feature
      ;;
    "pr list --head release/v1.0.0 --state open --json number,url")
      echo "[]" # No open PR for protected-feature
      ;;
    "pr comment 123 --body Psst! This branch, \`feature/stale-pr-feature\`, seems to be gathering a bit of digital dust. Perhaps it's time to give it some love, merge it, or send it off to the great byte-bin in the sky? Just a friendly whisper from the ApocalypsAI Branch Barnacle Banishment squad! https://github.com/test/repo/pull/123")
      echo "Commented on PR 123"
      ;;
    "issue create --title Branch Barnacle Alert! \`bugfix/stale-bug\` is feeling neglected. --body Greetings, @stale-bug-fixer! The ApocalypsAI Integrator has noticed that the branch \`bugfix/stale-bug\` hasn't seen any activity in over 30 days. It's looking a bit like a forgotten relic in our digital archives. Could you please take a moment to review its purpose? Perhaps it's ready to be merged, rebased, or gracefully retired? Let's keep our repository sparkling!")
      echo "Created issue for bugfix/stale-bug"
      ;;
    *)
      echo "Mocked gh command not found: $@" >&2
      return 1
      ;;
  esac
}

# Mock rationale: Simulating jq command to avoid external dependency and ensure deterministic tests.
jq() {
  case "$@" in
    '.length')
      if [[ "$1" == "[]" ]]; then echo 0; else echo 1; fi
      ;;
    '.[0].number')
      echo 123
      ;;
    '.[0].url')
      echo "https://github.com/test/repo/pull/123"
      ;;
    '.[0].url' | tr -d '\n'')
      echo "https://github.com/test/repo/pull/123"
      ;;
    *)
      echo "Mocked jq command not found: $@" >&2
      return 1
      ;;
  esac
}

setup() {
  export GITHUB_TOKEN="mock_token"
  export GITHUB_REPOSITORY="test/repo"
  export STALE_DAYS=30
  export PROTECTED_BRANCHES="main master feature/protected-feature release/*"
  export CURRENT_DATE_EPOCH=$(date +%s) # Set current time for relative date calculations
  # Ensure branch_banisher.sh is in PATH for bats to find it
  export PATH="$(pwd)/src:$PATH"
}

@test "no action taken for active branches" {
  run branch_banisher.sh
  assert_output --regexp "Skipping protected branch: main"
  assert_output --regexp "Branch: feature/active-feature, Last commit: .*, Age: 5 days"
  refute_output --regexp "Branch: feature/active-feature.*is stale"
  refute_output --regexp "Commented on PR"
  refute_output --regexp "Created issue"
}

@test "comment on PR for stale branch with open PR" {
  run branch_banisher.sh
  assert_output --regexp "Branch: feature/stale-pr-feature, Last commit: .*, Age: 70 days"
  assert_output --regexp "Branch 'feature/stale-pr-feature' is stale"
  assert_output --regexp "Found open PR #123 for 'feature/stale-pr-feature'. Adding a whimsical comment."
  assert_output --regexp "Commented on PR 123"
  refute_output --regexp "Created issue"
}

@test "create issue for stale branch without open PR" {
  run branch_banisher.sh
  assert_output --regexp "Branch: bugfix/stale-bug, Last commit: .*, Age: 40 days"
  assert_output --regexp "Branch 'bugfix/stale-bug' is stale"
  assert_output --regexp "No open PR for 'bugfix/stale-bug'. Creating a whimsical issue."
  assert_output --regexp "Created issue for bugfix/stale-bug"
  refute_output --regexp "Commented on PR"
}

@test "protected branches are skipped by exact name" {
  run branch_banisher.sh
  assert_output --regexp "Skipping protected branch: feature/protected-feature"
  refute_output --regexp "Branch: feature/protected-feature.*is stale"
  refute_output --regexp "Commented on PR"
  refute_output --regexp "Created issue"
}

@test "protected branches are skipped by pattern" {
  run branch_banisher.sh
  assert_output --regexp "Skipping protected branch: release/v1.0.0"
  refute_output --regexp "Branch: release/v1.0.0.*is stale"
  refute_output --regexp "Commented on PR"
  refute_output --regexp "Created issue"
}
