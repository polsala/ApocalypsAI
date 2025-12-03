# Automated PR Review, Approval, and Merging System

## Overview

This document describes the automated PR review, approval, and merging workflow for ApocalypsAI. The system ensures that PRs created by AI agents (Gemini, Groq, OpenRouter) are reviewed by the other two agents before being automatically approved and merged.

## Required Secrets

The automation system requires the following repository secrets to be configured:

- **`GH_TOKEN`**: Main GitHub token used for PR creation, reviews, and merging operations
- **`REVIWER_TOKEN`**: Secondary GitHub account token used specifically for PR approvals. This ensures that PRs are approved by a different account than the one that created them, complying with GitHub's platform rules against self-approval
- **`OPENROUTER_API_KEY`**: API key for OpenRouter LLM provider
- **`GROQ_API_KEY`**: API key for Groq LLM provider
- **`GOOGLE_API_KEY`**: API key for Google's Gemini LLM provider

## Architecture

### Key Components

1. **Multi-Agent Review System** (`pr_auto_review.yml`)
   - Triggers on PR open, synchronize, and ready_for_review events
   - Detects which AI agent created the PR based on branch name patterns
   - Assigns reviews to the other two agents
   - Each reviewing agent posts a comment with their feedback

2. **Auto-Approval and Merge** (`pr_auto_approve_merge.yml`)
   - Triggers on PR review submissions and check suite completions
   - Validates that all required agent reviews are present
   - Checks CI/test status
   - Auto-approves and merges eligible PRs

3. **Cron-Based PR Processor** (`pr_cron_review_merge.yml`)
   - Runs every 4 hours to process open PRs
   - Triggers missing reviews for PRs that need them
   - Auto-approves and merges PRs that meet all criteria
   - Helps clear backlog of open PRs

### Agent Assignment Logic

The system identifies the PR author agent based on branch naming conventions:

- `ai/gemini-*` → Created by Gemini agent → Reviewed by Groq and OpenRouter
- `ai/groq-*` → Created by Groq agent → Reviewed by Gemini and OpenRouter  
- `ai/openrouter-*` → Created by OpenRouter agent → Reviewed by Gemini and Groq
- Other branches → Reviewed by all three agents

### Review Format

Each agent review includes:
- Provider identification header: `## 🤖 Review by {PROVIDER} Agent`
- Structured sections:
  - ✅ What's solid
  - 🧪 Tests
  - 🔒 Security
  - 🧩 Docs/DX
  - 🧱 Mocks/Fakes

## Eligibility Criteria for Auto-Merge

A PR is eligible for auto-approval and merge when ALL of the following are true:

1. **PR State**: PR is open
2. **Branch Pattern**: PR is from an AI agent branch (`ai/gemini-*`, `ai/groq-*`, or `ai/openrouter-*`)
3. **Reviews Complete**: PR has review comments from the other two agents (not the author agent), identified by the header `## 🤖 Review by {PROVIDER} Agent`
4. **CI Status**: All required checks have passed
   - Combined status is "success" or empty (no status checks configured)
   - All check runs are "completed" with conclusion "success", "neutral", or "skipped"
5. **Note**: The presence of a review comment is sufficient for approval; content is not parsed for blocking issues (agents provide informational feedback)

## Workflow Files

### 1. pr_auto_review.yml

**Purpose**: Automatically trigger reviews by appropriate AI agents

**Triggers**:
- `pull_request` events: opened, synchronize, ready_for_review

**Jobs**:
- `detect-author`: Identifies PR author agent and determines which agents should review
- `review-gemini`: Runs Gemini agent review (if needed)
- `review-groq`: Runs Groq agent review (if needed)
- `review-openrouter`: Runs OpenRouter agent review (if needed)

**Environment Variables**:
- `APOCALYPSAI_PROVIDER`: Set to specific provider (gemini/groq/openrouter) for each review job
- Provider API keys: `OPENROUTER_API_KEY`, `GROQ_API_KEY`, `GOOGLE_API_KEY`
- `GITHUB_TOKEN`: For GitHub API access

### 2. pr_auto_approve_merge.yml

**Purpose**: Automatically approve and merge PRs that meet all criteria

**Triggers**:
- `pull_request_review` events: submitted
- `workflow_run` events: Test and Evaluate workflow completed

**Process**:
1. Checks PR eligibility based on criteria above
2. If eligible:
   - Approves the PR with a comment
   - Merges using squash merge strategy
3. If not eligible, logs the reason

### 3. pr_cron_review_merge.yml

**Purpose**: Periodically process open PRs to handle backlog and trigger missing reviews

**Triggers**:
- `schedule`: Every 4 hours (`0 */4 * * *`)
- `workflow_dispatch`: Manual trigger

**Process**:
For each open AI agent PR:
1. Determines which agent created the PR
2. Checks which agent reviews are present
3. Triggers missing reviews by running the reviewer agent
4. If all reviews are complete and CI passes:
   - Approves the PR
   - Merges the PR

## Updated Agent Code

### agent_utils.py

