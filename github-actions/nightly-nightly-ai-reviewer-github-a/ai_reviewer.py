import os
import json
import requests
import subprocess
import sys
from typing import Dict, List, Any


class AIReviewer:
    def __init__(self):
        self.api_key = os.environ.get('OPENROUTER_API_KEY')
        self.model = os.environ.get('MODEL', 'anthropic/claude-3-5-sonnet')
        self.max_tokens = int(os.environ.get('MAX_TOKENS', '2000'))
        self.temperature = float(os.environ.get('TEMPERATURE', '0.3'))
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.repository = os.environ.get('GITHUB_REPOSITORY')
        self.event_path = os.environ.get('GITHUB_EVENT_PATH')
        
        if not self.api_key:
            print("Error: OPENROUTER_API_KEY environment variable is required")
            sys.exit(1)
    
    def get_pr_diff(self) -> str:
        """Get the diff of the pull request"""
        try:
            # Get PR number from event
            with open(self.event_path, 'r') as f:
                event = json.load(f)
            
            pr_number = event['pull_request']['number']
            
            # Get diff using git
            diff = subprocess.check_output([
                'git', 'diff',
                f'origin/{event["pull_request"]["base"]["ref"]}',
                f'origin/{event["pull_request"]["head"]["ref"]}'
            ], text=True)
            
            return diff
        except Exception as e:
            print(f"Error getting PR diff: {e}")
            return ""
    
    def analyze_code(self, diff: str) -> str:
        """Analyze code changes using AI"""
        if not diff:
            return "No changes to review."
        
        prompt = f"""
Please review the following code changes and provide feedback:

1. Identify potential bugs or issues
2. Suggest improvements for code quality
3. Check for security vulnerabilities
4. Comment on performance implications
5. Suggest best practices

Code changes:
{diff}

Please provide a concise, actionable review focusing on the most important issues.
"""
        
        try:
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': self.model,
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': self.max_tokens,
                    'temperature': self.temperature
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                return f"Error: API request failed with status {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def post_review_comment(self, comment: str):
        """Post review comment to GitHub PR"""
        try:
            with open(self.event_path, 'r') as f:
                event = json.load(f)
            
            pr_number = event['pull_request']['number']
            
            response = requests.post(
                f'https://api.github.com/repos/{self.repository}/issues/{pr_number}/comments',
                headers={
                    'Authorization': f'token {self.github_token}',
                    'Accept': 'application/vnd.github.v3+json'
                },
                json={'body': comment}
            )
            
            if response.status_code == 201:
                print("Successfully posted review comment")
                # Set output for GitHub Actions
                print(f"::set-output name=comment::{comment[:200]}...")
            else:
                print(f"Failed to post comment: {response.status_code}")
        except Exception as e:
            print(f"Error posting comment: {str(e)}")
    
    def run(self):
        """Main execution method"""
        print("🤖 AI Code Reviewer starting...")
        
        # Get PR diff
        diff = self.get_pr_diff()
        print(f"📄 Analyzing {len(diff)} characters of changes...")
        
        # Analyze code
        review = self.analyze_code(diff)
        print("✅ Review completed")
        
        # Post review comment
        self.post_review_comment(review)
        
        return review


if __name__ == '__main__':
    reviewer = AIReviewer()
    review = reviewer.run()
    print("\n" + "="*50)
    print("AI REVIEW SUMMARY:")
    print("="*50)
    print(review)
    print("="*50)
