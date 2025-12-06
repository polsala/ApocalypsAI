import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Ensure the src directory is importable
src_path = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(src_path))

from pruner import get_merged_branches, filter_protected, pretty_print, main

class TestGitBranchPruner(unittest.TestCase):
    @patch("pruner.run_git")
    def test_get_merged_branches_success(self, mock_run):
        # Mock rationale: simulate `git branch --merged main` output.
        mock_run.return_value = MagicMock(returncode=0, stdout="  feature/a\n* main\n  bugfix/b\n", stderr="")
        branches = get_merged_branches("main")
        self.assertSetEqual(branches, {"feature/a", "main", "bugfix/b"})
        mock_run.assert_called_once_with(["branch", "--merged", "main"])

    @patch("pruner.run_git")
    def test_get_merged_branches_error(self, mock_run):
        # Mock rationale: git returns non‑zero exit code (e.g., unknown base).
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="fatal: ambiguous argument 'unknown'\n")
        with self.assertRaises(RuntimeError) as ctx:
            get_merged_branches("unknown")
        self.assertIn("Git error while listing merged branches", str(ctx.exception))

    def test_filter_protected(self):
        branches = {"main", "dev", "feature/x", "feature/y"}
        protect = {"main", "dev"}
        filtered = filter_protected(branches, protect)
        self.assertSetEqual(filtered, {"feature/x", "feature/y"})

    @patch("builtins.input", return_value="y")
    @patch("pruner.run_git")
    def test_delete_branches_success(self, mock_run, mock_input):
        # Mock rationale: simulate successful deletion via `git branch -d`.
        mock_run.return_value = MagicMock(returncode=0, stdout="Deleted branch feature/x (was abcdef).\n", stderr="")
        # Import inside test to avoid side‑effects.
        from pruner import delete_branches
        delete_branches({"feature/x"})
        mock_run.assert_called_once_with(["branch", "-d", "feature/x"])

    @patch("builtins.input", return_value="n")
    @patch("pruner.run_git")
    def test_delete_branches_user_abort(self, mock_run, mock_input):
        from pruner import delete_branches
        delete_branches({"feature/x"})
        mock_run.assert_not_called()

    @patch("pruner.get_merged_branches")
    @patch("pruner.pretty_print")
    @patch("pruner.delete_branches")
    def test_main_dry_run(self, mock_delete, mock_pretty, mock_merged):
        mock_merged.return_value = {"main", "feature/a", "feature/b"}
        exit_code = main(["--base", "main", "--protect", "main"])
        self.assertEqual(exit_code, 0)
        mock_pretty.assert_called_once()
        mock_delete.assert_not_called()

    @patch("pruner.get_merged_branches")
    @patch("pruner.pretty_print")
    @patch("pruner.delete_branches")
    @patch("builtins.input", return_value="y")
    def test_main_with_delete(self, mock_input, mock_delete, mock_pretty, mock_merged):
        mock_merged.return_value = {"main", "feature/a"}
        exit_code = main(["--delete", "--protect", "main"])
        self.assertEqual(exit_code, 0)
        mock_pretty.assert_called_once()
        mock_delete.assert_called_once()

if __name__ == "__main__":
    unittest.main()
