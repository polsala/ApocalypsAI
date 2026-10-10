use assert_cmd::prelude::*;
use predicates::prelude::*;
use std::process::Command;
use std::io::Write;
use tempfile::NamedTempFile;

#[test]
fn file_not_found() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Testing the CLI's error handling for a non-existent file path.
    // This is deterministic as it doesn't rely on external state beyond the file system's
    // ability to report a file as not found, which is consistent.
    let mut cmd = Command::cargo_bin("nightly-chrono-hash-stabilizer")?;
    cmd.arg("-f").arg("non_existent_file.txt");
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("Error: File not found"));
    Ok(())
}

#[test]
fn zero_iterations_error() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Testing the CLI's error handling for invalid input (zero iterations).
    // This is deterministic as it only checks argument parsing and internal validation.
    let mut file = NamedTempFile::new()?;
    writeln!(file, "test content")?;
    let file_path = file.path().to_path_buf();

    let mut cmd = Command::cargo_bin("nightly-chrono-hash-stabilizer")?;
    cmd.arg("-f").arg(&file_path).arg("-i").arg("0");
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("Error: Iterations must be greater than 0."));
    Ok(())
}

#[test]
fn basic_stabilization() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Creating a temporary file with known content to ensure deterministic hashing.
    // The file content is controlled, and SHA256 is a deterministic algorithm. This tests the full
    // execution path of the CLI tool in a controlled environment, confirming it processes a file
    // and reports 100% stability for an unchanging file.
    let mut file = NamedTempFile::new()?;
    let content = "ApocalypsAI is integrating!";
    writeln!(file, "{}", content)?;
    let file_path = file.path().to_path_buf();

    let mut cmd = Command::cargo_bin("nightly-chrono-hash-stabilizer")?;
    cmd.arg("-f").arg(&file_path).arg("-i").arg("3"); // 3 iterations for quick test
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Temporal Stability Score: 100.00%"))
        .stdout(predicate::str::contains("Status: Perfectly stable across all temporal observations. A beacon of consistency!"));
    Ok(())
}
