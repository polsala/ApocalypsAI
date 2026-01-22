import os
import json
import random
import sys
import requests

def load_event():
    path = os.getenv('GITHUB_EVENT_PATH')
    if not path:
        raise RuntimeError('GITHUB_EVENT_PATH not set')
    with open(path, 'r') as f:
        return json.load(f)

def get_issue_info(event):
    issue = event.get('issue')
    if not issue:
        raise RuntimeError('No issue in event')
    return issue['number'], issue.get('html_url')

def build_comment(issue_number):
    emojis = ["🚀","🌟","🦄","🤖","🎉","✨","🔥","💫"]
    # Deterministic selection based on issue number
    emoji = emojis[issue_number % len(emojis)]
    return f"{emoji} Welcome to the apocalypse! Thanks for opening this issue."

def post_comment(repo, issue_number, comment, token):
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    data = {"body": comment}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def main():
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise RuntimeError('GITHUB_TOKEN not set')
    repo = os.getenv('GITHUB_REPOSITORY')
    if not repo:
        raise RuntimeError('GITHUB_REPOSITORY not set')
    event = load_event()
    issue_number, _ = get_issue_info(event)
    comment = build_comment(issue_number)
    post_comment(repo, issue_number, comment, token)

if __name__ == "__main__":
    main()
