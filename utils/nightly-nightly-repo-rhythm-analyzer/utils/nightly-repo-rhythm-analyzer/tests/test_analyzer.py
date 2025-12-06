import unittest
import subprocess
import os
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

# Assuming analyzer.py is in src/
from src.analyzer import GitAnalyzer

class TestGitAnalyzer(unittest.TestCase):

    def setUp(self):
        # Create a dummy local repo for testing --path
        self.dummy_repo_path = os.path.join(os.getcwd(), "test_dummy_repo")
        os.makedirs(self.dummy_repo_path, exist_ok=True)
        # Initialize a dummy git repo
        subprocess.run(['git', 'init'], cwd=self.dummy_repo_path, capture_output=True, text=True, check=True)
        # Create a dummy file and commit
        with open(os.path.join(self.dummy_repo_path, "test_file.txt"), "w") as f:
            f.write("initial commit")
        subprocess.run(['git', 'add', 'test_file.txt'], cwd=self.dummy_repo_path, capture_output=True, text=True, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=self.dummy_repo_path, capture_output=True, text=True, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=self.dummy_repo_path, capture_output=True, text=True, check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=self.dummy_repo_path, capture_output=True, text=True, check=True)


    def tearDown(self):
        # Clean up the dummy local repo
        if os.path.exists(self.dummy_repo_path):
            shutil.rmtree(self.dummy_repo_path)

    @patch('subprocess.run')
    def test_init_with_repo_url_clones(self, mock_subprocess_run):
        # Mock rationale: Avoid actual network calls for cloning.
        # Simulate successful git clone.
        mock_subprocess_run.return_value = MagicMock(stdout="Cloning into 'temp_repo_...'...", stderr="", returncode=0)

        repo_url = "https://github.com/test/repo.git"
        with GitAnalyzer(repo_url=repo_url) as analyzer:
            self.assertIsNotNone(analyzer.temp_dir)
            self.assertTrue(analyzer.repo_path.startswith(os.getcwd()))
            # Ensure git clone was called
            mock_subprocess_run.assert_any_call(
                ['git', 'clone', '--depth', '1000', '--branch', 'main', repo_url, analyzer.temp_dir],
                cwd=os.getcwd(),
                capture_output=True,
                text=True,
                check=True
            )
        # Ensure cleanup is called on exit (temp_dir will be removed by __exit__)
        # Note: The mock doesn't create the directory, so we can't assert its non-existence directly here
        # without a more complex mock setup. The test primarily confirms the call to git clone.

    @patch('subprocess.run')
    def test_get_commit_timestamps(self, mock_subprocess_run):
        # Mock rationale: Avoid actual git log execution.
        # Simulate git log output with specific timestamps.
        mock_subprocess_run.return_value = MagicMock(
            stdout="1678886400\n1678890000\n1678972800", # March 15, 2023 00:00:00 UTC, 01:00:00 UTC, March 16, 2023 00:00:00 UTC
            stderr="",
            returncode=0
        )

        with GitAnalyzer(repo_path=self.dummy_repo_path) as analyzer:
            timestamps = analyzer._get_commit_timestamps()
            self.assertEqual(timestamps, [1678886400, 1678890000, 1678972800])
            mock_subprocess_run.assert_called_once_with(
                ['git', 'log', '--all', '--format=%at'],
                cwd=self.dummy_repo_path,
                capture_output=True,
                text=True,
                check=True
            )

    @patch('subprocess.run')
    @patch('builtins.print')
    def test_analyze_rhythm_output(self, mock_print, mock_subprocess_run):
        # Mock rationale: Avoid actual git log execution and capture print output.
        # Simulate git log output for a specific pattern:
        # 2 commits on Monday 09:00 UTC
        # 2 commits on Tuesday 10:00 UTC
        # 1 commit on Wednesday 11:00 UTC
        # Total 5 commits
        mock_subprocess_run.return_value = MagicMock(
            stdout=(
                f"{int(datetime(2023, 3, 13, 9, 0, 0, tzinfo=timezone.utc).timestamp())}\n"   # Monday 09:00 UTC
                f"{int(datetime(2023, 3, 13, 9, 30, 0, tzinfo=timezone.utc).timestamp())}\n"  # Monday 09:30 UTC
                f"{int(datetime(2023, 3, 14, 10, 0, 0, tzinfo=timezone.utc).timestamp())}\n" # Tuesday 10:00 UTC
                f"{int(datetime(2023, 3, 14, 10, 15, 0, tzinfo=timezone.utc).timestamp())}\n" # Tuesday 10:15 UTC
                f"{int(datetime(2023, 3, 15, 11, 0, 0, tzinfo=timezone.utc).timestamp())}"  # Wednesday 11:00 UTC
            ),
            stderr="",
            returncode=0
        )

        with GitAnalyzer(repo_path=self.dummy_repo_path) as analyzer:
            analyzer.analyze_rhythm()

            # Check for key phrases in the print calls
            mock_print.assert_any_call("\n--- Activity by Hour of Day (UTC) ---")
            mock_print.assert_any_call("Hour 09:00-09:59: 2 commits (40.0%)")
            mock_print.assert_any_call("Hour 10:00-10:59: 2 commits (40.0%)")
            mock_print.assert_any_call("Hour 11:00-11:59: 1 commits (20.0%)")
            # Peak hour will be the first one encountered if counts are equal, due to sorted iteration and `>` comparison.
            mock_print.assert_any_call("\nPeak Activity Hour (UTC): 09:00-09:59 with 2 commits.")

            mock_print.assert_any_call("\n--- Activity by Day of Week (UTC) ---")
            mock_print.assert_any_call("Monday: 2 commits (40.0%)")
            mock_print.assert_any_call("Tuesday: 2 commits (40.0%)")
            mock_print.assert_any_call("Wednesday: 1 commits (20.0%)")
            # Peak day will be the first one encountered if counts are equal.
            mock_print.assert_any_call("\nPeak Activity Day (UTC): Monday with 2 commits.")

            mock_print.assert_any_call("\nTotal Commits Analyzed: 5")

    @patch('subprocess.run')
    def test_cleanup_temp_dir_on_exit(self, mock_subprocess_run):
        # Mock rationale: Prevent actual git clone and ensure cleanup logic is called.
        # Simulate successful git clone.
        mock_subprocess_run.return_value = MagicMock(stdout="Cloning...", stderr="", returncode=0)

        # Manually create a temporary directory to ensure it exists for cleanup test
        temp_dir_path = os.path.join(os.getcwd(), f"temp_repo_{os.getpid()}_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        os.makedirs(temp_dir_path, exist_ok=True)

        with GitAnalyzer(repo_url="https://github.com/test/repo.git") as analyzer:
            # Override temp_dir to point to our manually created one for testing cleanup
            analyzer.temp_dir = temp_dir_path
            self.assertTrue(os.path.exists(analyzer.temp_dir))
        
        # After exiting the 'with' block, the temp_dir should be cleaned up
        self.assertFalse(os.path.exists(temp_dir_path))

    def test_init_no_path_or_url(self):
        # Test that a ValueError is raised if neither path nor repo_url is provided.
        with self.assertRaises(ValueError) as cm:
            GitAnalyzer()
        self.assertIn("Either --path or --repo-url must be provided.", str(cm.exception))

    @patch('subprocess.run')
    def test_git_command_failure(self, mock_subprocess_run):
        # Mock rationale: Simulate a git command failing.
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(128, ['git', 'log'], stderr="fatal: not a git repository")

        with GitAnalyzer(repo_path=self.dummy_repo_path) as analyzer:
            with self.assertRaises(subprocess.CalledProcessError):
                analyzer._get_commit_timestamps()

    @patch('subprocess.run', side_effect=FileNotFoundError("git command not found"))
    def test_git_not_found(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git' command not being in PATH.
        with GitAnalyzer(repo_path=self.dummy_repo_path) as analyzer:
            with self.assertRaises(FileNotFoundError):
                analyzer._get_commit_timestamps()

if __name__ == '__main__':
    unittest.main()
