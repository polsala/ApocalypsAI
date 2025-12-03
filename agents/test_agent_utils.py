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
        """Test that enable_auto_merge successfully enables auto-merge via GraphQL."""
        mock_pr_data = {"node_id": "PR_kwDOABCDEF12345"}
        mock_graphql_response = {
            "data": {
                "enablePullRequestAutoMerge": {
                    "pullRequest": {
                        "id": "PR_kwDOABCDEF12345",
                        "autoMergeRequest": {
                            "enabledAt": "2024-01-01T00:00:00Z",
                            "mergeMethod": "SQUASH"
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
            
            # Verify GraphQL mutation was called
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
