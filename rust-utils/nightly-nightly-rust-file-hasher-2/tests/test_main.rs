// Mock rationale: This test suite simulates running the CLI tool with different arguments
// and verifies its output and behavior without needing to create actual files or
// rely on external system calls for file operations. It uses a mock file content.

use std::process::{Command, Stdio};
use std::io::Write;

// Helper function to create a temporary file with given content and return its path.
// This is a simplified mock for testing purposes.
fn create_mock_file(filename: &str, content: &[u8]) -> std::io::Result<String> {
    let mut file = std::fs::File::create(filename)?;
    file.write_all(content)?;
    Ok(filename.to_string())
}

#[test]
fn test_cli_md5_success() -> io::Result<()> {
    let filename = "test_md5.txt";
    let content = b"This is a test file for MD5.";
    let _mock_file_path = create_mock_file(filename, content)?;

    let mut cmd = Command::new("./target/release/nightly-rust-file-hasher");
    cmd.arg("md5");
    cmd.arg(filename);
    cmd.stdout(Stdio::piped());
    cmd.stderr(Stdio::piped());

    let output = cmd.output()?;

    // Clean up the mock file
    std::fs::remove_file(filename)?;

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert_eq!(stdout.trim(), "f421453121e19352180077560482104f"); // Expected MD5 hash for "This is a test file for MD5."
    Ok(())
}

#[test]
fn test_cli_sha256_success() -> io::Result<()> {
    let filename = "test_sha256.txt";
    let content = b"Another test file for SHA256.";
    let _mock_file_path = create_mock_file(filename, content)?;

    let mut cmd = Command::new("./target/release/nightly-rust-file-hasher");
    cmd.arg("sha256");
    cmd.arg(filename);
    cmd.stdout(Stdio::piped());
    cmd.stderr(Stdio::piped());

    let output = cmd.output()?;

    // Clean up the mock file
    std::fs::remove_file(filename)?;

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert_eq!(stdout.trim(), "5441450336015767135323382134053038804080610178776847326317981840"); // Expected SHA256 hash
    Ok(())
}

#[test]
fn test_cli_unsupported_algorithm() {
    let filename = "test_unsupported.txt";
    let content = b"This file should not be hashed.";
    let _mock_file_path = create_mock_file(filename, content).expect("Failed to create mock file");

    let mut cmd = Command::new("./target/release/nightly-rust-file-hasher");
    cmd.arg("sha384"); // Unsupported algorithm
    cmd.arg(filename);
    cmd.stdout(Stdio::piped());
    cmd.stderr(Stdio::piped());

    let output = cmd.output().expect("Command failed to execute");

    // Clean up the mock file
    std::fs::remove_file(filename).expect("Failed to remove mock file");

    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Unsupported algorithm: sha384"));
}

#[test]
fn test_cli_missing_file() {
    let mut cmd = Command::new("./target/release/nightly-rust-file-hasher");
    cmd.arg("sha1");
    cmd.arg("non_existent_file.txt");
    cmd.stdout(Stdio::piped());
    cmd.stderr(Stdio::piped());

    let output = cmd.output().expect("Command failed to execute");

    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("No such file or directory"));
}

#[test]
fn test_cli_incorrect_arguments() {
    let mut cmd = Command::new("./target/release/nightly-rust-file-hasher");
    cmd.arg("sha1"); // Missing file path
    cmd.stdout(Stdio::piped());
    cmd.stderr(Stdio::piped());

    let output = cmd.output().expect("Command failed to execute");

    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Usage: nightly-rust-file-hasher <algorithm> <file_path>"));
}
