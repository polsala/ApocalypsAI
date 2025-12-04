from __future__ import annotations

import os
from typing import Any, Dict

import requests

GITHUB_API = "https://api.github.com"


class GitHubError(RuntimeError):
    """Raised when GitHub API requests fail."""


def _headers(use_reviewer_token: bool = False) -> Dict[str, str]:
    """Get headers for GitHub API requests.
    
    Args:
        use_reviewer_token: If True, use REVIWER_TOKEN instead of GITHUB_TOKEN.
                           This is used for PR approvals to allow a secondary
                           account to approve PRs.
    
    Returns:
        Dict with Authorization and other headers
    """
    if use_reviewer_token:
        token = os.environ.get("REVIWER_TOKEN")
        if not token:
            raise GitHubError("Missing REVIWER_TOKEN environment variable")
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise GitHubError("Missing GITHUB_TOKEN environment variable")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _request(method: str, path: str, *, json: Dict[str, Any] | None = None, use_reviewer_token: bool = False) -> Any:
    """Make a request to the GitHub API.
    
    Args:
        method: HTTP method (GET, POST, PUT, etc.)
        path: API path
        json: Optional JSON payload
        use_reviewer_token: If True, use REVIWER_TOKEN for authentication
    
    Returns:
        Response JSON or None for 204 responses
    """
    url = f"{GITHUB_API}{path}"
    response = requests.request(method, url, headers=_headers(use_reviewer_token), json=json, timeout=30.0)
    if response.status_code >= 400:
        raise GitHubError(f"{method} {path} failed: {response.status_code} {response.text}")
    if response.status_code == 204:
        return None
    return response.json()


def get_issue(repo: str, number: int) -> Dict[str, Any]:
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/issues/{number}"
    return _request("GET", path)


def get_pr(repo: str, number: int) -> Dict[str, Any]:
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/pulls/{number}"
    return _request("GET", path)


def post_issue_comment(repo: str, number: int, body: str) -> None:
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/issues/{number}/comments"
    _request("POST", path, json={"body": body})


def post_pr_comment(repo: str, number: int, body: str) -> None:
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/issues/{number}/comments"
    _request("POST", path, json={"body": body})


def add_issue_labels(repo: str, number: int, labels: list[str]) -> None:
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/issues/{number}/labels"
    _request("POST", path, json={"labels": labels})


def get_issue_comments(repo: str, number: int) -> list[Dict[str, Any]]:
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/issues/{number}/comments"
    return _request("GET", path)


def get_pr_files(repo: str, number: int) -> list[Dict[str, Any]]:
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/pulls/{number}/files"
    return _request("GET", path)


def get_pr_diff(repo: str, number: int) -> str:
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/pulls/{number}"
    url = f"{GITHUB_API}{path}"
    response = requests.get(
        url,
        headers={**_headers(), "Accept": "application/vnd.github.v3.diff"},
        timeout=30.0,
    )
    if response.status_code >= 400:
        raise GitHubError(f"GET {path} diff failed: {response.status_code} {response.text}")
    return response.text


def create_pr_review(repo: str, number: int, body: str, event: str = "COMMENT", use_reviewer_token: bool = False) -> None:
    """Create a PR review with the given body and event type.
    
    Args:
        repo: Repository in 'owner/name' format
        number: PR number
        body: Review comment body
        event: One of 'APPROVE', 'REQUEST_CHANGES', 'COMMENT'
        use_reviewer_token: If True, use REVIWER_TOKEN for authentication
    """
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/pulls/{number}/reviews"
    _request("POST", path, json={"body": body, "event": event}, use_reviewer_token=use_reviewer_token)


def approve_pr(repo: str, number: int, body: str = "Auto-approved by AI agent", use_reviewer_token: bool = True) -> None:
    """Approve a pull request.
    
    Args:
        repo: Repository in 'owner/name' format
        number: PR number
        body: Approval message
        use_reviewer_token: If True, use REVIWER_TOKEN for authentication (default: True)
    """
    create_pr_review(repo, number, body, "APPROVE", use_reviewer_token=use_reviewer_token)


def merge_pr(repo: str, number: int, merge_method: str = "squash") -> None:
    """Merge a pull request.
    
    Args:
        repo: Repository in 'owner/name' format
        number: PR number
        merge_method: One of 'merge', 'squash', 'rebase'
    """
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/pulls/{number}/merge"
    _request("PUT", path, json={"merge_method": merge_method})


def enable_auto_merge_old(repo: str, number: int, merge_method: str = "squash") -> None:
    """Enable auto-merge for a pull request.
    
    This allows the PR to be automatically merged once all branch protection
    requirements are satisfied (approvals, status checks, etc.).
    
    Args:
        repo: Repository in 'owner/name' format
        number: PR number
        merge_method: One of 'MERGE', 'SQUASH', 'REBASE' (uppercase for GraphQL)
    """
    # First, get the PR node ID (required for GraphQL mutation)
    pr_data = get_pr(repo, number)
    pr_node_id = pr_data.get("node_id")
    
    if not pr_node_id:
        raise GitHubError(f"Could not get node_id for PR #{number}")
    
    # GraphQL mutation to enable auto-merge
    mutation = """
    mutation EnableAutoMerge($pullRequestId: ID!, $mergeMethod: PullRequestMergeMethod!) {
      enablePullRequestAutoMerge(input: {pullRequestId: $pullRequestId, mergeMethod: $mergeMethod}) {
        pullRequest {
          id
          autoMergeRequest {
            enabledAt
            mergeMethod
          }
        }
      }
    }
    """
    
    variables = {
        "pullRequestId": pr_node_id,
        "mergeMethod": merge_method.upper()
    }
    
    # Make GraphQL request
    graphql_url = "https://api.github.com/graphql"
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise GitHubError("Missing GITHUB_TOKEN environment variable")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    response = requests.post(
        graphql_url,
        headers=headers,
        json={"query": mutation, "variables": variables},
        timeout=30.0
    )
    
    if response.status_code >= 400:
        raise GitHubError(f"GraphQL mutation failed: {response.status_code} {response.text}")
    
    result = response.json()
    if "errors" in result:
        raise GitHubError(f"GraphQL errors: {result['errors']}")
    

