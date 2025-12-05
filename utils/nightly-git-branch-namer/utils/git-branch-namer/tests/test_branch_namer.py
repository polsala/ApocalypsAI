import unittest
from src.branch_namer import slugify, build_branch_name


class TestSlugify(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Add user login"), "add-user-login")

    def test_punctuation_and_spaces(self):
        self.assertEqual(slugify("Fix:   bug #42!!"), "fix-bug-42")

    def test_mixed_case_and_unicode(self):
        self.assertEqual(slugify("Äççéntéd Tïtlé"), "cctitle")  # non‑ASCII stripped

    def test_custom_separator(self):
        self.assertEqual(slugify("Hello World", separator="_"), "hello_world")

    def test_empty_input(self):
        self.assertEqual(slugify("   !!!   "), "")


class TestBuildBranchName(unittest.TestCase):
    def test_without_prefix(self):
        self.assertEqual(build_branch_name("Add user login"), "add-user-login")

    def test_with_prefix(self):
        self.assertEqual(build_branch_name("Add user login", prefix="feat"), "feat-add-user-login")

    def test_prefix_with_spaces(self):
        self.assertEqual(build_branch_name("Add user login", prefix="Feature request"), "feature-request-add-user-login")

    def test_custom_separator(self):
        self.assertEqual(
            build_branch_name("Add user login", prefix="feat", separator="_"),
            "feat_add_user_login",
        )

    def test_empty_title_raises(self):
        with self.assertRaises(ValueError):
            build_branch_name("   !!!   ")

    def test_empty_prefix_is_ignored(self):
        # Prefix that becomes empty after slugify should be ignored
        self.assertEqual(build_branch_name("Add user login", prefix="!!!"), "add-user-login")


if __name__ == "__main__":
    # Mock rationale: Running unittest.main() directly would attempt to parse CLI args from the test runner.
    # To keep the test deterministic and offline, we invoke it with a dummy argv.
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
