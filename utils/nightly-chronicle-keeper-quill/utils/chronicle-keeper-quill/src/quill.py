import subprocess
import argparse
import re
import os

def run_git_command(command, cwd=None):
    """Helper to run git commands and capture output."""
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
        cwd=cwd
    )
    return result.stdout.strip()

def parse_commit_message(message):
    """Parses a commit message for type, scope, subject, and breaking changes."""
    lines = message.split('\n')
    header = lines[0]
    body = '\n'.join(lines[1:]).strip()

    # Regex for conventional commits: type(scope)!: subject
    match = re.match(r"^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?: (?P<subject>.*)", header)

    commit_type = "chore" # Default type
    scope = None
    subject = header
    is_breaking = False
    
    if match:
        commit_type = match.group('type').lower()
        scope = match.group('scope')
        subject = match.group('subject').strip()
        if match.group('breaking'):
            is_breaking = True
    
    # Also check body for BREAKING CHANGE: regardless of header format
    if "BREAKING CHANGE:" in body:
        is_breaking = True

    return {
        "type": commit_type,
        "scope": scope,
        "subject": subject,
        "body": body,
        "is_breaking": is_breaking
    }

def generate_changelog(start_ref, end_ref, cwd=None):
    """Generates a changelog from git history."""
    try:
        # Get commit hashes, subjects, and bodies
        # Format: %H (full hash), %s (subject), %b (body)
        # Use a unique separator for parsing
        log_format = "%H%n%s%n%b%n---COMMIT-SEPARATOR---"
        git_log_output = run_git_command(
            ["git", "log", f"--pretty=format:{log_format}", f"{start_ref}..{end_ref}"],
            cwd=cwd
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running git log: {e.stderr}")
        return "Error: Could not retrieve git history."

    commits_raw = git_log_output.split("---COMMIT-SEPARATOR---")
    
    # Filter out empty strings from split
    commits_raw = [c.strip() for c in commits_raw if c.strip()]

    parsed_commits = []
    for commit_block in commits_raw:
        if not commit_block:
            continue
        
        lines = commit_block.split('\n', 2) # Split into hash, header, and rest (body)
        if len(lines) < 2: # Malformed commit block
            continue
        
        commit_hash = lines[0]
        header = lines[1]
        body = lines[2] if len(lines) > 2 else ""
        
        full_message = f"{header}\n{body}"
        parsed = parse_commit_message(full_message)
        parsed["hash"] = commit_hash[:7] # Short hash
        parsed_commits.append(parsed)

    # Group commits by type
    grouped_commits = {
        "feat": [], "fix": [], "docs": [], "refactor": [], "perf": [],
        "chore": [], "build": [], "ci": [], "test": [], "revert": [],
        "other": []
    }
    breaking_changes = []

    for commit in parsed_commits:
        if commit["is_breaking"]:
            breaking_changes.append(commit)
        
        if commit["type"] in grouped_commits:
            grouped_commits[commit["type"]].append(commit)
        else:
            grouped_commits["other"].append(commit)

    # Build changelog Markdown
    changelog_md = []
    
    if breaking_changes:
        changelog_md.append("## 💥 Breaking Changes\n")
        for commit in breaking_changes:
            # Extract breaking change description from body if present
            breaking_desc = ""
            body_lines = commit["body"].split('\n')
            for line in body_lines:
                if line.strip().startswith("BREAKING CHANGE:"):
                    breaking_desc = line.strip().replace("BREAKING CHANGE:", "").strip()
                    break
            if not breaking_desc: # Fallback to subject if no specific breaking change description
                breaking_desc = commit["subject"]
            
            changelog_md.append(f"- **{commit['subject']}** ({commit['hash']})\n  {breaking_desc}\n")
        changelog_md.append("\n") # Add a newline for separation

    type_titles = {
        "feat": "✨ Features",
        "fix": "🐛 Bug Fixes",
        "docs": "📝 Documentation",
        "refactor": "♻️ Refactors",
        "perf": "⚡ Performance Improvements",
        "chore": "🧹 Chores",
        "build": "📦 Build System",
        "ci": "🚀 CI/CD",
        "test": "✅ Tests",
        "revert": "⏪ Reverts",
        "other": "🤷 Other Changes"
    }

    # Order of sections
    ordered_types = [
        "feat", "fix", "docs", "refactor", "perf", 
        "chore", "build", "ci", "test", "revert", "other"
    ]

    for commit_type in ordered_types:
        if grouped_commits[commit_type]:
            changelog_md.append(f"## {type_titles[commit_type]}\n")
            for commit in grouped_commits[commit_type]:
                scope_str = f"({commit['scope']})" if commit['scope'] else ""
                changelog_md.append(f"- {commit['subject']} {scope_str} ({commit['hash']})\n")
            changelog_md.append("\n") # Add a newline for separation

    return "".join(changelog_md).strip()

def main():
    parser = argparse.ArgumentParser(
        description="Generate a draft changelog from Git commit history."
    )
    parser.add_argument(
        "start_ref",
        help="The starting Git reference (e.g., a tag, commit hash, or branch name)."
    )
    parser.add_argument(
        "end_ref",
        nargs="?", # Optional argument
        default="HEAD",
        help="The ending Git reference (e.g., a tag, commit hash, or branch name). Defaults to HEAD."
    )
    parser.add_argument(
        "--cwd",
        default=os.getcwd(),
        help="The current working directory for git commands. Defaults to current directory."
    )

    args = parser.parse_args()

    changelog = generate_changelog(args.start_ref, args.end_ref, args.cwd)
    print(changelog)

if __name__ == "__main__":
    main()
