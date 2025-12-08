import os
import requests
import datetime
from typing import Dict, List

MOCK_DATA = {
    'prs': 14,
    'contributors': 7,
    'issues_closed': 22,
    'milestones': ['Survival Kit', 'Chaos Protocol']
}

def get_repo_stats() -> Dict:
    """Fetches real stats in production, returns mock data in tests"""
    if os.getenv('MOCK_ENV') == 'true':
        return MOCK_DATA
    
    # Actual GitHub API calls would go here
    # Example: Get PRs, contributors, etc.
    return {
        'prs': 0,
        'contributors': 0,
        'issues_closed': 0,
        'milestones': []
    }

def generate_echo_text(stats: Dict) -> str:
    now = datetime.datetime.now().strftime('%B %Y')
    return f"""
🌟 **ApocalypsAI Monthly Echo - {now}**

- 🛠️ **PRs Merged**: {stats['prs']}
- 🌍 **Contributors**: {stats['contributors']}
- 🧹 **Issues Closed**: {stats['issues_closed']}
- 🎯 **Milestones Achieved**: {', '.join(stats['milestones']) if stats['milestones'] else 'None'}

*The wasteland whispers: 'Keep building, keep surviving!'*
"""

if __name__ == "__main__":
    stats = get_repo_stats()
    print(generate_echo_text(stats))
    
    # In production, this would create a GitHub issue
    # if 'create_issue' in sys.argv:
    #     create_github_issue(stats)
    #     print('✅ Created summary issue')
    # else:
    #     print('ℹ️  Use `create_issue` argument to post to GitHub')
