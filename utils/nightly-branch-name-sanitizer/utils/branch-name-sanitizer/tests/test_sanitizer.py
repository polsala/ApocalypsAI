import unittest
from src.sanitizer import sanitize_branch_name

class TestBranchNameSanitizer(unittest.TestCase):
    def test_basic_conversion(self):
        self.assertEqual(sanitize_branch_name("My Feature! #1"), "my-feature-1")

    def test_multiple_spaces_and_symbols(self):
        raw = "  ***Crazy   Feature---Name!!!   "
        expected = "crazy-feature-name"
        self.assertEqual(sanitize_branch_name(raw), expected)

    def test_leading_non_letter(self):
        self.assertEqual(sanitize_branch_name("123start"), "branch-123start")
        self.assertEqual(sanitize_branch_name("_underscore"), "branch-underscore")

    def test_max_length_truncation(self):
        long_name = "a" * 60  # 60 a's
        result = sanitize_branch_name(long_name)
        self.assertTrue(len(result) <= 50)
        self.assertEqual(result, "a" * 50)

    def test_idempotent_on_clean_name(self):
        clean = "feature-xyz"
        self.assertEqual(sanitize_branch_name(clean), clean)

    def test_type_error_on_non_string(self):
        with self.assertRaises(TypeError):
            sanitize_branch_name(12345)  # type: ignore

if __name__ == "__main__":
    unittest.main()
