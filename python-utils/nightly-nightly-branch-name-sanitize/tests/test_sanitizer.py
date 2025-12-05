import unittest
import os
import tempfile
from sanitizer import sanitize_branch_name, validate_branch_name


class TestBranchNameSanitizer(unittest.TestCase):
    """Test cases for branch name sanitization."""
    
    def test_basic_sanitization(self):
        """Test basic character replacement."""
        result = sanitize_branch_name("feature/unsafe#branch@name")
        expected = "feature/unsafe-branch-name"
        self.assertEqual(result, expected)
    
    def test_multiple_special_chars(self):
        """Test multiple consecutive special characters."""
        result = sanitize_branch_name("feature///test###name@@@")
        expected = "feature/test-name"
        self.assertEqual(result, expected)
    
    def test_leading_trailing_hyphens(self):
        """Test removal of leading/trailing hyphens."""
        result = sanitize_branch_name("---feature-test---")
        expected = "feature-test"
        self.assertEqual(result, expected)
    
    def test_empty_after_sanitization(self):
        """Test handling of empty result after sanitization."""
        result = sanitize_branch_name("###@@@!!!")
        expected = "sanitized-branch"
        self.assertEqual(result, expected)
    
    def test_slash_handling(self):
        """Test slash removal at start and end."""
        result = sanitize_branch_name("/feature/test/")
        expected = "feature/test"
        self.assertEqual(result, expected)
    
    def test_allow_special_chars(self):
        """Test allowing additional special characters."""
        result = sanitize_branch_name("feature+test=name", allow_special_chars="+=")
        expected = "feature+test=name"
        self.assertEqual(result, expected)
    
    def test_empty_branch_name(self):
        """Test error handling for empty branch name."""
        with self.assertRaises(ValueError):
            sanitize_branch_name("")
    
    def test_valid_git_names(self):
        """Test validation of valid Git branch names."""
        valid_names = [
            "feature/test",
            "bugfix/hotfix",
            "release/v1.0",
            "main",
            "develop",
            "feature-123",
            "_private_branch"
        ]
        
        for name in valid_names:
            with self.subTest(name=name):
                self.assertTrue(validate_branch_name(name))
    
    def test_invalid_git_names(self):
        """Test validation of invalid Git branch names."""
        invalid_names = [
            "feature..test",      # Consecutive dots
            "feature test",       # Whitespace
            "feature~test",       # Tilde
            "feature^test",       # Caret
            "-feature",           # Starts with dash
            "feature/./test",     # Contains /./
            "feature/../test",    # Contains /../
            "@{test}",            # Contains @{
            "feature\test",      # Contains backslash
            "feature:test",       # Contains colon
            "feature?test",       # Contains question mark
            "feature*test",       # Contains asterisk
            "feature[test",       # Contains bracket
            "feature\ntest",     # Contains newline
            " feature",          # Starts with space
            "feature "           # Ends with space
        ]
        
        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(validate_branch_name(name))
    
    def test_integration_sanitization_and_validation(self):
        """Integration test: sanitize then validate."""
        unsafe_names = [
            "feature/unsafe#branch@name",
            "bugfix..hotfix",
            "release/v1.0-beta",
            "feature test name",
            "---invalid---"
        ]
        
        for unsafe_name in unsafe_names:
            with self.subTest(unsafe_name=unsafe_name):
                sanitized = sanitize_branch_name(unsafe_name)
                # After sanitization, the name should be valid
                self.assertTrue(validate_branch_name(sanitized), 
                              f"Sanitized name '{sanitized}' is not valid for Git")
    
    def test_file_output(self):
        """Test writing sanitized name to file."""
        unsafe_name = "feature/unsafe#branch@name"
        expected = "feature/unsafe-branch-name"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file = f.name
        
        try:
            # Simulate command line arguments
            import sys
            original_args = sys.argv
            sys.argv = ['sanitizer.py', '--branch', unsafe_name, '--output', temp_file]
            
            # Import and run main function
            from sanitizer import main
            main()
            
            # Check file contents
            with open(temp_file, 'r') as f:
                result = f.read().strip()
            
            self.assertEqual(result, expected)
            
        finally:
            sys.argv = original_args
            os.unlink(temp_file)


if __name__ == '__main__':
    # Mock rationale: These tests verify that branch names are properly sanitized
    # and validated according to Git standards, ensuring CI/CD pipeline safety.
    unittest.main()
