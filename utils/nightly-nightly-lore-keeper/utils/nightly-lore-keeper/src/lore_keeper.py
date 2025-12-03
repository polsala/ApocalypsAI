import subprocess
import sys
import re
from typing import List, Dict, Any

def get_recent_commit_messages(num_commits: int = 10) -> List[str]:
    """
    Retrieves the raw commit messages for the last N non-merge commits.
    Each message includes subject and body, separated by a blank line.
    """
    try:
        # Using --pretty=format:%B%x00 to get full raw commit message (subject + body)
        # and separate individual commits with a null byte (%x00).
        # -n N to limit to N commits
        # --no-merges to exclude merge commits
        result = subprocess.run(
            ['git', 'log', f'-n{num_commits}', '--no-merges', '--pretty=format:%B%x00'],
            capture_output=True, text=True, check=True, encoding='utf-8'
        )
        # Split by null byte and filter out empty strings
        messages = [msg.strip() for msg in result.stdout.split('\x00') if msg.strip()]
        return messages
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print("Git command not found. Please ensure Git is installed and in your PATH.", file=sys.stderr)
        return []

def parse_commit_message(raw_message: str) -> Dict[str, str]:
    """Parses a raw commit message into subject and body."""
    parts = raw_message.split('\n', 1)
    subject = parts[0].strip()
    body = parts[1].strip() if len(parts) > 1 else ''
    return {'subject': subject, 'body': body, 'raw': raw_message}

def check_commit_message(
    commit_data: Dict[str, str],
    config: Dict[str, Any]
) -> List[str]:
    """Checks a single commit message against configured rules."""
    violations = []
    subject = commit_data['subject']
    body = commit_data['body']

    # Rule 1: Subject line length
    max_subject_length = config.get('max_subject_length', 72)
    if len(subject) > max_subject_length:
        violations.append(f"Subject line exceeds {max_subject_length} characters ({len(subject)}).")

    # Rule 2: Conventional commit prefix
    required_prefixes = config.get('conventional_commit_prefixes', [])
    if required_prefixes:
        # Pattern to match 'prefix: message' or 'prefix(scope): message'
        prefix_pattern = r"^(" + "|".join(re.escape(p) for p in required_prefixes) + r")(\(.*\))?: .*"
        if not re.match(prefix_pattern, subject):
            violations.append(f"Subject line does not follow conventional commit format (e.g., 'feat: message'). Expected prefixes: {', '.join(required_prefixes)}.")

    # Rule 3: Body presence (if min_body_length > 0 or require_body_for_short_subject is True)
    min_body_length = config.get('min_body_length', 0)
    if min_body_length > 0 and len(body) < min_body_length:
        violations.append(f"Commit body is too short ({len(body)} characters). Minimum required: {min_body_length}.")
    elif config.get('require_body_for_short_subject', False) and len(subject) < 20 and not body:
        violations.append("Commit body is required for short subject lines (subject < 20 chars).")

    return violations

def main():
    # Default configuration
    config = {
        'num_commits_to_check': 10,
        'max_subject_length': 72,
        'conventional_commit_prefixes': [
            'feat:', 'fix:', 'docs:', 'chore:', 'refactor:', 'test:', 'build:', 'ci:', 'perf:', 'revert:'
        ],
        'min_body_length': 0, # Set to > 0 to enforce a minimum body length
        'require_body_for_short_subject': False # If True, requires a body if subject length < 20 chars
    }

    print(f"Nightly Lore Keeper: Checking the last {config['num_commits_to_check']} commit messages...")

    raw_messages = get_recent_commit_messages(config['num_commits_to_check'])
    if not raw_messages:
        print("No commit messages found or unable to retrieve them.")
        sys.exit(2) # No-op

    total_violations = 0
    for i, raw_msg in enumerate(raw_messages):
        commit_data = parse_commit_message(raw_msg)
        violations = check_commit_message(commit_data, config)

        if violations:
            total_violations += 1
            # Display only the first 70 chars of subject for brevity in report
            display_subject = commit_data['subject'][:70] + ('...' if len(commit_data['subject']) > 70 else '')
            print(f"\n--- Commit {i+1} (Subject: '{display_subject}') ---")
            for violation in violations:
                print(f"  - VIOLATION: {violation}")

    if total_violations > 0:
        print(f"\nLore Keeper detected {total_violations} commit message violations.")
        sys.exit(1) # Failure
    else:
        print("\nAll recent commit messages adhere to the lore. The chronicles are pristine!")
        sys.exit(0) # Success

if __name__ == "__main__":
    main()
