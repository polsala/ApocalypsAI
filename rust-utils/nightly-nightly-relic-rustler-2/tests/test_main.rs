use std::process::Command;
use std::fs;
use std::io::Write;
use tempfile::NamedTempFile;
use sha2::{Digest, Sha256}; // For calculating expected hashes

// Helper to create a temp file with content
fn create_temp_file(content: &str) -> NamedTempFile {
    let mut file = NamedTempFile::new().expect("Failed to create temp file");
    file.write_all(content.as_bytes()).expect("Failed to write to temp file");
    file
}

// Helper to calculate SHA256 for a given content string
fn calculate_sha256_string(content: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(content.as_bytes());
    format!("{:x}", hasher.finalize())
}

#[test]
fn test_checksum_command() {
    // Mock rationale: Using tempfile for deterministic, offline file operations.
    let content = "The quick brown fox jumps over the lazy dog.";
    let expected_hash = calculate_sha256_string(content);

    let temp_file = create_temp_file(content);
    let path = temp_file.path();

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-relic-rustler"))
        .arg("checksum")
        .arg("--file")
        .arg(path)
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains(&format!("SHA256 of {}: {}", path.display(), expected_hash)));
}

#[test]
fn test_scramble_and_unscramble_commands() {
    // Mock rationale: Using tempfile for deterministic, offline file operations.
    let original_content = "Secret message for the wasteland.";
    let key = "temporal_frequency";

    let original_file = create_temp_file(original_content);
    let scrambled_file = NamedTempFile::new().expect("Failed to create scrambled temp file");
    let unscrambled_file = NamedTempFile::new().expect("Failed to create unscrambled temp file");

    let original_path = original_file.path();
    let scrambled_path = scrambled_file.path();
    let unscrambled_path = unscrambled_file.path();

    // Scramble
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-relic-rustler"))
        .arg("scramble")
        .arg("--input")
        .arg(original_path)
        .arg("--output")
        .arg(scrambled_path)
        .arg("--key")
        .arg(key)
        .output()
        .expect("Failed to execute scramble command");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains(&format!("File '{}' scrambled to '{}' with key.", original_path.display(), scrambled_path.display())));

    // Unscramble
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-relic-rustler"))
        .arg("unscramble")
        .arg("--input")
        .arg(scrambled_path)
        .arg("--output")
        .arg(unscrambled_path)
        .arg("--key")
        .arg(key)
        .output()
        .expect("Failed to execute unscramble command");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains(&format!("File '{}' unscrambled to '{}' with key.", scrambled_path.display(), unscrambled_path.display())));

    let unscrambled_content = fs::read_to_string(unscrambled_path).expect("Failed to read unscrambled file");
    assert_eq!(unscrambled_content, original_content);
}

#[test]
fn test_verify_command_success() {
    // Mock rationale: Using tempfile for deterministic, offline file operations.
    let original_content = "Vital coordinates: N34.0522 W118.2437";
    let key = "whispers_of_the_void";
    let original_hash = calculate_sha256_string(original_content);

    let original_file = create_temp_file(original_content);
    let scrambled_file = NamedTempFile::new().expect("Failed to create scrambled temp file");

    let original_path = original_file.path();
    let scrambled_path = scrambled_file.path();

    // Scramble the file first
    let scramble_output = Command::new(env!("CARGO_BIN_EXE_nightly-relic-rustler"))
        .arg("scramble")
        .arg("--input")
        .arg(original_path)
        .arg("--output")
        .arg(scrambled_path)
        .arg("--key")
        .arg(key)
        .output()
        .expect("Failed to execute scramble command");
    assert!(scramble_output.status.success());

    // Verify
    let verify_output = Command::new(env!("CARGO_BIN_EXE_nightly-relic-rustler"))
        .arg("verify")
        .arg("--scrambled-file")
        .arg(scrambled_path)
        .arg("--original-hash")
        .arg(&original_hash)
        .arg("--key")
        .arg(key)
        .output()
        .expect("Failed to execute verify command");

    assert!(verify_output.status.success());
    let stdout = String::from_utf8_lossy(&verify_output.stdout);
    assert!(stdout.contains("Verification successful! Original content hash matches."));
}

#[test]
fn test_verify_command_failure_wrong_key() {
    // Mock rationale: Using tempfile for deterministic, offline file operations.
    let original_content = "Critical intel: Alpha team rendezvous at sector 7.";
    let correct_key = "secure_channel";
    let wrong_key = "noisy_interference";
    let original_hash = calculate_sha256_string(original_content);

    let original_file = create_temp_file(original_content);
    let scrambled_file = NamedTempFile::new().expect("Failed to create scrambled temp file");

    let original_path = original_file.path();
    let scrambled_path = scrambled_file.path();

    // Scramble the file with the correct key
    let scramble_output = Command::new(env!("CARGO_BIN_EXE_nightly-relic-rustler"))
        .arg("scramble")
        .arg("--input")
        .arg(original_path)
        .arg("--output")
        .arg(scrambled_path)
        .arg("--key")
        .arg(correct_key)
        .output()
        .expect("Failed to execute scramble command");
    assert!(scramble_output.status.success());

    // Verify with the WRONG key
    let verify_output = Command::new(env!("CARGO_BIN_EXE_nightly-relic-rustler"))
        .arg("verify")
        .arg("--scrambled-file")
        .arg(scrambled_path)
        .arg("--original-hash")
        .arg(&original_hash)
        .arg("--key")
        .arg(wrong_key)
        .output()
        .expect("Failed to execute verify command");

    assert!(!verify_output.status.success()); // Expect failure
    let stderr = String::from_utf8_lossy(&verify_output.stderr);
    assert!(stderr.contains("Verification FAILED!"));
}

#[test]
fn test_scramble_command_empty_key_error() {
    // Mock rationale: Using tempfile for deterministic, offline file operations.
    let original_content = "Some data.";
    let key = ""; // Empty key

    let original_file = create_temp_file(original_content);
    let scrambled_file = NamedTempFile::new().expect("Failed to create scrambled temp file");

    let original_path = original_file.path();
    let scrambled_path = scrambled_file.path();

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-relic-rustler"))
        .arg("scramble")
        .arg("--input")
        .arg(original_path)
        .arg("--output")
        .arg(scrambled_path)
        .arg("--key")
        .arg(key)
        .output()
        .expect("Failed to execute scramble command");

    assert!(!output.status.success()); // Expect failure
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Key cannot be empty"));
}
