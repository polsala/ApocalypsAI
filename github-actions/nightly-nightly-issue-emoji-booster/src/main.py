import os
import json
import random
import sys
import requests

EMOJIS = ["+1", "heart", "rocket", "tada", "eyes", "sparkles", "thumbsup", "clap"]

def main():
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not token or not repo or not event_path:
        print("Missing required environment variables.", file=sys.stderr)
        sys.exit(1)
    with open(event_path, "r") as f:
        event = json.load(f)
    issue = event.get("issue")
    if not issue:
        print("No issue data in event.", file=sys.stderr)
        sys.exit(0)
    issue_number = issue["number"]
    emoji = random.choice(EMOJIS)
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/reactions"
    headers = {
        "Accept": "application/vnd.github.squirrel-girl-preview+json",
        "Authorization": f"token {token}"
    }
    data = {"content": emoji}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Added reaction :{emoji}: to issue #{issue_number}")
    else:
        print(f"Failed to add reaction: {response.status_code} {response.text}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
