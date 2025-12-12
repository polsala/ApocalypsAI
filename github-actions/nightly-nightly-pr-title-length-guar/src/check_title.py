import json
import os
import sys

def load_event(event_path: str) -> dict:
    """Load the GitHub event JSON from the given path."""
    with open(event_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_pr_title(event: dict) -> str:
    """Extract the pull request title from the event payload.
    Supports both `pull_request` and `pull_request_target` events.
    """
    pr = event.get("pull_request") or event.get("pull_request_target")
    if not pr:
        raise ValueError("No pull request information found in event payload.")
    title = pr.get("title")
    if title is None:
        raise ValueError("Pull request title missing in payload.")
    return title

def main(max_length_str: str) -> None:
    max_length = int(max_length_str)
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        print("::error::GITHUB_EVENT_PATH not set. Cannot read event payload.")
        sys.exit(1)
    try:
        event = load_event(event_path)
        title = get_pr_title(event)
    except Exception as e:
        print(f"::error::{e}")
        sys.exit(1)
    title_len = len(title)
    if title_len > max_length:
        print(f"::error::PR title is too long ({title_len} > {max_length} characters).")
        print(f"Title: '{title}'")
        sys.exit(1)
    else:
        print(f"PR title length check passed ({title_len}/{max_length} characters).")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: check_title.py <max-length>")
        sys.exit(1)
    main(sys.argv[1])
