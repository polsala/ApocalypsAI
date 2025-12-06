import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import subprocess

# Add the src directory to the Python path to allow importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from changelog_synthesizer import synthesize_changelog, _run_git_command

class TestChangelogSynthesizer(unittest.TestCase):

    @patch('subprocess.run')
    def test_synthesize_changelog_basic(self, mock_subprocess_run):
        # Mock rationale: We need to simulate 'git log' output without actually running git.
        # This ensures tests are fast, deterministic, and don't depend on the local git history.
        mock_subprocess_run.return_value = MagicMock(
            stdout="""feat: Add new cosmic ray deflector
            
fix: Correct temporal anomaly in flux capacitor

chore: Update dependency manifest

docs: Add more details about warp drive calibration

refactor: Optimize subspace communication protocols

perf: Improve hyperspace jump calculations

test: Add unit tests for new API endpoints

build: Update CI configuration for new galaxy cluster

ci: Configure nightly integration tests

revert: Revert accidental black hole creation

Initial commit
""",
            stderr="",
            returncode=0
        )

        expected_changelog = """# Changelog from v1.0.0 to HEAD

## Features
*   feat: Add new cosmic ray deflector

## Bug Fixes
*   fix: Correct temporal anomaly in flux capacitor

## Performance Improvements
*   perf: Improve hyperspace jump calculations

## Refactoring
*   refactor: Optimize subspace communication protocols

## Documentation
*   docs: Add more details about warp drive calibration

## Build System
*   build: Update CI configuration for new galaxy cluster

## CI/CD
*   ci: Configure nightly integration tests

## Tests
*   test: Add unit tests for new API endpoints

## Chores
*   chore: Update dependency manifest

## Reverts
*   revert: Revert accidental black hole creation

## Other Changes
*   Initial commit"""
        
        changelog = synthesize_changelog('v1.0.0', 'HEAD')
        self.assertEqual(changelog.strip(), expected_changelog.strip()) # .strip() to handle leading/trailing newlines
        
        mock_subprocess_run.assert_called_once_with(
            ['git', 'log', '--pretty=format:%s%n%b', 'v1.0.0..HEAD'],
            capture_output=True,
            text=True,
            check=True,
            cwd='.',
            encoding='utf-8'
        )

    @patch('subprocess.run')
    def test_synthesize_changelog_empty_range(self, mock_subprocess_run):
        # Mock rationale: Simulate a git log command that returns no commits.
        mock_subprocess_run.return_value = MagicMock(
            stdout="",
            stderr="",
            returncode=0
        )

        expected_changelog = "# Changelog from v1.0.0 to v1.0.0\n\nNo commits found in this range or log is empty."
        changelog = synthesize_changelog('v1.0.0', 'v1.0.0')
        self.assertEqual(changelog.strip(), expected_changelog.strip())

    @patch('subprocess.run')
    def test_synthesize_changelog_only_one_type(self, mock_subprocess_run):
        # Mock rationale: Simulate a git log with only 'fix' commits.
        mock_subprocess_run.return_value = MagicMock(
            stdout="""fix: Bug A
            
fix: Bug B
""",
            stderr="",
            returncode=0
        )

        expected_changelog = """# Changelog from v1.0.0 to v1.0.1

## Bug Fixes
*   fix: Bug A
*   fix: Bug B"""
        changelog = synthesize_changelog('v1.0.0', 'v1.0.1')
        self.assertEqual(changelog.strip(), expected_changelog.strip())

    @patch('subprocess.run')
    def test_synthesize_changelog_with_scopes(self, mock_subprocess_run):
        # Mock rationale: Test parsing of conventional commits with scopes.
        mock_subprocess_run.return_value = MagicMock(
            stdout="""feat(auth): Implement new login flow
            
fix(ui): Fix button alignment issue
""",
            stderr="",
            returncode=0
        )

        expected_changelog = """# Changelog from v1.0.0 to v1.0.1

## Features
*   feat(auth): Implement new login flow

## Bug Fixes
*   fix(ui): Fix button alignment issue"""
        changelog = synthesize_changelog('v1.0.0', 'v1.0.1')
        self.assertEqual(changelog.strip(), expected_changelog.strip())

    @patch('subprocess.run')
    def test_synthesize_changelog_no_conventional_commits(self, mock_subprocess_run):
        # Mock rationale: Test behavior when no conventional commits are present.
        mock_subprocess_run.return_value = MagicMock(
            stdout="""Initial commit
            
Another random commit message
""",
            stderr="",
            returncode=0
        )

        expected_changelog = """# Changelog from v0.0.0 to v0.0.1

## Other Changes
*   Another random commit message
*   Initial commit"""
        changelog = synthesize_changelog('v0.0.0', 'v0.0.1')
        self.assertEqual(changelog.strip(), expected_changelog.strip())

    @patch('subprocess.run')
    def test_run_git_command_error(self, mock_subprocess_run):
        # Mock rationale: Simulate a git command failing (e.g., invalid ref).
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(
            returncode=128, cmd=['git', 'log'], stderr='fatal: bad object v_invalid'
        )
        
        # We expect sys.exit(1) to be called, so we capture it.
        with self.assertRaises(SystemExit) as cm:
            _run_git_command(['git', 'log', 'v_invalid..HEAD'])
        self.assertEqual(cm.exception.code, 1)

    @patch('subprocess.run')
    def test_run_git_command_git_not_found(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git' command not being in PATH.
        mock_subprocess_run.side_effect = FileNotFoundError
        
        with self.assertRaises(SystemExit) as cm:
            _run_git_command(['git', 'log', 'HEAD'])
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
