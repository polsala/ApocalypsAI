import subprocess
import datetime
import sys

def get_commit_count(since_days: int) -> int:
    """Counts commits since a given number of days ago."""
    since_date = datetime.datetime.now() - datetime.timedelta(days=since_days)
    since_iso = since_date.isoformat()

    try:
        # Mock rationale: subprocess.run is mocked in tests to provide deterministic git log output.
        result = subprocess.run(
            ['git', 'log', '--since', since_iso, '--pretty=format:"%h"'],
            capture_output=True,
            text=True,
            check=True
        )
        # Use splitlines() to correctly handle empty output vs single empty string
        commits = result.stdout.strip().splitlines()
        return len(commits)
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        return -1 # Indicate an error
    except FileNotFoundError:
        print("Error: 'git' command not found. Is Git installed and in your PATH?", file=sys.stderr)
        return -1

def get_heartbeat_diagnosis(avg_commits_per_day: float) -> str:
    """Provides a whimsical diagnosis based on commit heartbeat."""
    if avg_commits_per_day < 0:
        return "Unable to take pulse. Repository might be in a coma or Git is not installed."
    elif avg_commits_per_day == 0:
        return "The repository seems to be in a deep slumber. Perhaps a jolt of inspiration is needed?"
    elif avg_commits_per_day < 1:
        return "A faint pulse detected. The repository is resting, but showing signs of life."
    elif avg_commits_per_day < 3:
        return "A steady rhythm. The repository is maintaining a healthy pace."
    elif avg_commits_per_day < 7:
        return "The code is buzzing with activity! Keep up the good work, little bots!"
    else:
        return "A frantic pace! The repository is on fire! (In a good way, hopefully!)"

def main():
    monitoring_days = 7
    print("🩺 Repository Vital Signs Report 🩺\n")
    print(f"Monitoring period: Last {monitoring_days} days\n")

    commit_count = get_commit_count(monitoring_days)

    if commit_count == -1:
        print("Diagnosis: Failed to retrieve commit data. Please check logs for errors.")
        sys.exit(1)

    avg_commits_per_day = commit_count / monitoring_days if monitoring_days > 0 else 0

    print(f"Commit Heartbeat: {avg_commits_per_day:.1f} commits/day")
    print(f"Diagnosis: {get_heartbeat_diagnosis(avg_commits_per_day)}")

    sys.exit(0)

if __name__ == "__main__":
    main()
