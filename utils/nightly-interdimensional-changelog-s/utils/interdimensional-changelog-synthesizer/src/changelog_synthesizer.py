import subprocess
import sys
from collections import defaultdict

def _run_git_command(command):
    """Helper to run git commands and capture output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            cwd='.', # Ensure it runs in the current directory (repo root)
            encoding='utf-8'
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {' '.join(command)}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'git' command not found. Please ensure Git is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)

def synthesize_changelog(start_ref: str, end_ref: str) -> str:
    """
    Synthesizes a human-readable changelog from Git commit messages
    between two specified references.
    """
    git_log_command = [
        'git', 'log',
        '--pretty=format:%s%n%b', # Subject line, then body
        f'{start_ref}..{end_ref}'
    ]
    
    log_output = _run_git_command(git_log_command)
    
    if not log_output:
        return f"# Changelog from {start_ref} to {end_ref}\n\nNo commits found in this range or log is empty."

    commits = log_output.split('\n\n') # Split by double newline for commit separation
    
    categorized_commits = defaultdict(list)
    
    # Define mapping for conventional commit types to display names
    commit_type_map = {
        'feat': 'Features',
        'fix': 'Bug Fixes',
        'chore': 'Chores',
        'docs': 'Documentation',
        'refactor': 'Refactoring',
        'perf': 'Performance Improvements',
        'test': 'Tests',
        'build': 'Build System',
        'ci': 'CI/CD',
        'revert': 'Reverts'
    }

    for commit_message in commits:
        if not commit_message.strip():
            continue

        first_line = commit_message.split('\n')[0].strip()
        
        # Try to parse conventional commit type
        matched_type = 'Other Changes'
        for prefix, display_name in commit_type_map.items():
            if first_line.startswith(f'{prefix}:') or first_line.startswith(f'{prefix}('):
                matched_type = display_name
                break
        
        categorized_commits[matched_type].append(first_line)

    output = [f"# Changelog from {start_ref} to {end_ref}", ""]

    # Order of categories for consistent output
    ordered_categories = [
        'Features', 'Bug Fixes', 'Performance Improvements', 'Refactoring',
        'Documentation', 'Build System', 'CI/CD', 'Tests', 'Chores', 'Reverts',
        'Other Changes'
    ]

    for category in ordered_categories:
        if categorized_commits[category]:
            output.append(f"## {category}")
            for commit in sorted(categorized_commits[category]): # Sort for deterministic output
                output.append(f"*   {commit}")
            output.append("") # Add a blank line after each category

    return '\n'.join(output).strip()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python src/changelog_synthesizer.py <start_ref> <end_ref>", file=sys.stderr)
        sys.exit(1)
    
    start_ref = sys.argv[1]
    end_ref = sys.argv[2]
    
    changelog = synthesize_changelog(start_ref, end_ref)
    print(changelog)
