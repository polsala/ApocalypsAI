import datetime
import unittest
from branch_cleaner import is_branch_stale, get_stale_branches, delete_branches


class TestBranchCleaner(unittest.TestCase):
    def setUp(self):
        # Fixed reference point for deterministic tests
        self.now = datetime.datetime(2024, 10, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)

    def test_is_branch_stale_true(self):
        # Mock rationale: branch last commit 200 days ago should be stale for 180‑day threshold
        old_date = "2024-03-15T12:00:00Z"
        self.assertTrue(is_branch_stale(old_date, days_threshold=180, now=self.now))

    def test_is_branch_stale_false(self):
        # Mock rationale: branch last commit 30 days ago is recent
        recent_date = "2024-09-01T12:00:00Z"
        self.assertFalse(is_branch_stale(recent_date, days_threshold=180, now=self.now))

    def test_get_stale_branches(self):
        # Mock rationale: mixed set of branches
        branches = {
            "old-feature": "2024-01-01T00:00:00Z",   # 274 days old
            "new-feature": "2024-09-20T00:00:00Z",   # 11 days old
            "main": "2024-10-01T08:30:00Z",          # same day
        }
        stale = get_stale_branches(branches, days_threshold=180, now=self.now)
        self.assertListEqual(stale, ["old-feature"])

    def test_delete_branches(self):
        # Mock rationale: ensure function returns input list unchanged
        to_delete = ["old-feature", "unused"]
        deleted = delete_branches(to_delete)
        self.assertListEqual(deleted, to_delete)


if __name__ == "__main__":
    unittest.main()
