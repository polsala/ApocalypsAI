import argparse
import subprocess
import os
import shutil
from collections import defaultdict
from datetime import datetime, timezone

class GitAnalyzer:
    def __init__(self, repo_path=None, repo_url=None, branch='main'):
        self.repo_path = repo_path
        self.repo_url = repo_url
        self.branch = branch
        self.temp_dir = None

        if not self.repo_path and not self.repo_url:
            raise ValueError("Either --path or --repo-url must be provided.")

        if self.repo_url:
            # Create a unique temporary directory name
            self.temp_dir = os.path.join(os.getcwd(), f"temp_repo_{os.getpid()}_{datetime.now().strftime('%Y%m%d%H%M%S')}")
            self._clone_repo()
            self.repo_path = self.temp_dir

    def _run_git_command(self, command, cwd=None):
        """Helper to run git commands."""
        try:
            result = subprocess.run(
                ['git'] + command,
                cwd=cwd or self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running git command: {' '.join(['git'] + command)}")
            print(f"Stderr: {e.stderr}")
            raise
        except FileNotFoundError:
            print("Error: 'git' command not found. Please ensure Git is installed and in your PATH.")
            raise

    def _clone_repo(self):
        """Clones the repository into a temporary directory."""
        print(f"Cloning {self.repo_url} into {self.temp_dir}...")
        try:
            self._run_git_command(['clone', '--depth', '1000', '--branch', self.branch, self.repo_url, self.temp_dir], cwd=os.getcwd())
            print("Cloning complete.")
        except Exception as e:
            self._cleanup_temp_dir()
            raise e

    def _get_commit_timestamps(self):
        """Fetches commit timestamps from the Git log."""
        # %at: author date, UNIX timestamp
        log_output = self._run_git_command(['log', '--all', '--format=%at'])
        timestamps = [int(ts) for ts in log_output.splitlines() if ts.strip()]
        return timestamps

    def analyze_rhythm(self):
        """Analyzes commit timestamps to determine activity patterns."""
        timestamps = self._get_commit_timestamps()
        if not timestamps:
            print("No commits found to analyze.")
            return

        total_commits = len(timestamps)
        hourly_activity = defaultdict(int) # 0-23
        daily_activity = defaultdict(int)  # 0=Monday, 6=Sunday

        for ts in timestamps:
            dt_object = datetime.fromtimestamp(ts, tz=timezone.utc)
            hourly_activity[dt_object.hour] += 1
            daily_activity[dt_object.weekday()] += 1 # Monday is 0, Sunday is 6

        self._print_report(total_commits, hourly_activity, daily_activity)

    def _print_report(self, total_commits, hourly_activity, daily_activity):
        """Prints the analysis report."""
        print(f"\nRepo Rhythm Analysis for: {self.repo_path}")
        print(f"\n--- Activity by Hour of Day (UTC) ---")
        sorted_hourly = sorted(hourly_activity.items())
        peak_hour_count = -1
        peak_hour = -1

        for hour, count in sorted_hourly:
            percentage = (count / total_commits) * 100 if total_commits else 0
            hour_str = f"{hour:02d}:00-{hour:02d}:59"
            print(f"Hour {hour_str}: {count} commits ({percentage:.1f}%)")
            if count > peak_hour_count:
                peak_hour_count = count
                peak_hour = hour

        if peak_hour != -1:
            print(f"\nPeak Activity Hour (UTC): {peak_hour:02d}:00-{peak_hour:02d}:59 with {peak_hour_count} commits.")

        print(f"\n--- Activity by Day of Week (UTC) ---")
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        sorted_daily = sorted(daily_activity.items())
        peak_day_count = -1
        peak_day = -1

        for day_index, count in sorted_daily:
            percentage = (count / total_commits) * 100 if total_commits else 0
            print(f"{day_names[day_index]}: {count} commits ({percentage:.1f}%)")
            if count > peak_day_count:
                peak_day_count = count
                peak_day = day_index

        if peak_day != -1:
            print(f"\nPeak Activity Day (UTC): {day_names[peak_day]} with {peak_day_count} commits.")

        print(f"\nTotal Commits Analyzed: {total_commits}")

    def _cleanup_temp_dir(self):
        """Removes the temporary cloned repository."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            print(f"Cleaning up temporary directory: {self.temp_dir}")
            shutil.rmtree(self.temp_dir)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cleanup_temp_dir()


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Git commit history to find activity patterns."
    )
    parser.add_argument(
        "--path",
        type=str,
        help="Path to a local Git repository."
    )
    parser.add_argument(
        "--repo-url",
        type=str,
        help="URL of a remote Git repository to clone and analyze."
    )
    parser.add_argument(
        "--branch",
        type=str,
        default="main",
        help="Branch to analyze (default: main)."
    )

    args = parser.parse_args()

    try:
        with GitAnalyzer(repo_path=args.path, repo_url=args.repo_url, branch=args.branch) as analyzer:
            analyzer.analyze_rhythm()
    except ValueError as e:
        print(f"Error: {e}")
        parser.print_help()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    main()
