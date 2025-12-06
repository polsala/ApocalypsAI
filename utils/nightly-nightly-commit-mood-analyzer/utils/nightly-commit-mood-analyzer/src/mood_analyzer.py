import subprocess
import re
import os
from collections import defaultdict

class MoodAnalyzer:
    def __init__(self, repo_path='.', time_period='--since="24 hours ago"'):
        self.repo_path = repo_path
        self.time_period = time_period
        self.mood_keywords = {
            'Joyful Jolt': ['feat', 'add', 'implement', 'new', 'release', 'celebrate', 'yay', 'initial'],
            'Buggy Blues': ['fix', 'bug', 'error', 'issue', 'broken', 'fail', 'debug', 'hotfix'],
            'Refactor Rhapsody': ['refactor', 'clean', 'improve', 'optimize', 'perf', 'style', 'lint', 'restructure'],
            'Feature Fiesta': ['feat', 'add', 'implement', 'new', 'feature', 'develop'],
            'Documentation Delight': ['docs', 'doc', 'readme', 'comment', 'explain', 'typo'],
            'Maintenance Mumble': ['chore', 'ci', 'build', 'test', 'config', 'update', 'deps', 'upgrade', 'workflow']
        }
        self.mood_descriptions = {
            'Joyful Jolt': 'New Features, Additions',
            'Buggy Blues': 'Bug Fixes, Error Handling',
            'Refactor Rhapsody': 'Refactoring, Cleaning, Optimizing',
            'Feature Fiesta': 'New Features, Additions',
            'Documentation Delight': 'Docs, Comments, READMEs',
            'Maintenance Mumble': 'Chores, CI, Builds',
            'Neutral Nudge': 'General, Uncategorized'
        }

    def get_git_log(self):
        """Fetches recent commit messages using git log."""
        try:
            # Use --no-merges to focus on direct development commits
            # Use --pretty=format:%s to get only the subject line
            command = ['git', 'log', self.time_period, '--no-merges', '--pretty=format:%s']
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n')
        except subprocess.CalledProcessError as e:
            print(f"Error fetching git log: {e}")
            print(f"Stderr: {e.stderr}")
            return []
        except FileNotFoundError:
            print("Error: 'git' command not found. Is Git installed and in your PATH?")
            return []

    def analyze_commits(self, commit_messages):
        """Analyzes commit messages and categorizes them into moods.""" 
        mood_counts = defaultdict(int)
        total_commits = 0

        for msg in commit_messages:
            if not msg.strip(): # Skip empty messages
                continue
            total_commits += 1
            matched = False
            lower_msg = msg.lower()

            for mood, keywords in self.mood_keywords.items():
                # Use word boundaries to match whole keywords
                if any(re.search(r'\b' + keyword + r'\b', lower_msg) for keyword in keywords):
                    mood_counts[mood] += 1
                    matched = True
                    # Break after first match to avoid double counting for primary mood
                    # If a commit matches multiple, it will be counted for the first one found.
                    # For simplicity, we assign to the first matching mood.
                    break 
            
            if not matched:
                mood_counts['Neutral Nudge'] += 1
        
        return mood_counts, total_commits

    def generate_report(self, mood_counts, total_commits):
        """Generates a Markdown report based on mood analysis."""
        report = []
        report.append(f"# 🌌 Repo Emotional Forecast ({self.time_period.replace('--since=', '').replace('"', '')})")
        report.append("")

        if total_commits == 0:
            report.append("## Current Mood: Calm Waters! 🌊\n")
            report.append("No commits found in the specified period. The repository is currently in a state of serene tranquility.")
            return "\n".join(report)

        # Determine the predominant mood
        predominant_mood = 'Neutral Nudge'
        max_count = 0
        # Iterate through a consistent order (e.g., sorted keys) to ensure deterministic predominant mood selection
        # if counts are tied, prefer non-neutral moods, then alphabetical.
        sorted_mood_keys = sorted(mood_counts.keys())
        for mood in sorted_mood_keys:
            count = mood_counts[mood]
            if count > max_count:
                max_count = count
                predominant_mood = mood
            elif count == max_count and mood != 'Neutral Nudge' and predominant_mood == 'Neutral Nudge':
                # If tied with Neutral Nudge, prefer the non-neutral one
                predominant_mood = mood
            elif count == max_count and mood != 'Neutral Nudge' and predominant_mood != 'Neutral Nudge':
                # If tied with another non-neutral, prefer alphabetically earlier one
                if mood < predominant_mood:
                    predominant_mood = mood

        # Add a whimsical emoji based on predominant mood
        mood_emoji = {
            'Joyful Jolt': '🎉',
            'Buggy Blues': '🐛',
            'Refactor Rhapsody': '🎶',
            'Feature Fiesta': '🚀',
            'Documentation Delight': '📚',
            'Maintenance Mumble': '🛠️',
            'Neutral Nudge': '🧘'
        }.get(predominant_mood, '✨')

        report.append(f"## Current Mood: {predominant_mood}! {mood_emoji}\n")
        report.append("### Mood Breakdown:\n")

        # Sort moods for consistent output: predominant first, then by count (desc), then alphabetically
        sorted_moods = sorted(
            mood_counts.items(),
            key=lambda item: (item[0] != predominant_mood, -item[1], item[0])
        )

        for mood, count in sorted_moods:
            percentage = (count / total_commits) * 100 if total_commits > 0 else 0
            description = self.mood_descriptions.get(mood, 'General, Uncategorized')
            report.append(f"*   **{mood}** ({description}): {count} commits ({percentage:.2f}%)")
        
        report.append("\n---\n")
        report.append(f"*Total commits analyzed: {total_commits}*\n")
        report.append("*This forecast is based on the sentiment detected in commit messages. May your code be ever joyful!*\n")

        return "\n".join(report)

if __name__ == '__main__':
    # This script assumes it's run from the root of the Git repository
    # it intends to analyze. The default repo_path='.' handles this.
    analyzer = MoodAnalyzer()
    commits = analyzer.get_git_log()
    moods, total = analyzer.analyze_commits(commits)
    report = analyzer.generate_report(moods, total)
    print(report)
