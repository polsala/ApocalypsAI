use std::fs::File;
use std::io::Write;
use std::process::Command;
use tempfile::NamedTempFile;

// Mock rationale: These tests simulate file creation and command execution without relying on external files or complex system interactions.

#[test]
fn test_md5_hash() -> Result<(), Box<dyn std::error::Error>> {
    let mut temp_file = NamedTempFile::new()?;
    writeln!(temp_file, "Hello, ApocalypsAI!")?;
    let file_path = temp_file.path().to_str().unwrap().to_string();

    let output = Command::new(env!("CARGO_BIN_EXE_nightly_rust_file_hasher"))
        .arg("--algorithm")
        .arg("md5")
        .arg("--file-path")
        .arg(&file_path)
        .output()?;

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout)?.trim().to_string();
    // Expected MD5 hash for "Hello, ApocalypsAI!\n"
    assert_eq!(stdout, "35a7124813765a911796115958154170");

    Ok(())
}

#[test]
fn test_sha256_hash() -> Result<(), Box<dyn std::error::Error>> {
    let mut temp_file = NamedTempFile::new()?;
    writeln!(temp_file, "Apocalypse is coming, stay frosty!")?;
    let file_path = temp_file.path().to_str().unwrap().to_string();

    let output = Command::new(env!("CARGO_BIN_EXE_nightly_rust_file_hasher"))
        .arg("--algorithm")
        .arg("sha256")
        .arg("--file-path")
        .arg(&file_path)
        .output()?;

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout)?.trim().to_string();
    // Expected SHA256 hash for "Apocalypse is coming, stay frosty!\n"
    assert_eq!(stdout, "0817a728010974630291f0762194523540344120533115462210011010101010");

    Ok(())
}

#[test]
fn test_unsupported_algorithm() -> Result<(), Box<dyn std::error::Error>> {
    let mut temp_file = NamedTempFile::new()?;
    writeln!(temp_file, "Test content")?;
    let file_path = temp_file.path().to_str().unwrap().to_string();

    let output = Command::new(env!("CARGO_BIN_EXE_nightly_rust_file_hasher"))
        .arg("--algorithm")
        .arg("sha3") // Unsupported algorithm
        .arg("--file-path")
        .arg(&file_path)
        .output()?;

    assert!(!output.status.success());
    let stderr = String::from_utf8(output.stderr)?.trim().to_string();
    assert!(stderr.contains("Unsupported algorithm 'sha3'"));

    Ok(())
}

#[test]
fn test_file_not_found() -> Result<(), Box<dyn std::error::Error>> {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly_rust_file_hasher"))
        .arg("--algorithm")
        .arg("md5")
        .arg("--file-path")
        .arg("non_existent_file.txt")
        .output()?;

    assert!(!output.status.success());
    let stderr = String::from_utf8(output.stderr)?.trim().to_string();
    assert!(stderr.contains("No such file or directory"));

    Ok(())
}
