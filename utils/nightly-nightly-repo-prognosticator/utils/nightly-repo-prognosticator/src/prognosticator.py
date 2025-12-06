import subprocess
import datetime
import re
import os
import argparse

def _run_git_command(command):
    """Helper to run a git command and return its output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            cwd=os.getcwd() # Ensure it runs in the current directory (expected to be repo root)
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # print(f"Error running git command: {' '.join(command)}")
        # print(f"Stderr: {e.stderr.strip()}")
        return None
    except FileNotFoundError:
        # print("Error: 'git' command not found. Please ensure Git is installed and in your PATH.")
        return None

def get_last_commit_date(branch_name):
    """Gets the last commit date for a given branch."""
    command = ['git', 'log', branch_name, '-1', '--format=%cd']
    output = _run_git_command(command)
    if output:
        return output
    return "N/A"

def get_stale_branches(stale_days, main_branch_name):
    """Identifies branches that haven't been updated in stale_days."""
    stale_threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=stale_days)
    stale_branches = []

    # Get all local branches and their upstream tracking info
    branch_info_output = _run_git_command(['git', 'branch', '-vv', '--no-color'])

    if not branch_info_output:
        return []

    for line in branch_info_output.splitlines():
        match = re.match(r'\s*\*?\s*([^\s]+)\s+([0-9a-f]+)\s+.*', line)
        if match:
            branch_name = match.group(1)
            if branch_name == main_branch_name: # Don't consider the main branch stale
                continue

            # Get the last commit date for this specific branch
            commit_date_str = _run_git_command(['git', 'log', branch_name, '-1', '--format=%cd'])
            if commit_date_str and commit_date_str != "N/A":
                try:
                    commit_datetime = datetime.datetime.strptime(commit_date_str, '%a %b %d %H:%M:%S %Y %z')
                    if commit_datetime < stale_threshold:
                        stale_branches.append({
                            'name': branch_name,
                            'last_commit': commit_datetime.strftime('%Y-%m-%d')
                        })
                except ValueError:
                    # Log parsing error but continue
                    pass
    return stale_branches

def get_prognosis(last_commit_date_str, stale_branches):
    """Generates a whimsical prognosis based on repo health."""
    prognosis_messages = []

    # Check last commit date for overall activity
    if last_commit_date_str == "N/A":
        prognosis_messages.append("The repository's star has dimmed. Awaiting new cosmic energy infusions.")
    else:
        try:
            last_commit_datetime = datetime.datetime.strptime(last_commit_date_str, '%a %b %d %H:%M:%S %Y %z')
            now = datetime.datetime.now(datetime.timezone.utc)
            days_since_last_commit = (now - last_commit_datetime).days

            if days_since_last_commit > 180: # Very old
                prognosis_messages.append("Warning: The repository shows signs of cosmic dormancy. Re-energize soon!")
            elif days_since_last_commit > 60: # Moderately old
                prognosis_messages.append("The celestial currents are slowing. Consider injecting fresh cosmic dust.")
            else:
                prognosis_messages.append("Cosmic currents are favorable. Repository systems are humming along.")
        except ValueError:
            prognosis_messages.append("Unable to determine recent activity. The cosmic forecast is hazy.")

    # Check stale branches
    if stale_branches:
        if len(stale_branches) > 5:
            prognosis_messages.append("Warning: A nebula of forgotten branches is forming. Initiate immediate stellar cleanup protocols!")
        elif len(stale_branches) > 0:
            prognosis_messages.append("Minor gravitational anomalies detected in auxiliary branches. Consider a celestial sweep.")

    if not prognosis_messages:
        return "The cosmic forecast is clear. All systems nominal."
    return " ".join(prognosis_messages)

def main():
    parser = argparse.ArgumentParser(description="Nightly Repository Prognosticator")
    parser.add_argument('--stale-days', type=int, default=90, help='Number of days after which a branch is considered stale.')
    parser.add_argument('--main-branch', type=str, default='main', help='The name of your main development branch (e.g., main, master).')
    args = parser.parse_args()

    print("🌌 Repository Prognosis Report 🌌\n")
    print("--- Health Metrics ---")

    last_commit = get_last_commit_date(args.main_branch)
    print(f"Last commit on '{args.main_branch}': {last_commit}")

    stale_branches = get_stale_branches(args.stale_days, args.main_branch)
    if stale_branches:
        print(f"Stale branches (older than {args.stale_days} days):")
        for branch in stale_branches:
            print(f"  - {branch['name']} (last commit: {branch['last_commit']})")
    else:
        print(f"No stale branches detected (older than {args.stale_days} days).")

    print("\n--- Cosmic Prognosis ---")
    prognosis = get_prognosis(last_commit, stale_branches)
    print(prognosis)

if __name__ == '__main__':
    main()
