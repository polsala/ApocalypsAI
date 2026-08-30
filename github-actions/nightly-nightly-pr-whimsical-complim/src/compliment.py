import os
import random
import json
import sys
import urllib.request

COMPLIMENTS = [
    "Your code is poetry in motion!",
    "Looks like you just turned coffee into features!",
    "This PR is a masterpiece of digital craftsmanship.",
    "Your commit messages could win a literary award!",
    "The bugs tremble before your brilliance.",
    "Your pull request radiates pure joy!",
    "If code were music, this would be a symphony.",
    "You just made the repository a happier place.",
    "Your logic is as clear as a mountain lake.",
    "Bravo! This PR deserves a standing ovation."
]

def select_compliment():
    """Return a random compliment from the list."""
    return random.choice(COMPLIMENTS)

def post_comment(repo, pr_number, token, body):
    """Post a comment to the specified PR using the GitHub REST API.

    Args:
        repo (str): "owner/repo" identifier.
        pr_number (int): Pull request number.
        token (str): GitHub token with repo scope.
        body (str): Comment body.
    """
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    data = json.dumps({"body": body}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    with urllib.request.urlopen(req) as resp:
        resp_data = json.load(resp)
    return resp_data

def main():
    # Gather required environment variables
    repo = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("GITHUB_PULL_REQUEST_NUMBER")
    token = os.getenv("GITHUB_TOKEN")
    github_output = os.getenv("GITHUB_OUTPUT")

    if not all([repo, pr_number, token, github_output]):
        print("Missing required environment variables.", file=sys.stderr)
        sys.exit(1)

    compliment = select_compliment()
    comment_body = f"💡 **Compliment:** {compliment}"
    # Post comment (network call may be mocked in tests)
    post_comment(repo, pr_number, token, comment_body)

    # Write output for the composite action
    with open(github_output, "a", encoding="utf-8") as f:
        f.write(f"compliment={compliment}\n")

if __name__ == "__main__":
    main()
