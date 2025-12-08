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
    
    Fetches up to 200 open PRs by paginating through 2 pages of 100 PRs each.
    
    Args:
        repo: Repository in 'owner/name' format
        
    Returns:
        List of PR objects (up to 200)
    """
    owner, name = repo.split("/", 1)
    prs = []
    for page in range(1, 3):
        path = f"/repos/{owner}/{name}/pulls?state=open&per_page=100&page={page}"
        prs_page = _request("GET", path)
        if not prs_page:
            break
        prs += prs_page
        if len(prs_page) < 100:
            break
    return prs


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


def create_check_run(
    repo: str,
    name: str,
    head_sha: str,
    status: str = "completed",
    conclusion: str | None = None,
    output: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Create a check run for a commit.
    
    Args:
        repo: Repository in 'owner/name' format
        name: Name of the check (e.g., 'review-groq')
        head_sha: The SHA of the commit
        status: The current status ('queued', 'in_progress', 'completed')
        conclusion: Required if status is 'completed'. One of:
                   'action_required', 'cancelled', 'failure', 'neutral',
                   'success', 'skipped', 'stale', 'timed_out'
        output: Optional output object with title, summary, text
        
    Returns:
        The created check run object
    """
    owner, name_part = repo.split("/", 1)
    path = f"/repos/{owner}/{name_part}/check-runs"
    
    payload: Dict[str, Any] = {
        "name": name,
        "head_sha": head_sha,
        "status": status,
    }
    
    if conclusion is not None:
        payload["conclusion"] = conclusion
    
    if output is not None:
        payload["output"] = output
    
    return _request("POST", path, json=payload)


