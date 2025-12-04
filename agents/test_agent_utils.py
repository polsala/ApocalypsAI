"""Tests for agent_utils GitHub API functions."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agents.agent_utils import (
    GitHubError,
    get_branch_protection,
    get_required_status_checks,
    is_pr_approved,
    enable_auto_merge,
    create_check_run,
    update_check_run,
    find_check_run,
    create_or_update_check_run,
)


class TestBranchProtection:
    """Test branch protection and required checks functions."""

    def test_get_branch_protection_returns_protection_data(self):
        """Test that get_branch_protection returns protection data when available."""
        mock_protection = {
            "required_status_checks": {
                "contexts": ["ci/test", "ci/build"],
                "checks": []
            }
        }
        
        with patch("agents.agent_utils._request") as mock_request:
            mock_request.return_value = mock_protection
            result = get_branch_protection("owner/repo", "main")
            assert result == mock_protection
            mock_request.assert_called_once_with("GET", "/repos/owner/repo/branches/main/protection")

    def test_get_branch_protection_returns_none_on_error(self):
        """Test that get_branch_protection returns None when branch is not protected."""
        with patch("agents.agent_utils._request") as mock_request:
            mock_request.side_effect = GitHubError("404 Not Found")
            result = get_branch_protection("owner/repo", "main")
            assert result is None

    def test_get_required_status_checks_with_contexts(self):
        """Test that get_required_status_checks extracts contexts correctly."""
        mock_protection = {
            "required_status_checks": {
                "contexts": ["ci/test", "ci/build"],
                "checks": []
            }
        }
        
        with patch("agents.agent_utils.get_branch_protection") as mock_get_protection:
            mock_get_protection.return_value = mock_protection
            result = get_required_status_checks("owner/repo", "main")
            assert set(result) == {"ci/test", "ci/build"}

    def test_get_required_status_checks_with_checks_array(self):
        """Test that get_required_status_checks extracts from checks array."""
        mock_protection = {
            "required_status_checks": {
                "contexts": [],
                "checks": [
                    {"context": "ci/test"},
                    {"context": "ci/build"}
                ]
            }
        }
        
        with patch("agents.agent_utils.get_branch_protection") as mock_get_protection:
            mock_get_protection.return_value = mock_protection
            result = get_required_status_checks("owner/repo", "main")
            assert set(result) == {"ci/test", "ci/build"}

    def test_get_required_status_checks_combines_both_formats(self):
        """Test that get_required_status_checks combines contexts and checks."""
        mock_protection = {
            "required_status_checks": {
                "contexts": ["ci/test"],
                "checks": [
                    {"context": "ci/build"}
                ]
            }
        }
        
        with patch("agents.agent_utils.get_branch_protection") as mock_get_protection:
            mock_get_protection.return_value = mock_protection
            result = get_required_status_checks("owner/repo", "main")
            assert set(result) == {"ci/test", "ci/build"}

    def test_get_required_status_checks_no_protection(self):
        """Test that get_required_status_checks returns empty list when no protection."""
        with patch("agents.agent_utils.get_branch_protection") as mock_get_protection:
            mock_get_protection.return_value = None
            result = get_required_status_checks("owner/repo", "main")
            assert result == []

    def test_get_required_status_checks_no_required_checks(self):
        """Test that get_required_status_checks returns empty list when no required checks."""
        mock_protection = {
            "required_status_checks": None
        }
        
        with patch("agents.agent_utils.get_branch_protection") as mock_get_protection:
            mock_get_protection.return_value = mock_protection
            result = get_required_status_checks("owner/repo", "main")
            assert result == []

    def test_get_required_status_checks_empty_required_checks(self):
        """Test that get_required_status_checks handles empty required_status_checks."""
        mock_protection = {
            "required_status_checks": {
                "contexts": [],
                "checks": []
            }
        }
        
        with patch("agents.agent_utils.get_branch_protection") as mock_get_protection:
            mock_get_protection.return_value = mock_protection
            result = get_required_status_checks("owner/repo", "main")
            assert result == []

    def test_get_required_status_checks_filters_empty_strings(self):
        """Test that get_required_status_checks filters out empty strings and missing context keys.
        
        This test verifies that the function handles malformed check data gracefully:
        - Empty strings in contexts array are filtered out
        - Empty strings in checks array contexts are filtered out  
        - Check objects missing the 'context' key are handled without error
        """
        mock_protection = {
            "required_status_checks": {
                "contexts": ["ci/test", ""],
                "checks": [
                    {"context": "ci/build"},
                    {"context": ""},
                    {}  # Missing context key entirely
                ]
            }
        }
        
        with patch("agents.agent_utils.get_branch_protection") as mock_get_protection:
            mock_get_protection.return_value = mock_protection
            result = get_required_status_checks("owner/repo", "main")
            # Should only contain non-empty strings
            assert set(result) == {"ci/test", "ci/build"}
            assert "" not in result


class TestPRApproval:
    """Test PR approval checking functions."""

    def test_is_pr_approved_returns_true_when_approved(self):
        """Test that is_pr_approved returns True when PR has at least one approval."""
        mock_reviews = [
            {"state": "COMMENTED", "user": {"login": "user1"}},
            {"state": "APPROVED", "user": {"login": "user2"}},
        ]
        
        with patch("agents.agent_utils.get_pr_reviews") as mock_get_reviews:
            mock_get_reviews.return_value = mock_reviews
            result = is_pr_approved("owner/repo", 123)
            assert result is True
            mock_get_reviews.assert_called_once_with("owner/repo", 123)

    def test_is_pr_approved_returns_false_when_not_approved(self):
        """Test that is_pr_approved returns False when PR has no approvals."""
        mock_reviews = [
            {"state": "COMMENTED", "user": {"login": "user1"}},
            {"state": "CHANGES_REQUESTED", "user": {"login": "user2"}},
        ]
        
        with patch("agents.agent_utils.get_pr_reviews") as mock_get_reviews:
            mock_get_reviews.return_value = mock_reviews
            result = is_pr_approved("owner/repo", 123)
            assert result is False

    def test_is_pr_approved_returns_false_when_no_reviews(self):
        """Test that is_pr_approved returns False when PR has no reviews."""
        with patch("agents.agent_utils.get_pr_reviews") as mock_get_reviews:
            mock_get_reviews.return_value = []
            result = is_pr_approved("owner/repo", 123)
            assert result is False

    def test_is_pr_approved_handles_multiple_approvals(self):
        """Test that is_pr_approved returns True with multiple approvals."""
        mock_reviews = [
            {"state": "APPROVED", "user": {"login": "user1"}},
            {"state": "APPROVED", "user": {"login": "user2"}},
        ]
        
        with patch("agents.agent_utils.get_pr_reviews") as mock_get_reviews:
            mock_get_reviews.return_value = mock_reviews
            result = is_pr_approved("owner/repo", 123)
            assert result is True


class TestAutoMerge:
    """Test auto-merge enabling functions."""

    def test_enable_auto_merge_success(self):
        """Test that enable_auto_merge (alias for merge_pr) successfully merges the PR via GraphQL.
        
        Note: enable_auto_merge is now an alias for merge_pr, which merges immediately
        rather than enabling auto-merge. This maintains backward compatibility while
        using the immediate merge approach.
        """
        mock_pr_data = {"node_id": "PR_kwDOABCDEF12345"}
        mock_graphql_response = {
            "data": {
                "mergePullRequest": {
                    "pullRequest": {
                        "id": "PR_kwDOABCDEF12345",
                        "merged": True,
                        "mergedAt": "2024-01-01T00:00:00Z",
                        "mergeCommit": {
                            "oid": "abc123"
                        }
                    }
                }
            }
        }
        
        with patch("agents.agent_utils.get_pr") as mock_get_pr, \
             patch("agents.agent_utils.requests.post") as mock_post, \
             patch("os.environ.get") as mock_env:
            mock_get_pr.return_value = mock_pr_data
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_graphql_response
            mock_env.return_value = "fake_token"
            
            # Should not raise an exception
            enable_auto_merge("owner/repo", 123, merge_method="squash")
            
            # Verify GraphQL mutation was called with correct parameters
            assert mock_post.called
            call_args = mock_post.call_args
            assert "query" in call_args[1]["json"]
            assert "variables" in call_args[1]["json"]
            assert call_args[1]["json"]["variables"]["pullRequestId"] == "PR_kwDOABCDEF12345"
            assert call_args[1]["json"]["variables"]["mergeMethod"] == "SQUASH"

    def test_enable_auto_merge_missing_node_id(self):
        """Test that enable_auto_merge raises error when node_id is missing."""
        mock_pr_data = {}  # Missing node_id
        
        with patch("agents.agent_utils.get_pr") as mock_get_pr:
            mock_get_pr.return_value = mock_pr_data
            
            with pytest.raises(GitHubError, match="Could not get node_id"):
                enable_auto_merge("owner/repo", 123)

    def test_enable_auto_merge_graphql_errors(self):
        """Test that enable_auto_merge raises error on GraphQL errors."""
        mock_pr_data = {"node_id": "PR_kwDOABCDEF12345"}
        mock_graphql_response = {
            "errors": [
                {"message": "Auto-merge is not allowed for this repository"}
            ]
        }
        
        with patch("agents.agent_utils.get_pr") as mock_get_pr, \
             patch("agents.agent_utils.requests.post") as mock_post, \
             patch("os.environ.get") as mock_env:
            mock_get_pr.return_value = mock_pr_data
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_graphql_response
            mock_env.return_value = "fake_token"
            
            with pytest.raises(GitHubError, match="GraphQL errors"):
                enable_auto_merge("owner/repo", 123)


class TestCheckRuns:
    """Test check run creation and update functions."""

    def test_create_check_run_success(self):
        """Test that create_check_run creates a check run successfully."""
        mock_check_run = {
            "id": 12345,
            "name": "review-groq",
            "status": "completed",
            "conclusion": "success"
        }
        
        with patch("agents.agent_utils._request") as mock_request:
            mock_request.return_value = mock_check_run
            result = create_check_run(
                repo="owner/repo",
                name="review-groq",
                head_sha="abc123",
                status="completed",
                conclusion="success"
            )
            assert result == mock_check_run
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[0] == ("POST", "/repos/owner/repo/check-runs")
            assert call_args[1]["json"]["name"] == "review-groq"
            assert call_args[1]["json"]["head_sha"] == "abc123"
            assert call_args[1]["json"]["status"] == "completed"
            assert call_args[1]["json"]["conclusion"] == "success"

    def test_create_check_run_with_output(self):
        """Test that create_check_run includes output when provided."""
        mock_check_run = {"id": 12345}
        output = {
            "title": "Review completed",
            "summary": "All checks passed"
        }
        
        with patch("agents.agent_utils._request") as mock_request:
            mock_request.return_value = mock_check_run
            create_check_run(
                repo="owner/repo",
                name="review-groq",
                head_sha="abc123",
                output=output
            )
            call_args = mock_request.call_args
            assert call_args[1]["json"]["output"] == output

    def test_update_check_run_success(self):
        """Test that update_check_run updates a check run successfully."""
        mock_check_run = {
            "id": 12345,
            "status": "completed",
            "conclusion": "success"
        }
        
        with patch("agents.agent_utils._request") as mock_request:
            mock_request.return_value = mock_check_run
            result = update_check_run(
                repo="owner/repo",
                check_run_id=12345,
                status="completed",
                conclusion="success"
            )
            assert result == mock_check_run
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[0] == ("PATCH", "/repos/owner/repo/check-runs/12345")
            assert call_args[1]["json"]["status"] == "completed"
            assert call_args[1]["json"]["conclusion"] == "success"

    def test_find_check_run_found(self):
        """Test that find_check_run returns check run when found."""
        mock_check_runs = {
            "check_runs": [
                {"id": 1, "name": "review-gemini"},
                {"id": 2, "name": "review-groq"},
                {"id": 3, "name": "review-openrouter"}
            ]
        }
        
        with patch("agents.agent_utils.get_check_runs") as mock_get_check_runs:
            mock_get_check_runs.return_value = mock_check_runs
            result = find_check_run("owner/repo", "abc123", "review-groq")
            assert result == {"id": 2, "name": "review-groq"}

    def test_find_check_run_not_found(self):
        """Test that find_check_run returns None when not found."""
        mock_check_runs = {
            "check_runs": [
                {"id": 1, "name": "review-gemini"}
            ]
        }
        
        with patch("agents.agent_utils.get_check_runs") as mock_get_check_runs:
            mock_get_check_runs.return_value = mock_check_runs
            result = find_check_run("owner/repo", "abc123", "review-groq")
            assert result is None

    def test_create_or_update_check_run_creates_new(self):
        """Test that create_or_update_check_run creates new run when none exists."""
        mock_check_run = {"id": 12345, "name": "review-groq"}
        
        with patch("agents.agent_utils.find_check_run") as mock_find, \
             patch("agents.agent_utils.create_check_run") as mock_create:
            mock_find.return_value = None
            mock_create.return_value = mock_check_run
            
            result = create_or_update_check_run(
                repo="owner/repo",
                name="review-groq",
                head_sha="abc123",
                conclusion="success"
            )
            
            assert result == mock_check_run
            mock_find.assert_called_once_with("owner/repo", "abc123", "review-groq")
            mock_create.assert_called_once()

    def test_create_or_update_check_run_updates_existing(self):
        """Test that create_or_update_check_run updates existing run."""
        existing_run = {"id": 12345, "name": "review-groq"}
        updated_run = {"id": 12345, "name": "review-groq", "conclusion": "success"}
        
        with patch("agents.agent_utils.find_check_run") as mock_find, \
             patch("agents.agent_utils.update_check_run") as mock_update:
            mock_find.return_value = existing_run
            mock_update.return_value = updated_run
            
            result = create_or_update_check_run(
                repo="owner/repo",
                name="review-groq",
                head_sha="abc123",
                conclusion="success"
            )
            
            assert result == updated_run
            mock_find.assert_called_once_with("owner/repo", "abc123", "review-groq")
            mock_update.assert_called_once_with(
                "owner/repo", 12345, "completed", "success", None
            )
