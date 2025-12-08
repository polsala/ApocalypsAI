use std::fs::{self, File};
use std::io::Write;
use std::path::{Path, PathBuf};
use tempfile::tempdir; // For creating temporary directories for tests
use assert_cmd::Command; // For running the CLI tool as a command
use predicates::prelude::*; // For asserting on command output

// Mock rationale: These tests operate on the local file system by creating temporary files
// and directories. This is a deterministic and offline way to test a file system utility.
// No external services or network calls are made. The temporary files serve as controlled
// "mock" inputs for the CLI tool.

#[test]
fn test_no_drifts_or_duplicates() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    File::create(path.join("file1.txt"))?.write_all(b"content1")?;
    File::create(path.join("file2.txt"))?.write_all(b"content2")?;

    let mut cmd = Command::cargo_bin("temporal-drift-scrut")?;
    cmd.arg(path.to_str().unwrap());

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("No exact duplicates found."))
        .stdout(predicate::str::contains("No same-name, different-content drifts found."));

    Ok(())
}

#[test]
fn test_exact_duplicates() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    File::create(path.join("fileA.txt"))?.write_all(b"duplicate_content")?;
    File::create(path.join("fileB.txt"))?.write_all(b"duplicate_content")?;
    fs::create_dir(path.join("subdir"))?;
    File::create(path.join("subdir/fileC.txt"))?.write_all(b"duplicate_content")?;

    let mut cmd = Command::cargo_bin("temporal-drift-scrut")?;
    cmd.arg(path.to_str().unwrap());

    let output = cmd.assert().success().stdout(predicate::str::is_empty().not()).get_output().stdout;
    let output_str = String::from_utf8_lossy(&output);

    assert!(output_str.contains("--- Exact Duplicates Detected ---"));
    assert!(output_str.contains("fileA.txt"));
    assert!(output_str.contains("fileB.txt"));
    assert!(output_str.contains("subdir/fileC.txt"));
    assert!(!output_str.contains("No exact duplicates found."));
    assert!(output_str.contains("No same-name, different-content drifts found."));

    Ok(())
}

#[test]
fn test_same_name_different_content() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    File::create(path.join("report.txt"))?.write_all(b"initial report content")?;
    fs::create_dir(path.join("archive"))?;
    File::create(path.join("archive/report.txt"))?.write_all(b"updated report content")?;
    File::create(path.join("archive/report.txt.old"))?.write_all(b"initial report content")?; // This is a duplicate of the first report.txt

    let mut cmd = Command::cargo_bin("temporal-drift-scrut")?;
    cmd.arg(path.to_str().unwrap());

    let output = cmd.assert().success().stdout(predicate::str::is_empty().not()).get_output().stdout;
    let output_str = String::from_utf8_lossy(&output);

    assert!(output_str.contains("--- Same Name, Different Content Detected ---"));
    assert!(output_str.contains("Filename: report.txt"));
    assert!(output_str.contains("report.txt (Hash:"));
    assert!(output_str.contains("archive/report.txt (Hash:"));
    assert!(!output_str.contains("No same-name, different-content drifts found."));

    // Also check for exact duplicates, as report.txt and archive/report.txt.old are duplicates
    assert!(output_str.contains("--- Exact Duplicates Detected ---"));
    assert!(output_str.contains("report.txt.old")); // The one in archive
    assert!(output_str.contains("report.txt")); // The one in root
    assert!(!output_str.contains("No exact duplicates found."));

    Ok(())
}

#[test]
fn test_mixed_drifts_and_duplicates() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Same name, different content
    File::create(path.join("config.ini"))?.write_all(b"version 1")?;
    fs::create_dir(path.join("backup"))?;
    File::create(path.join("backup/config.ini"))?.write_all(b"version 2")?;

    // Exact duplicates
    File::create(path.join("data.log"))?.write_all(b"log entry 1\nlog entry 2")?;
    File::create(path.join("copy_of_data.log"))?.write_all(b"log entry 1\nlog entry 2")?;

    // Unique file
    File::create(path.join("unique.txt"))?.write_all(b"unique content")?;

    let mut cmd = Command::cargo_bin("temporal-drift-scrut")?;
    cmd.arg(path.to_str().unwrap());

    let output = cmd.assert().success().stdout(predicate::str::is_empty().not()).get_output().stdout;
    let output_str = String::from_utf8_lossy(&output);

    // Check for same name, different content
    assert!(output_str.contains("--- Same Name, Different Content Detected ---"));
    assert!(output_str.contains("Filename: config.ini"));
    assert!(output_str.contains("config.ini (Hash:"));
    assert!(output_str.contains("backup/config.ini (Hash:"));

    // Check for exact duplicates
    assert!(output_str.contains("--- Exact Duplicates Detected ---"));
    assert!(output_str.contains("data.log"));
    assert!(output_str.contains("copy_of_data.log"));

    // Ensure unique file isn't reported as a drift
    assert!(!output_str.contains("unique.txt"));

    Ok(())
}

#[test]
fn test_invalid_path() -> Result<(), Box<dyn std::error::Error>> {
    let mut cmd = Command::cargo_bin("temporal-drift-scrut")?;
    cmd.arg("/non/existent/path/12345");

    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("Error: Provided path is not a directory"));

    Ok(())
}
