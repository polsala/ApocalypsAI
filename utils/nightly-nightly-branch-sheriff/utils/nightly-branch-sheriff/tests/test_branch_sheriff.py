import json
import unittest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

# Mock rationale: we patch datetime.now to a fixed point so the age calculations are deterministic.
from utils.nightly_branch_sheriff.src.branch_sheriff import find_stale_branches


class TestBranchSheriff(unittest.TestCase):
    def setUp(self):
        # Fixed reference time: 2024-10-15T12:00:00Z
        self.fixed_now = datetime(2024, 10, 15, 12, 0, 0, tzinfo=timezone.utc)

    def test_basic_stale_detection(self):
        branches = [
            ("feature/old", "2024-08-01T09:30:00Z"),  # 75 days old
            ("bugfix/recent", "2024-10-10T08:00:00Z"),  # 5 days old
        ]
        with patch('utils.nightly_branch_sheriff.src.branch_sheriff.datetime') as mock_dt:
            mock_dt.now.return_value = self.fixed_now
            mock_dt.now.return_value.tzinfo = timezone.utc
            # Ensure _parse_iso still works – we let the real datetime class handle it via side_effect.
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
            stale = find_stale_branches(branches, max_age_days=30, now=self.fixed_now)
        self.assertListEqual(stale, ["feature/old"])

    def test_all_fresh(self):
        branches = [
            ("feature/new", "2024-10-14T23:59:59Z"),
            ("hotfix/now", "2024-10-15T11:59:59Z"),
        ]
        stale = find_stale_branches(branches, max_age_days=1, now=self.fixed_now)
        self.assertListEqual(stale, [])

    def test_invalid_timestamp_raises(self):
        branches = [("bad/branch", "not-a-date")]
        with self.assertRaises(ValueError) as ctx:
            find_stale_branches(branches, max_age_days=10, now=self.fixed_now)
        self.assertIn("Invalid ISO timestamp", str(ctx.exception))

    def test_cli_integration(self):
        # Simulate CLI call via subprocess-like invocation of the module's _cli function.
        # Mock sys.argv and capture stdout.
        import sys
        from io import StringIO
        from utils.nightly_branch_sheriff.src import branch_sheriff

        test_args = [
            "branch_sheriff.py",
            "--branches",
            json.dumps([
                ["old", "2024-07-01T00:00:00Z"],
                ["new", "2024-10-14T00:00:00Z"],
            ]),
            "--max-age-days",
            "60",
        ]
        with patch.object(sys, "argv", test_args), patch('sys.stdout', new_callable=StringIO) as mock_out:
            # The CLI uses datetime.now internally, but we pass a fixed now via env var hack –
            # instead we monkey‑patch the function to inject our fixed now.
            with patch('utils.nightly_branch_sheriff.src.branch_sheriff.datetime') as mock_dt:
                mock_dt.now.return_value = self.fixed_now
                mock_dt.now.return_value.tzinfo = timezone.utc
                mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
                branch_sheriff._cli()
            output = mock_out.getvalue().strip()
        self.assertEqual(output, json.dumps(["old"]))


if __name__ == "__main__":
    unittest.main()
