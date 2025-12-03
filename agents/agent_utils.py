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
