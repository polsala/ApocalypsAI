import subprocess
import argparse
import re
import os
from datetime import datetime

def run_git_log(count=None, since=None, until=None):
    """Runs git log and returns its output."""
    cmd = [
        'git',
        'log',
        '--pretty=format:"%h|%an|%s"',
        '--no-merges'
    ]

    if count:
        cmd.append(f'-{count}')
    if since:
        cmd.append(f'--since="{since}"')
    if until:
        cmd.append(f'--until="{until}"')

    try:
        # Mock rationale: subprocess.run is mocked in tests to avoid actual git calls.
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=os.getcwd())
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running git log: {e}")
        print(f"Stderr: {e.stderr}")
        return ""
    except FileNotFoundError:
        print("Error: 'git' command not found. Please ensure Git is installed and in your PATH.")
        return ""

def parse_commit_log(log_output):
    """Parses git log output into a list of commit dictionaries."""
    commits = []
    for line in log_output.strip().split('\n'):
        if not line:
            continue
        try:
            parts = line.split('|', 2)
            if len(parts) == 3:
                commit_hash, author, message = parts
                commits.append({
                    'hash': commit_hash.strip(),
                    'author': author.strip(),
                    'message': message.strip()
                })
        except ValueError:
            # Skip malformed lines
            continue
    return commits

def categorize_commits(commits):
    """Categorizes commits based on conventional commit prefixes."""
    categories = {
        'feat': {'title': '✨ Features', 'commits': []},
        'fix': {'title': '🐛 Bug Fixes', 'commits': []},
        'docs': {'title': '📚 Documentation', 'commits': []},
        'chore': {'title': '🧹 Chores', 'commits': []},
        'refactor': {'title': '🔨 Refactors', 'commits': []},
        'perf': {'title': '⚡ Performance', 'commits': []},
        'test': {'title': '🧪 Tests', 'commits': []},
        'build': {'title': '📦 Builds', 'commits': []},
        'ci': {'title': '⚙️ CI/CD', 'commits': []},
        'revert': {'title': '⏪ Reverts', 'commits': []},
        'style': {'title': '🎨 Styles', 'commits': []},
        'other': {'title': '📝 Other Changes', 'commits': []},
    }

    for commit in commits:
        message = commit['message']
        match = re.match(r'^(feat|fix|docs|chore|refactor|perf|test|build|ci|revert|style)(\([^)]+\))?:\s*(.*)', message, re.IGNORECASE)
        if match:
            commit_type = match.group(1).lower()
            description = match.group(3).strip()
            commit['description'] = description
            categories[commit_type]['commits'].append(commit)
        else:
            commit['description'] = message # Use full message if no conventional prefix
            categories['other']['commits'].append(commit)
    return categories

def format_markdown_output(categorized_commits):
    """Formats the categorized commits into a Markdown string."""
    output = ["# Commit Chronicle\n"]

    # Define order of categories for consistent output
    category_order = ['feat', 'fix', 'docs', 'refactor', 'perf', 'test', 'build', 'ci', 'revert', 'style', 'chore', 'other']

    for category_key in category_order:
        category = categorized_commits[category_key]
        if category['commits']:
            output.append(f"## {category['title']}\n")
            for commit in category['commits']:
                output.append(f"*   `{commit['hash']}` ({commit['author']}) {commit['description']}\n")
            output.append("\n") # Add an extra newline for spacing between categories

    return "".join(output)

def main():
    parser = argparse.ArgumentParser(
        description="Summarize recent Git commit messages into a categorized chronicle."
    )
    parser.add_argument(
        '--count', type=int, default=10,
        help="Summarize the last N commits. Defaults to 10."
    )
    parser.add_argument(
        '--since', type=str,
        help="Summarize commits since a specific date (e.g., '2023-01-01')."
    )
    parser.add_argument(
        '--until', type=str,
        help="Summarize commits until a specific date (e.g., '2023-12-31')."
    )
    parser.add_argument(
        '--format', type=str, default='markdown',
        choices=['markdown'],
        help="Output format. Currently only 'markdown' is supported."
    )

    args = parser.parse_args()

    # Validate date formats if provided
    if args.since:
        try:
            datetime.strptime(args.since, '%Y-%m-%d')
        except ValueError:
            print("Error: --since date must be in YYYY-MM-DD format.")
            return
    if args.until:
        try:
            datetime.strptime(args.until, '%Y-%m-%d')
        except ValueError:
            print("Error: --until date must be in YYYY-MM-DD format.")
            return

    log_output = run_git_log(count=args.count, since=args.since, until=args.until)
    if not log_output:
        print("No git log output or an error occurred.")
        return

    commits = parse_commit_log(log_output)
    if not commits:
        print("No commits found matching the criteria.")
        return

    categorized = categorize_commits(commits)
    if args.format == 'markdown':
        print(format_markdown_output(categorized))
    else:
        print(f"Unsupported format: {args.format}")

if __name__ == '__main__':
    main()