def update_check_run(
    repo: str,
    check_run_id: int,
    status: str = "completed",
    conclusion: str | None = None,
    output: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Update an existing check run.
    
    Args:
        repo: Repository in 'owner/name' format
        check_run_id: ID of the check run to update
        status: The current status ('queued', 'in_progress', 'completed')
        conclusion: Required if status is 'completed'. One of:
                   'action_required', 'cancelled', 'failure', 'neutral',
                   'success', 'skipped', 'stale', 'timed_out'
        output: Optional output object with title, summary, text
        
    Returns:
        The updated check run object
    """
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/check-runs/{check_run_id}"
    
    payload: Dict[str, Any] = {
        "status": status,
    }
    
    if conclusion is not None:
        payload["conclusion"] = conclusion
    
    if output is not None:
        payload["output"] = output
    
    return _request("PATCH", path, json=payload)


def find_check_run(repo: str, head_sha: str, check_name: str) -> Dict[str, Any] | None:
    """Find a check run by name for a given commit.
    
    Args:
        repo: Repository in 'owner/name' format
        head_sha: The SHA of the commit
        check_name: Name of the check to find
        
    Returns:
        The check run object if found, None otherwise
    """
    check_runs_data = get_check_runs(repo, head_sha)
    runs = check_runs_data.get("check_runs", [])
    
    for run in runs:
        if run.get("name") == check_name:
            return run
    
    return None


def create_or_update_check_run(
    repo: str,
    name: str,
    head_sha: str,
    status: str = "completed",
    conclusion: str | None = "success",
    output: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Create a new check run or update an existing one.
    
    This is a convenience function that checks if a check run exists
    and either updates it or creates a new one.
    
    Args:
        repo: Repository in 'owner/name' format
        name: Name of the check (e.g., 'review-groq')
        head_sha: The SHA of the commit
        status: The current status ('queued', 'in_progress', 'completed')
        conclusion: Required if status is 'completed'. One of:
                   'action_required', 'cancelled', 'failure', 'neutral',
                   'success', 'skipped', 'stale', 'timed_out'
        output: Optional output object with title, summary, text
        
    Returns:
        The created or updated check run object
    """
    existing_run = find_check_run(repo, head_sha, name)
    
    if existing_run:
        check_run_id = existing_run.get("id")
        if check_run_id:
            return update_check_run(repo, check_run_id, status, conclusion, output)
    
    return create_check_run(repo, name, head_sha, status, conclusion, output)


def close_pr(repo: str, number: int, comment: str | None = None) -> None:
    """Close a pull request.
    
    Args:
        repo: Repository in 'owner/name' format
        number: PR number
        comment: Optional comment to post before closing
    """
    if comment:
        post_pr_comment(repo, number, comment)
    
    owner, name = repo.split("/", 1)
    path = f"/repos/{owner}/{name}/pulls/{number}"
    _request("PATCH", path, json={"state": "closed"})


def _graphql_request(query: str, variables: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Make a GraphQL request to GitHub API.
    
    Args:
        query: GraphQL query or mutation
        variables: Optional variables for the query
        
    Returns:
        Response data
    """
    graphql_url = "https://api.github.com/graphql"
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise GitHubError("Missing GITHUB_TOKEN environment variable")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload: Dict[str, Any] = {"query": query}
    if variables:
        payload["variables"] = variables
    
    response = requests.post(graphql_url, headers=headers, json=payload, timeout=30.0)
    
    if response.status_code >= 400:
        raise GitHubError(f"GraphQL request failed: {response.status_code} {response.text}")
    
    result = response.json()
    if "errors" in result:
        raise GitHubError(f"GraphQL errors: {result['errors']}")
    
    return result.get("data", {})


def get_discussion(repo: str, discussion_number: int) -> Dict[str, Any]:
    """Get a discussion by number.
    
    Args:
        repo: Repository in 'owner/name' format
        discussion_number: Discussion number
        
    Returns:
        Discussion object with id, title, body, category, author, etc.
    """
    owner, name = repo.split("/", 1)
    
    query = """
    query GetDiscussion($owner: String!, $name: String!, $number: Int!) {
      repository(owner: $owner, name: $name) {
        discussion(number: $number) {
          id
          number
          title
          body
          category {
            id
            name
            emoji
          }
          author {
            login
          }
          createdAt
          updatedAt
        }
      }
    }
    """
    
    variables = {
        "owner": owner,
        "name": name,
        "number": discussion_number
    }
    
    data = _graphql_request(query, variables)
    discussion = data.get("repository", {}).get("discussion")
    if not discussion:
        raise GitHubError(f"Discussion #{discussion_number} not found")
    return discussion


def get_discussion_comments(repo: str, discussion_id: str, limit: int = 20) -> list[Dict[str, Any]]:
    """Get comments for a discussion.
    
    Args:
        repo: Repository in 'owner/name' format
        discussion_id: Discussion GraphQL node ID
        limit: Maximum number of comments to fetch
        
    Returns:
        List of comment objects
    """
    query = """
    query GetDiscussionComments($discussionId: ID!, $limit: Int!) {
      node(id: $discussionId) {
        ... on Discussion {
          comments(first: $limit) {
            nodes {
              id
              body
              author {
                login
              }
              createdAt
              replies(first: 10) {
                nodes {
                  id
                  body
                  author {
                    login
                  }
                  createdAt
                }
              }
            }
          }
        }
      }
    }
    """
    
    variables = {
        "discussionId": discussion_id,
        "limit": limit
    }
    
    data = _graphql_request(query, variables)
    comments = data.get("node", {}).get("comments", {}).get("nodes", [])
    return comments


def post_discussion_comment(discussion_id: str, body: str) -> Dict[str, Any]:
    """Post a comment to a discussion.
    
    Args:
        discussion_id: Discussion GraphQL node ID
        body: Comment body (markdown)
        
    Returns:
        Created comment object
    """
    mutation = """
    mutation AddDiscussionComment($discussionId: ID!, $body: String!) {
      addDiscussionComment(input: {discussionId: $discussionId, body: $body}) {
        comment {
          id
          body
          createdAt
        }
      }
    }
    """
    
    variables = {
        "discussionId": discussion_id,
        "body": body
    }
    
    data = _graphql_request(mutation, variables)
    comment = data.get("addDiscussionComment", {}).get("comment")
    if not comment:
        raise GitHubError("Failed to create discussion comment")
    return comment


def post_discussion_comment_reply(comment_id: str, body: str) -> Dict[str, Any]:
    """Reply to a discussion comment.
    
    Args:
        comment_id: Comment GraphQL node ID to reply to
        body: Reply body (markdown)
        
    Returns:
        Created reply object
    """
    mutation = """
    mutation AddDiscussionCommentReply($commentId: ID!, $body: String!) {
      addDiscussionComment(input: {discussionId: $commentId, body: $body}) {
        comment {
          id
          body
          createdAt
        }
      }
    }
    """
    
    variables = {
        "commentId": comment_id,
        "body": body
    }
    
    data = _graphql_request(mutation, variables)
    reply = data.get("addDiscussionComment", {}).get("comment")
    if not reply:
        raise GitHubError("Failed to create discussion comment reply")
    return reply