Added functions for PR management:
- `create_pr_review()`: Create a formal PR review (supports `use_reviewer_token` parameter)
- `approve_pr()`: Approve a PR (uses `REVIWER_TOKEN` by default for secondary account approval)
- `merge_pr()`: Merge a PR with specified strategy
- `get_pr_reviews()`: Get all reviews for a PR
- `get_commit_status()`: Get combined CI status for a commit
- `get_check_runs()`: Get check runs for a commit
- `list_open_prs()`: List all open PRs in a repository

#### REVIWER_TOKEN Support

The `approve_pr()` function now uses the `REVIWER_TOKEN` environment variable by default. This allows a secondary GitHub account to approve PRs, preventing the same account that created the PR from approving it (which violates GitHub's platform rules).

**Key Implementation Details:**
- `_headers()` function accepts `use_reviewer_token` parameter to switch between tokens
- `_request()` function passes through the `use_reviewer_token` flag
- `approve_pr()` defaults to `use_reviewer_token=True` to use the secondary account for approvals
- The secondary account token must be configured as a repository secret named `REVIWER_TOKEN`

### agent_reviewer.py

Updated to support provider-specific reviews:
- Uses `call_provider()` instead of `cheap_mix()` to track which provider generated the review
- Returns provider name along with review text
- Adds provider header to review comments (e.g., `## 🤖 Review by GEMINI Agent`)
- Respects `APOCALYPSAI_PROVIDER` environment variable

### llm_clients.py

Enhanced with provider tracking:
- `call_provider()`: New function that returns `(response, provider_name)` tuple
- Respects `APOCALYPSAI_PROVIDER` environment variable for targeted provider usage
- Falls back to `cheap_mix` behavior when no specific provider is set

## Edge Cases and Handling

### Scenario: An agent's review fails
- **Cron workflow**: Will retry on next run (every 4 hours)
- **Manual fix**: Maintainer can manually trigger review workflow or add comment manually

### Scenario: CI checks fail
- **Behavior**: PR will not be auto-merged
- **Resolution**: Agent can update PR, triggering new checks; if checks pass, will be merged on next eligible event

### Scenario: PR has merge conflicts
- **Behavior**: Merge will fail with GitHub API error
- **Resolution**: Manual intervention required to resolve conflicts

### Scenario: Non-AI PR is opened
- **Behavior**: All three agents will review (no agent is excluded)
- **Auto-merge**: Only applies to AI agent branches; manual merge required for others

### Scenario: Review contains blocking security issues
- **Current**: Reviews are informational; presence of review is sufficient for merge
- **Note**: Agents provide feedback in structured format, but content is not parsed for blocking markers
- **Recommendation**: Agents should use clear, actionable language; maintainers can intervene if critical issues are found

## Testing

To test the workflows:

1. **Local Testing** (Python components):
   ```bash
   # Test agent_reviewer with specific provider
   export APOCALYPSAI_PROVIDER=gemini
   export GOOGLE_API_KEY=your_key
   export GITHUB_TOKEN=your_token
   python agents/agent_reviewer.py --repo polsala/ApocalypsAI --pr 123
   ```

2. **Workflow Testing**:
   - Create a test PR from an AI agent branch (e.g., `ai/gemini-test-123`)
   - Observe that the other two agents post reviews
   - Once all checks pass, PR should be auto-approved and merged

3. **Cron Testing**:
   - Manually trigger via GitHub Actions UI: Actions → "Cron - Review and Merge Open PRs" → Run workflow
   - Check logs to see which PRs were processed

## Acceptance Criteria

- [x] Automated trigger for the review workflow on new or open PRs
- [x] AI-generated review comments from the other agents (not the PR author)
- [x] Automated approval and merging for PRs passing all requirements
- [x] Cron job to process and merge eligible open PRs regularly
- [x] CI/test status checks before auto-merge
- [x] Agent reviews are tagged with provider identifier
- [x] System handles edge cases gracefully (failed reviews, failed CI, etc.)

## Future Enhancements

1. **Smart Review Content Analysis**:
   - Parse review content for blocking issues
   - Prevent auto-merge if critical security issues are found

2. **Review Quality Metrics**:
   - Track review thoroughness
   - Require minimum word count or coverage

3. **Adaptive Merge Strategy**:
   - Choose merge method based on PR characteristics
   - Support merge commits for feature branches

4. **Notification System**:
   - Notify maintainers of auto-merged PRs
   - Alert on stuck PRs (reviews pending for >24 hours)

5. **Rollback Mechanism**:
   - Detect if merged PR breaks main branch
   - Automatically revert and re-open PR for fixes

## Monitoring and Debugging

### Logs
- Review workflow logs: Check individual agent review job logs
- Auto-approve/merge logs: Check Python script output for eligibility decisions
- Cron workflow logs: See processing status for each PR

### Common Issues

**Issue**: Reviews not triggering
- **Check**: Verify branch name matches expected pattern (`ai/{agent}-*`)
- **Check**: Ensure workflow file permissions are correct
- **Check**: Review GitHub Actions workflow logs for errors

**Issue**: Auto-merge not happening
- **Check**: Verify all required reviews are present with correct headers
- **Check**: Ensure CI checks have all passed
- **Check**: Look for errors in auto-approve workflow logs

**Issue**: Cron workflow timing out
- **Check**: Reduce number of open PRs or increase timeout
- **Check**: Optimize review generation (reduce diff size, simplify prompts)
