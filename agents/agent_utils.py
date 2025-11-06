from __future__ import annotations

import os
from typing import Any, Dict

import requests

GITHUB_API = "https://api.github.com"


class GitHubError(RuntimeError):
    """Raised when GitHub API requests fail."""


def _headers() -> Dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise GitHubError("Missing GITHUB_TOKEN environment variable")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _request(method: str, path: str, *, json: Dict[str, Any] | None = None) -> Any:
    url = f"{GITHUB_API}{path}"
    response = requests.request(method, url, headers=_headers(), json=json, timeout=30.0)
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
