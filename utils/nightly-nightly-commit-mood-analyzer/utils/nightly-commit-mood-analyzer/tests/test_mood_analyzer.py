import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from collections import defaultdict

# Mock rationale: Ensures the test can find the module regardless of where the test is run from.
# This makes the test self-contained and runnable without external setup.
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_path)

from mood_analyzer import MoodAnalyzer

class TestMoodAnalyzer(unittest.TestCase):

    def setUp(self):
        # Initialize MoodAnalyzer with a dummy path for testing
        self.analyzer = MoodAnalyzer(repo_path='/tmp/test_repo', time_period='-n 10')

    @patch('subprocess.run')
    def test_get_git_log_success(self, mock_subprocess_run):
        # Mock rationale: We don't want to actually run git commands during tests.
        # We simulate successful git log output.
        mock_subprocess_run.return_value = MagicMock(
            stdout="feat: Add new feature\nfix: Resolve critical bug\nchore: Update dependencies",
            stderr="",
            returncode=0
        )
        
        commits = self.analyzer.get_git_log()
        self.assertEqual(len(commits), 3)
        self.assertIn("feat: Add new feature", commits)
        self.assertIn("fix: Resolve critical bug", commits)
        self.assertIn("chore: Update dependencies", commits)
        
        # Verify subprocess.run was called with the correct arguments
        expected_command = ['git', 'log', '-n 10', '--no-merges', '--pretty=format:%s']
        mock_subprocess_run.assert_called_once_with(
            expected_command,
            cwd='/tmp/test_repo',
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    def test_get_git_log_empty(self, mock_subprocess_run):
        # Mock rationale: Simulate a scenario where no commits are found.
        mock_subprocess_run.return_value = MagicMock(
            stdout="",
            stderr="",
            returncode=0
        )
        commits = self.analyzer.get_git_log()
        self.assertEqual(len(commits), 1) # split('\n') on empty string gives ['']
        self.assertEqual(commits[0], '')

    @patch('subprocess.run')
    def test_get_git_log_error(self, mock_subprocess_run):
        # Mock rationale: Simulate a git command failure.
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=['git', 'log'],
            stderr='fatal: not a git repository'
        )
        commits = self.analyzer.get_git_log()
        self.assertEqual(commits, [])

    @patch('subprocess.run')
    def test_get_git_log_git_not_found(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git' command not being available.
        mock_subprocess_run.side_effect = FileNotFoundError
        commits = self.analyzer.get_git_log()
        self.assertEqual(commits, [])

    def test_analyze_commits_various_moods(self):
        commit_messages = [
            "feat: Implement user authentication", # Joyful Jolt / Feature Fiesta
            "fix: Correct typo in README",        # Buggy Blues / Documentation Delight (typo)
            "refactor: Clean up old API endpoints", # Refactor Rhapsody
            "chore: Update CI configuration",     # Maintenance Mumble
            "docs: Add new usage examples",       # Documentation Delight
            "add: New dashboard widget",          # Joyful Jolt / Feature Fiesta
            "style: Format code with black",      # Refactor Rhapsody
            "Initial commit",                     # Joyful Jolt
            "Update project description",         # Neutral Nudge
            "fix(bug): Critical security vulnerability", # Buggy Blues
            "perf: Optimize database queries"     # Refactor Rhapsody
        ]
        mood_counts, total_commits = self.analyzer.analyze_commits(commit_messages)

        self.assertEqual(total_commits, 11)
        self.assertEqual(mood_counts['Joyful Jolt'], 3) # feat, add, Initial
        self.assertEqual(mood_counts['Buggy Blues'], 2) # fix, fix(bug)
        self.assertEqual(mood_counts['Refactor Rhapsody'], 3) # refactor, style, perf
        self.assertEqual(mood_counts['Maintenance Mumble'], 1) # chore
        self.assertEqual(mood_counts['Documentation Delight'], 2) # fix (typo), docs
        self.assertEqual(mood_counts['Neutral Nudge'], 0) # All should be categorized

    def test_analyze_commits_empty_messages(self):
        commit_messages = ["", "   ", "feat: A real commit"]
        mood_counts, total_commits = self.analyzer.analyze_commits(commit_messages)
        self.assertEqual(total_commits, 1)
        self.assertEqual(mood_counts['Joyful Jolt'], 1)
        self.assertEqual(mood_counts['Neutral Nudge'], 0)

    def test_analyze_commits_no_matches(self):
        commit_messages = [
            "Some general update",
            "Another commit message",
            "Just a change"
        ]
        mood_counts, total_commits = self.analyzer.analyze_commits(commit_messages)
        self.assertEqual(total_commits, 3)
        self.assertEqual(mood_counts['Neutral Nudge'], 3)
        self.assertEqual(sum(v for k, v in mood_counts.items() if k != 'Neutral Nudge'), 0)

    def test_generate_report_no_commits(self):
        mood_counts = defaultdict(int)
        total_commits = 0
        report = self.analyzer.generate_report(mood_counts, total_commits)
        self.assertIn("Current Mood: Calm Waters! 🌊", report)
        self.assertIn("No commits found", report)

    def test_generate_report_with_data(self):
        mood_counts = defaultdict(int, {
            'Refactor Rhapsody': 5,
            'Joyful Jolt': 3,
            'Buggy Blues': 2,
            'Documentation Delight': 1,
            'Maintenance Mumble': 1
        })
        total_commits = 12
        report = self.analyzer.generate_report(mood_counts, total_commits)
        
        self.assertIn("# 🌌 Repo Emotional Forecast (-n 10)", report)
        self.assertIn("## Current Mood: Refactor Rhapsody! 🎶", report)
        self.assertIn("### Mood Breakdown:", report)
        self.assertIn("*   **Refactor Rhapsody** (Refactoring, Cleaning, Optimizing): 5 commits (41.67%)", report)
        self.assertIn("*   **Joyful Jolt** (New Features, Additions): 3 commits (25.00%)", report)
        self.assertIn("*   **Buggy Blues** (Bug Fixes, Error Handling): 2 commits (16.67%)", report)
        self.assertIn("*Total commits analyzed: 12*", report)
        self.assertIn("May your code be ever joyful!", report)

    def test_generate_report_predominant_tie_breaker(self):
        # Test case where Neutral Nudge is tied with another mood
        mood_counts = defaultdict(int, {
            'Neutral Nudge': 2,
            'Joyful Jolt': 2
        })
        total_commits = 4
        report = self.analyzer.generate_report(mood_counts, total_commits)
        self.assertIn("## Current Mood: Joyful Jolt! 🎉", report) # Joyful Jolt should be preferred over Neutral Nudge

        # Test case where two non-neutral moods are tied (alphabetical preference)
        mood_counts = defaultdict(int, {
            'Refactor Rhapsody': 2,
            'Joyful Jolt': 2,
            'Buggy Blues': 1
        })
        total_commits = 5
        report = self.analyzer.generate_report(mood_counts, total_commits)
        # 'Joyful Jolt' comes before 'Refactor Rhapsody' alphabetically, so it should be chosen if tied.
        self.assertIn("## Current Mood: Joyful Jolt! 🎉", report)

if __name__ == '__main__':
    unittest.main()
