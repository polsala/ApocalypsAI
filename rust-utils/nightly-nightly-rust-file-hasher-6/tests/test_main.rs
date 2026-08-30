use std::process::Command;
use std::io::Write;
use tempfile::NamedTempFile;

// Mock rationale: These tests use `tempfile` to create temporary files and `Command` to run the compiled binary. This allows for deterministic testing without relying on pre-existing files or complex mocking frameworks for external processes.

#[test]
fn test_sha256_default_output() {
    let mut file = NamedTempFile::new().expect("Failed to create temp file");
    let content = b"This is a test string for SHA256.";
    file.write_all(content).expect("Failed to write to temp file");
    let file_path = file.path().to_str().expect("Failed to get file path");

    let output = Command::new("./target/release/nightly-rust-file-hasher")
        .arg(file_path)
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).expect("Failed to parse stdout");
    let expected_len = 64; // SHA256 hex is 64 characters
    assert_eq!(stdout.trim().len(), expected_len);
    assert!(stdout.trim().chars().all(|c| c.is_digit(16) || (c >= 'a' && c <= 'f')));
}

#[test]
fn test_md5_hex_output() {
    let mut file = NamedTempFile::new().expect("Failed to create temp file");
    let content = b"Another test for MD5.";
    file.write_all(content).expect("Failed to write to temp file");
    let file_path = file.path().to_str().expect("Failed to get file path");

    let output = Command::new("./target/release/nightly-rust-file-hasher")
        .arg(file_path)
        .arg("--algorithm")
        .arg("md5")
        .arg("--output")
        .arg("hex")
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).expect("Failed to parse stdout");
    let expected_len = 32; // MD5 hex is 32 characters
    assert_eq!(stdout.trim().len(), expected_len);
    assert!(stdout.trim().chars().all(|c| c.is_digit(16) || (c >= 'a' && c <= 'f')));
}

#[test]
fn test_sha1_base64_output() {
    let mut file = NamedTempFile::new().expect("Failed to create temp file");
    let content = b"Test for SHA1 in Base64.";
    file.write_all(content).expect("Failed to write to temp file");
    let file_path = file.path().to_str().expect("Failed to get file path");

    let output = Command::new("./target/release/nightly-rust-file-hasher")
        .arg(file_path)
        .arg("--algorithm")
        .arg("sha1")
        .arg("--output")
        .arg("base64")
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).expect("Failed to parse stdout");
    // Base64 length is not fixed, but we can check for valid characters and non-empty output.
    let trimmed_stdout = stdout.trim();
    assert!(!trimmed_stdout.is_empty());
    assert!(trimmed_stdout.chars().all(|c| c.is_ascii_alphanumeric() || c == '+' || c == '/' || c == '='));
}

#[test]
fn test_file_not_found_error() {
    let output = Command::new("./target/release/nightly-rust-file-hasher")
        .arg("non_existent_file.xyz")
        .output()
        .expect("Failed to execute command");

    assert!(!output.status.success());
    let stderr = String::from_utf8(output.stderr).expect("Failed to parse stderr");
    assert!(stderr.contains("No such file or directory"));
}

#[test]
fn test_unsupported_algorithm_error() {
    let mut file = NamedTempFile::new().expect("Failed to create temp file");
    let content = b"Some content.";
    file.write_all(content).expect("Failed to write to temp file");
    let file_path = file.path().to_str().expect("Failed to get file path");

    let output = Command::new("./target/release/nightly-rust-file-hasher")
        .arg(file_path)
        .arg("--algorithm")
        .arg("sha512") // Unsupported algorithm
        .output()
        .expect("Failed to execute command");

    assert!(!output.status.success());
    let stderr = String::from_utf8(output.stderr).expect("Failed to parse stderr");
    assert!(stderr.contains("Unsupported algorithm. Use md5, sha1, or sha256."));
}
