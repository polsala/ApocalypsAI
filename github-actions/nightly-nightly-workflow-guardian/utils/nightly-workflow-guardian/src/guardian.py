import os
import requests
import json
from datetime import datetime, timedelta

# Mock rationale: These are placeholder values for testing purposes.
# In a real scenario, these would be dynamically fetched or configured.
GITHUB_API_URL = os.environ.get('GITHUB_API_URL', 'https://api.github.com')
REPO_OWNER = os.environ.get('REPO_OWNER', 'polsala')
REPO_NAME = os.environ.get('REPO_NAME', 'ApocalypsAI')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', 'mock_github_token')

# Mock rationale: This mock allows testing the API call without actual network requests.
# The actual implementation would use requests.get.
class MockResponse:
    def __init__(self, json_data, status_code):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP Error: {self.status_code}")

def mock_requests_get(url, headers):
    print(f"Mock GET request to: {url}")
    if "/actions/runs" in url:
        # Mock response for workflow runs
        return MockResponse({
            "workflow_runs": [
                {
                    "id": 12345,
                    "name": "Build and Test",
                    "status": "completed",
                    "conclusion": "success",
                    "created_at": (datetime.utcnow() - timedelta(hours=1)).isoformat() + 'Z',
                    "html_url": "http://example.com/run/12345"
                },
                {
                    "id": 12346,
                    "name": "Deploy to Staging",
                    "status": "completed",
                    "conclusion": "failure",
                    "created_at": (datetime.utcnow() - timedelta(hours=2)).isoformat() + 'Z',
                    "html_url": "http://example.com/run/12346"
                },
                {
                    "id": 12347,
                    "name": "Linting",
                    "status": "completed",
                    "conclusion": "success",
                    "created_at": (datetime.utcnow() - timedelta(hours=3)).isoformat() + 'Z',
                    "html_url": "http://example.com/run/12347"
                }
            ]
        }, 200)
    return MockResponse({}, 404)


def get_recent_workflow_runs():
    """Fetches recent workflow runs from the GitHub API."""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    # Fetch runs from the last 24 hours
    since = (datetime.utcnow() - timedelta(days=1)).isoformat() + 'Z'
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs?since={since}"
    
    # Use mock_requests_get for testing, replace with requests.get for actual execution
    # response = requests.get(url, headers=headers)
    response = mock_requests_get(url, headers=headers)
    
    response.raise_for_status() # Raise an exception for bad status codes
    return response.json()['workflow_runs']

def analyze_workflow_health(runs):
    """Analyzes workflow runs for potential issues."""
    failed_runs = []
    for run in runs:
        if run['status'] == 'completed' and run['conclusion'] == 'failure':
            failed_runs.append(run)
    
    if failed_runs:
        message = f"Found {len(failed_runs)} failed workflow run(s) in the last 24 hours:\n"
        for run in failed_runs:
            message += f"- Workflow: {run['name']} (ID: {run['id']}) - Status: {run['conclusion']} - Link: {run['html_url']}\n"
        return "failure", message
    else:
        return "success", "All workflows executed successfully in the last 24 hours."

def main():
    try:
        runs = get_recent_workflow_runs()
        status, message = analyze_workflow_health(runs)
        print(f"Workflow Guardian Status: {status}")
        print(f"Message: {message}")
        
        # Output for GitHub Actions
        print(f"::set-output name=status::{status}")
        print(f"::set-output name=message::{message}")

    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching workflow runs: {e}"
        print(f"Workflow Guardian Status: failure")
        print(f"Message: {error_message}")
        print(f"::set-output name=status::failure")
        print(f"::set-output name=message::{error_message}")
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(f"Workflow Guardian Status: failure")
        print(f"Message: {error_message}")
        print(f"::set-output name=status::failure")
        print(f"::set-output name=message::{error_message}")

if __name__ == "__main__":
    main()
