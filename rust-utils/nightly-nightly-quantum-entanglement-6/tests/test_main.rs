use std::fs;
use std::path::Path;
use std::process::Command;

const BIN_PATH: &str = "target/release/nightly-quantum-entanglement-checker";

/// Helper to create a temporary test file
fn create_test_file(path: &str, content: &str) {
    fs::write(path, content).expect("Failed to create test file");
}

/// Helper to run the binary and capture output
fn run_checker(args: &[&str]) -> (String, String, i32) {
    let output = Command::new(BIN_PATH)
        .args(args)
        .output()
        .expect("Failed to run checker");
    
    let stdout = String::from_utf8_lossy(&output.stdout).to_string();
    let stderr = String::from_utf8_lossy(&output.stderr).to_string();
    let status = output.status.code().unwrap_or(-1);
    
    (stdout, stderr, status)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_help_output() {
        // Test help flag
        let (stdout, stderr, status) = run_checker(&["--help"]);
        
        assert_eq!(status, 0, "Help should exit with code 0");
        assert!(stdout.contains("Quantum Entanglement Checker"), "Help should contain title");
        assert!(stdout.contains("Usage:"), "Help should contain usage");
        assert!(stdout.contains("<file1> <file2>"), "Help should show usage pattern");
        assert!(stderr.is_empty(), "Help should not write to stderr");
    }

    #[test]
    fn test_short_help_flag() {
        // Test short help flag
        let (stdout, stderr, status) = run_checker(&["-h"]);
        
        assert_eq!(status, 0, "Short help should exit with code 0");
        assert!(stdout.contains("Quantum Entanglement Checker"), "Help should contain title");
        assert!(stderr.is_empty(), "Help should not write to stderr");
    }

    #[test]
    fn test_insufficient_arguments() {
        // Test with no arguments
        let (stdout, stderr, status) = run_checker(&[]);
        
        assert_eq!(status, 1, "Should exit with code 1 for insufficient args");
        assert!(stderr.contains("Error:"), "Should write error to stderr");
        assert!(stderr.contains("two file paths"), "Error should mention file paths");
        assert!(stdout.is_empty(), "Should not write to stdout on error");
    }

    #[test]
    fn test_nonexistent_file() {
        // Test with non-existent file
        let (stdout, stderr, status) = run_checker(&["nonexistent.txt", "also_nonexistent.txt"]);
        
        assert_eq!(status, 1, "Should exit with code 1 for non-existent file");
        assert!(stderr.contains("File not found"), "Should report file not found");
        assert!(stdout.is_empty(), "Should not write to stdout on error");
    }

    #[test]
    fn test_identical_files() {
        // Create two identical test files
        create_test_file("test_identical_1.txt", "Hello, quantum world!");
        create_test_file("test_identical_2.txt", "Hello, quantum world!");
        
        let (stdout, stderr, status) = run_checker(&["test_identical_1.txt", "test_identical_2.txt"]);
        
        // Cleanup
        let _ = fs::remove_file("test_identical_1.txt");
        let _ = fs::remove_file("test_identical_2.txt");
        
        assert_eq!(status, 0, "Should exit with code 0 for successful comparison");
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"), "Should detect entanglement");
        assert!(stdout.contains("quantum-entangled (identical)"), "Should report identical");
        assert!(stdout.contains("Spooky action at a distance confirmed"), "Should mention spooky action");
        assert!(stderr.is_empty(), "Should not write to stderr on success");
    }

    #[test]
    fn test_different_files() {
        // Create two different test files
        create_test_file("test_diff_1.txt", "Hello, quantum world!");
        create_test_file("test_diff_2.txt", "Hello, classical world!");
        
        let (stdout, stderr, status) = run_checker(&["test_diff_1.txt", "test_diff_2.txt"]);
        
        // Cleanup
        let _ = fs::remove_file("test_diff_1.txt");
        let _ = fs::remove_file("test_diff_2.txt");
        
        assert_eq!(status, 0, "Should exit with code 0 for successful comparison");
        assert!(stdout.contains("QUANTUM ENTANGLEMENT NOT FOUND"), "Should report no entanglement");
        assert!(stdout.contains("not quantum-entangled (different)"), "Should report different");
        assert!(stdout.contains("No spooky action detected"), "Should mention no spooky action");
        assert!(stderr.is_empty(), "Should not write to stderr on success");
    }

    #[test]
    fn test_verbose_flag() {
        // Create two identical test files
        create_test_file("test_verbose_1.txt", "Quantum content for verbose testing");
        create_test_file("test_verbose_2.txt", "Quantum content for verbose testing");
        
        let (stdout, stderr, status) = run_checker(&["test_verbose_1.txt", "test_verbose_2.txt", "--verbose"]);
        
        // Cleanup
        let _ = fs::remove_file("test_verbose_1.txt");
        let _ = fs::remove_file("test_verbose_2.txt");
        
        assert_eq!(status, 0, "Should exit with code 0 for verbose comparison");
        assert!(stdout.contains("Verbose Details"), "Should show verbose details");
        assert!(stdout.contains("Identical: true"), "Should report identical status");
        assert!(stderr.is_empty(), "Should not write to stderr on success");
    }

    #[test]
    fn test_short_verbose_flag() {
        // Create two different test files
        create_test_file("test_short_v_1.txt", "Short verbose test");
        create_test_file("test_short_v_2.txt", "Short verbose different");
        
        let (stdout, stderr, status) = run_checker(&["test_short_v_1.txt", "test_short_v_2.txt", "-v"]);
        
        // Cleanup
        let _ = fs::remove_file("test_short_v_1.txt");
        let _ = fs::remove_file("test_short_v_2.txt");
        
        assert_eq!(status, 0, "Should exit with code 0 for short verbose comparison");
        assert!(stdout.contains("Verbose Details"), "Should show verbose details with -v");
        assert!(stderr.is_empty(), "Should not write to stderr on success");
    }

    #[test]
    fn test_large_files() {
        // Create large test files (1MB each)
        let large_content = "0123456789".repeat(100_000); // ~1MB
        create_test_file("test_large_1.txt", &large_content);
        create_test_file("test_large_2.txt", &large_content);
        
        let (stdout, stderr, status) = run_checker(&["test_large_1.txt", "test_large_2.txt"]);
        
        // Cleanup
        let _ = fs::remove_file("test_large_1.txt");
        let _ = fs::remove_file("test_large_2.txt");
        
        assert_eq!(status, 0, "Should handle large files successfully");
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"), "Should detect entanglement for large files");
        assert!(stderr.is_empty(), "Should not write to stderr on success");
    }

    #[test]
    fn test_empty_files() {
        // Create empty test files
        create_test_file("test_empty_1.txt", "");
        create_test_file("test_empty_2.txt", "");
        
        let (stdout, stderr, status) = run_checker(&["test_empty_1.txt", "test_empty_2.txt"]);
        
        // Cleanup
        let _ = fs::remove_file("test_empty_1.txt");
        let _ = fs::remove_file("test_empty_2.txt");
        
        assert_eq!(status, 0, "Should handle empty files successfully");
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"), "Should detect entanglement for empty files");
        assert!(stderr.is_empty(), "Should not write to stderr on success");
    }

    #[test]
    fn test_mixed_case_flags() {
        // Test case sensitivity of flags
        let (stdout, stderr, status) = run_checker(&["--HELP"]);
        
        // Most Rust CLIs are case-sensitive, so this should work as --help
        assert_eq!(status, 0, "Should handle uppercase flags");
        assert!(stdout.contains("Quantum Entanglement Checker"), "Should show help for uppercase flag");
        assert!(stderr.is_empty(), "Should not write to stderr");
    }

    #[test]
    fn test_unicode_content() {
        // Create files with Unicode content
        let unicode_content = "🎉 Quantum Entanglement 🧪
 spooky action at a distance ✨
 测试中文内容 🚀";
        create_test_file("test_unicode_1.txt", unicode_content);
        create_test_file("test_unicode_2.txt", unicode_content);
        
        let (stdout, stderr, status) = run_checker(&["test_unicode_1.txt", "test_unicode_2.txt"]);
        
        // Cleanup
        let _ = fs::remove_file("test_unicode_1.txt");
        let _ = fs::remove_file("test_unicode_2.txt");
        
        assert_eq!(status, 0, "Should handle Unicode content");
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"), "Should detect entanglement for Unicode");
        assert!(stderr.is_empty(), "Should not write to stderr on success");
    }

    #[test]
    fn test_file_with_newlines() {
        // Create files with different newline patterns
        create_test_file("test_newlines_1.txt", "Line 1\nLine 2\nLine 3");
        create_test_file("test_newlines_2.txt", "Line 1\nLine 2\nLine 3");
        
        let (stdout, stderr, status) = run_checker(&["test_newlines_1.txt", "test_newlines_2.txt"]);
        
        // Cleanup
        let _ = fs::remove_file("test_newlines_1.txt");
        let _ = fs::remove_file("test_newlines_2.txt");
        
        assert_eq!(status, 0, "Should handle files with newlines");
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"), "Should detect entanglement with newlines");
        assert!(stderr.is_empty(), "Should not write to stderr on success");
    }

    #[test]
    fn test_help_with_extra_args() {
        // Test that help is shown even with extra arguments
        let (stdout, stderr, status) = run_checker(&["--help", "extra_arg"]);
        
        assert_eq!(status, 0, "Should show help even with extra args");
        assert!(stdout.contains("Quantum Entanglement Checker"), "Should show help content");
        assert!(stderr.is_empty(), "Should not write to stderr");
    }

    #[test]
    fn test_file_path_with_spaces() {
        // Create files with spaces in names
        create_test_file("test file with spaces 1.txt", "Content with spaces");
        create_test_file("test file with spaces 2.txt", "Content with spaces");
        
        let (stdout, stderr, status) = run_checker(&["test file with spaces 1.txt", "test file with spaces 2.txt"]);
        
        // Cleanup
        let _ = fs::remove_file("test file with spaces 1.txt");
        let _ = fs::remove_file("test file with spaces 2.txt");
        
        assert_eq!(status, 0, "Should handle file paths with spaces");
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"), "Should detect entanglement for files with spaces");
        assert!(stderr.is_empty(), "Should not write to stderr on success");
    }

    #[test]
    fn test_different_file_extensions() {
        // Test with different file extensions but same content
        create_test_file("test_different_ext.txt", "Same content");
        create_test_file("test_different_ext.md", "Same content");
        
        let (stdout, stderr, status) = run_checker(&["test_different_ext.txt", "test_different_ext.md"]);
        
        // Cleanup
        let _ = fs::remove_file("test_different_ext.txt");
        let _ = fs::remove_file("test_different_ext.md");
        
        assert_eq!(status, 0, "Should handle different file extensions");
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"), "Should detect entanglement regardless of extension");
        assert!(stderr.is_empty(), "Should not write to stderr on success");
    }

    #[test]
    fn test_binary_files() {
        // Create binary test files
        let binary_content = vec![0u8, 1, 2, 3, 4, 5, 255, 254, 253, 252];
        fs::write("test_binary_1.bin", &binary_content).expect("Failed to create binary test file 1");
        fs::write("test_binary_2.bin", &binary_content).expect("Failed to create binary test file 2");
        
        let (stdout, stderr, status) = run_checker(&["test_binary_1.bin", "test_binary_2.bin"]);
        
        // Cleanup
        let _ = fs::remove_file("test_binary_1.bin");
        let _ = fs::remove_file("test_binary_2.bin");
        
        assert_eq!(status, 0, "Should handle binary files");
        assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"), "Should detect entanglement for binary files");
        assert!(stderr.is_empty(), "Should not write to stderr on success");
    }

    #[test]
    fn test_file_size_formatting() {
        // Create a file of specific size to test formatting
        let content = "x".repeat(1536); // 1.5 KB
        create_test_file("test_size.txt", &content);
        create_test_file("test_size_copy.txt", &content);
        
        let (stdout, stderr, status) = run_checker(&["test_size.txt", "test_size_copy.txt"]);
        
        // Cleanup
        let _ = fs::remove_file("test_size.txt");
        let _ = fs::remove_file("test_size_copy.txt");
        
        assert_eq!(status, 0, "Should handle size formatting");
        assert!(stdout.contains("1.5 KB"), "Should format 1536 bytes as 1.5 KB");
        assert!(stderr.is_empty(), "Should not write to stderr on success");
    }
}