def merge_pr(repo: str, number: int, merge_method: str = "squash") -> None:
    """Merge a pull request immediately (no auto-merge).

    Args:
        repo: Repository in 'owner/name' format
        number: PR number
        merge_method: One of 'MERGE', 'SQUASH', 'REBASE' (case-insensitive)
    """
    # 1) Get PR node ID for GraphQL
    pr_data = get_pr(repo, number)  # assuming you already have this helper
    pr_node_id = pr_data.get("node_id")

    if not pr_node_id:
        raise GitHubError(f"Could not get node_id for PR #{number}")

    # 2) GraphQL mutation to merge the PR *now*
    mutation = """
    mutation MergePullRequest($pullRequestId: ID!, $mergeMethod: PullRequestMergeMethod!) {
      mergePullRequest(input: {pullRequestId: $pullRequestId, mergeMethod: $mergeMethod}) {
        pullRequest {
          id
          merged
          mergedAt
          mergeCommit {
            oid
          }
        }
      }
    }
    """

    variables = {
        "pullRequestId": pr_node_id,
        "mergeMethod": merge_method.upper(),  # MERGE / SQUASH / REBASE
    }

    graphql_url = "https://api.github.com/graphql"
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise GitHubError("Missing GITHUB_TOKEN environment variable")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        graphql_url,
        headers=headers,
        json={"query": mutation, "variables": variables},
        timeout=30.0,
    )

    if response.status_code >= 400:
        raise GitHubError(f"GraphQL mutation failed: {response.status_code} {response.text}")

    result = response.json()
    if "errors" in result:
        raise GitHubError(f"GraphQL errors: {result['errors']}")

    merge_info = (
        result.get("data", {})
        .get("mergePullRequest", {})
        .get("pullRequest", {})
    )

    if not merge_info or not merge_info.get("merged"):
        raise GitHubError(f"PR #{number} was not merged: {merge_info}")

enable_auto_merge = merge_pr


def get_pr_reviews(repo: str, number: int) -> list[Dict[str, Any]]:
    """Get all reviews for a pull request.
    
    Args:
        repo: Repository in 'owner/name' format
        number: PR number
        
    Returns:
        List of review objects
    """
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/pulls/{number}/reviews"
    return _request("GET", path)


def is_pr_approved(repo: str, number: int) -> bool:
    """Check if a pull request is already approved.
    
    Args:
        repo: Repository in 'owner/name' format
        number: PR number
        
    Returns:
        True if the PR has at least one approval, False otherwise
    """
    reviews = get_pr_reviews(repo, number)
    # Check if any review has state "APPROVED"
    # Note: GitHub tracks the latest review per user, so we just need to check if any is APPROVED
    for review in reviews:
        if review.get("state") == "APPROVED":
            return True
    return False


def get_commit_status(repo: str, ref: str) -> Dict[str, Any]:
    """Get combined status for a commit/ref.
    
    Args:
        repo: Repository in 'owner/name' format
        ref: Git commit SHA, branch name, or tag
        
    Returns:
        Combined status object with state and statuses
    """
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/commits/{ref}/status"
    return _request("GET", path)


def get_check_runs(repo: str, ref: str) -> Dict[str, Any]:
    """Get check runs for a commit/ref.
    
    Args:
        repo: Repository in 'owner/name' format
        ref: Git commit SHA, branch name, or tag
        
    Returns:
        Check runs object with total_count and check_runs list
    """
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/commits/{ref}/check-runs"
    return _request("GET", path)


def list_open_prs(repo: str) -> list[Dict[str, Any]]:
    """List all open pull requests in a repository.
    
    Args:
        repo: Repository in 'owner/name' format
        
    Returns:
        List of PR objects
    """
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/pulls?state=open"
    return _request("GET", path)


def get_branch_protection(repo: str, branch: str) -> Dict[str, Any] | None:
    """Get branch protection rules for a branch.
    
    Args:
        repo: Repository in 'owner/name' format
        branch: Branch name
        
    Returns:
        Branch protection object or None if not protected
    """
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/branches/{branch}/protection"
    try:
        return _request("GET", path)
    except GitHubError:
        # Branch might not be protected, return None
        return None


def get_required_status_checks(repo: str, branch: str) -> list[str]:
    """Get list of required status check contexts for a branch.
    
    Args:
        repo: Repository in 'owner/name' format
        branch: Branch name
        
    Returns:
        List of required status check context names
    """
    protection = get_branch_protection(repo, branch)
    if not protection:
        return []
    
    required_checks = protection.get("required_status_checks", {})
    if not required_checks:
        return []
    
    # Get the contexts (check names)
    contexts = required_checks.get("contexts", [])
    # Also get checks from the newer checks array
    checks = required_checks.get("checks", [])
    
    # Combine both formats, filtering out empty strings
    check_names = set(c for c in contexts if c)
    for check in checks:
        context = check.get("context", "")
        if context:  # Only add non-empty contexts
            check_names.add(context)
    
    return list(check_names)
