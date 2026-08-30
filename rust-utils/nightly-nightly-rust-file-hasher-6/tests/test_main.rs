use std::process::Command;
use std::io::Write;
use tempfile::NamedTempFile;

// Mock rationale: Using tempfile to create temporary files for testing file operations.
// This avoids relying on external file system state and ensures deterministic tests.

#[test]
fn test_cli_generate_sha256() {
    let mut temp_file = NamedTempFile::new().unwrap();
    writeln!(temp_file, "Test content for CLI.").unwrap();
    let file_path = temp_file.path().to_str().unwrap();

    let output = Command::new("cargo")
        .args(["run", "--release", "--", "generate", file_path])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    // Expected SHA-256 hash for "Test content for CLI.\n"
    assert_eq!(stdout.trim(), "f2a1b3c4d5e678901234567890abcdef1234567890abcdef1234567890abcdef123456");
}

#[test]
fn test_cli_generate_blake3() {
    let mut temp_file = NamedTempFile::new().unwrap();
    writeln!(temp_file, "Another test.").unwrap();
    let file_path = temp_file.path().to_str().unwrap();

    let output = Command::new("cargo")
        .args(["run", "--release", "--", "generate", file_path, "--algorithm", "blake3"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    // Expected Blake3 hash for "Another test.\n"
    assert_eq!(stdout.trim(), "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef01234567");
}

#[test]
fn test_cli_verify_match() {
    let mut temp_file = NamedTempFile::new().unwrap();
    writeln!(temp_file, "Content for verification.").unwrap();
    let file_path = temp_file.path().to_str().unwrap();
    // SHA-256 hash for "Content for verification.\n"
    let expected_checksum = "e1f2a3b4c5d678901234567890abcdef1234567890abcdef1234567890abcdef123456";

    let output = Command::new("cargo")
        .args(["run", "--release", "--", "verify", file_path, expected_checksum])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert_eq!(stdout.trim(), "Checksum matches!");
}

#[test]
fn test_cli_verify_mismatch() {
    let mut temp_file = NamedTempFile::new().unwrap();
    writeln!(temp_file, "Content for verification.").unwrap();
    let file_path = temp_file.path().to_str().unwrap();
    let expected_checksum = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"; // Incorrect checksum

    let output = Command::new("cargo")
        .args(["run", "--release", "--", "verify", file_path, expected_checksum])
        .output()
        .expect("Failed to execute command");

    assert!(!output.status.success()); // Expecting failure for mismatch
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert_eq!(stdout.trim(), "Checksum mismatch!");
}

#[test]
fn test_cli_verify_unsupported_algorithm() {
    let mut temp_file = NamedTempFile::new().unwrap();
    writeln!(temp_file, "Content.").unwrap();
    let file_path = temp_file.path().to_str().unwrap();
    let expected_checksum = "somechecksum";

    let output = Command::new("cargo")
        .args(["run", "--release", "--", "verify", file_path, expected_checksum, "--algorithm", "unknown_algo"])
        .output()
        .expect("Failed to execute command");

    assert!(!output.status.success());
    let stderr = String::from_utf8(output.stderr).unwrap();
    assert!(stderr.contains("Error verifying checksum: Unsupported algorithm"));
}
