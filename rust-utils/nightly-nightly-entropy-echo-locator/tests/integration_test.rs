use std::fs::{self, File};
use std::io::Write;
use std::path::Path;
use assert_cmd::Command;
use tempfile::tempdir;

// Mock rationale: Creating temporary files with known content allows for deterministic
// and offline testing of the entropy calculation logic without relying on external resources.

#[test]
fn test_empty_file_entropy() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("empty.txt");
    File::create(&file_path)?.write_all(b"")?;

    let mut cmd = Command::cargo_bin("nightly-entropy-echo-locator")?;
    cmd.arg(&file_path);

    cmd.assert()
        .success()
        .stdout(format!("File: {}, Entropy: 0.000 bits/byte\n", file_path.display()));

    Ok(())
}

#[test]
fn test_zero_byte_file_entropy() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("zeros.bin");
    File::create(&file_path)?.write_all(&vec![0; 100])?;

    let mut cmd = Command::cargo_bin("nightly-entropy-echo-locator")?;
    cmd.arg(&file_path);

    cmd.assert()
        .success()
        .stdout(format!("File: {}, Entropy: 0.000 bits/byte\n", file_path.display()));

    Ok(())
}

#[test]
fn test_repeating_pattern_file_entropy() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("pattern.txt");
    File::create(&file_path)?.write_all(b"ABABABABAB")?;

    let mut cmd = Command::cargo_bin("nightly-entropy-echo-locator")?;
    cmd.arg(&file_path);

    // Expected entropy for 'ABABABABAB' (10 bytes, 5 'A', 5 'B')
    // p_A = 0.5, p_B = 0.5
    // H = - (0.5 * log2(0.5) + 0.5 * log2(0.5))
    // H = - (0.5 * -1 + 0.5 * -1) = - (-0.5 - 0.5) = 1.0
    cmd.assert()
        .success()
        .stdout(format!("File: {}, Entropy: 1.000 bits/byte\n", file_path.display()));

    Ok(())
}

#[test]
fn test_high_entropy_file() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("random.bin");
    // Generate 256 bytes, each unique from 0 to 255
    let data: Vec<u8> = (0..=255).collect();
    File::create(&file_path)?.write_all(&data)?;

    let mut cmd = Command::cargo_bin("nightly-entropy-echo-locator")?;
    cmd.arg(&file_path);

    // For 256 unique bytes, each appearing once, p_i = 1/256
    // H = - sum( (1/256) * log2(1/256) ) for 256 terms
    // H = - 256 * (1/256) * log2(1/256)
    // H = - log2(1/256) = - (-8) = 8.0
    cmd.assert()
        .success()
        .stdout(format!("File: {}, Entropy: 8.000 bits/byte\n", file_path.display()));

    Ok(())
}

#[test]
fn test_multiple_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file1_path = dir.path().join("file1.txt");
    let file2_path = dir.path().join("file2.bin");

    File::create(&file1_path)?.write_all(b"AAAAA")?;
    File::create(&file2_path)?.write_all(&vec![0x00, 0xFF, 0x00, 0xFF])?;

    let mut cmd = Command::cargo_bin("nightly-entropy-echo-locator")?;
    cmd.arg(&file1_path).arg(&file2_path);

    // file1: 'AAAAA' -> Entropy 0.0
    // file2: 0x00, 0xFF, 0x00, 0xFF -> p_00 = 0.5, p_FF = 0.5 -> Entropy 1.0
    let expected_output = format!(
        "File: {}, Entropy: 0.000 bits/byte\nFile: {}, Entropy: 1.000 bits/byte\n",
        file1_path.display(),
        file2_path.display()
    );

    cmd.assert()
        .success()
        .stdout(expected_output);

    Ok(())
}

#[test]
fn test_non_existent_file() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("non_existent.txt");

    let mut cmd = Command::cargo_bin("nightly-entropy-echo-locator")?;
    cmd.arg(&file_path);

    cmd.assert()
        .failure()
        .stderr(predicates::str::contains(format!("Error processing file {}: No such file or directory", file_path.display())));

    Ok(())
}

#[test]
fn test_no_args() -> Result<(), Box<dyn std::error::Error>> {
    let mut cmd = Command::cargo_bin("nightly-entropy-echo-locator")?;

    cmd.assert()
        .failure()
        .stderr(predicates::str::contains("Error: No files provided."));

    Ok(())
}
