use super::*;
use std::io::Write;
use tempfile::NamedTempFile;

// Mock rationale: This function creates a temporary file with specific content.
// It's a utility for testing and doesn't rely on external services or complex logic.
fn create_temp_file(content: &str) -> NamedTempFile {
    let mut temp_file = NamedTempFile::new().expect("Failed to create temp file");
    temp_file.write_all(content.as_bytes()).expect("Failed to write to temp file");
    temp_file
}

#[test]
fn test_calculate_md5_hash() {
    let temp_file = create_temp_file("hello world");
    let file_path = temp_file.path();
    let hash = calculate_hash(file_path, HashAlgorithm::Md5).expect("MD5 calculation failed");
    assert_eq!(hash, "5eb63bbbe01eeed093cb22bb8f5acdc3");
}

#[test]
fn test_calculate_sha1_hash() {
    let temp_file = create_temp_file("hello world");
    let file_path = temp_file.path();
    let hash = calculate_hash(file_path, HashAlgorithm::Sha1).expect("SHA1 calculation failed");
    assert_eq!(hash, "2aae6c014333170298fc826442134916021256da");
}

#[test]
fn test_calculate_sha256_hash() {
    let temp_file = create_temp_file("hello world");
    let file_path = temp_file.path();
    let hash = calculate_hash(file_path, HashAlgorithm::Sha256).expect("SHA256 calculation failed");
    assert_eq!(hash, "b94d27b9934d3e08a52e52d7712fb54e4a703fce5027c82164892092332877f1");
}

#[test]
fn test_calculate_hash_empty_file() {
    let temp_file = create_temp_file("");
    let file_path = temp_file.path();
    let hash_md5 = calculate_hash(file_path, HashAlgorithm::Md5).expect("MD5 calculation failed");
    assert_eq!(hash_md5, "d41d8cd98f00b204e9800998ecf8427e");

    let hash_sha256 = calculate_hash(file_path, HashAlgorithm::Sha256).expect("SHA256 calculation failed");
    assert_eq!(hash_sha256, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
}

#[test]
fn test_algorithm_from_str() {
    assert_eq!(HashAlgorithm::from_str("md5"), Some(HashAlgorithm::Md5));
    assert_eq!(HashAlgorithm::from_str("SHA1"), Some(HashAlgorithm::Sha1));
    assert_eq!(HashAlgorithm::from_str("sHa256"), Some(HashAlgorithm::Sha256));
    assert_eq!(HashAlgorithm::from_str("unknown"), None);
}

#[test]
fn test_algorithm_name() {
    assert_eq!(HashAlgorithm::Md5.name(), "MD5");
    assert_eq!(HashAlgorithm::Sha1.name(), "SHA1");
    assert_eq!(HashAlgorithm::Sha256.name(), "SHA256");
}

// Mock rationale: This integration test simulates running the CLI tool.
// It uses `std::process::Command` to execute the compiled binary.
// This is a standard way to test CLI applications and doesn't require external services.
#[test]
fn test_cli_usage() {
    // This test requires the binary to be built. In a real CI, you'd build it first.
    // For local testing, ensure you run `cargo test` in the project root.
    // We'll assume the binary is available in target/debug/ or target/release/.
    // For simplicity, we'll try to run it directly.

    let temp_file = create_temp_file("cli test content");
    let file_path = temp_file.path().to_str().unwrap();

    // Test default algorithm (SHA256)
    let output_default = std::process::Command::new(env!("CARGO_BIN_EXE_nightly-rust-file-hasher"))
        .arg(file_path)
        .output()
        .expect("Failed to execute CLI command");

    assert!(output_default.status.success());
    let stdout_default = String::from_utf8(output_default.stdout).unwrap();
    assert!(stdout_default.contains("SHA256 (single-thread): "));
    let expected_sha256 = "a227878b1e65934451887113041791378226542145636056213211102922864c";
    assert!(stdout_default.contains(expected_sha256));

    // Test with MD5 algorithm
    let output_md5 = std::process::Command::new(env!("CARGO_BIN_EXE_nightly-rust-file-hasher"))
        .arg(file_path)
        .arg("--algorithm")
        .arg("md5")
        .output()
        .expect("Failed to execute CLI command");

    assert!(output_md5.status.success());
    let stdout_md5 = String::from_utf8(output_md5.stdout).unwrap();
    assert!(stdout_md5.contains("MD5 (single-thread): "));
    let expected_md5 = "5eb63bbbe01eeed093cb22bb8f5acdc3";
    assert!(stdout_md5.contains(expected_md5));

    // Test with invalid algorithm
    let output_invalid = std::process::Command::new(env!("CARGO_BIN_EXE_nightly-rust-file-hasher"))
        .arg(file_path)
        .arg("--algorithm")
        .arg("invalid_algo")
        .output()
        .expect("Failed to execute CLI command");

    assert!(!output_invalid.status.success());
    let stderr_invalid = String::from_utf8(output_invalid.stderr).unwrap();
    assert!(stderr_invalid.contains("Invalid algorithm specified"));
}
