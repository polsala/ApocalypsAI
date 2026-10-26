use assert_cmd::Command;
use predicates::prelude::*;
use std::fs;
use std::io::Write;
use std::time::{SystemTime, Duration};
use tempfile::NamedTempFile;
use filetime::{set_file_mtime, FileTime};

// Mock rationale: We use `tempfile` to create temporary files and `filetime` to deterministically set their modification timestamps.
// This allows us to control the inputs (content and mtime) precisely for reproducible tests without relying on actual system time changes or external resources.

#[test]
fn test_same_content_same_mtime_produces_same_hash() -> Result<(), Box<dyn std::error::Error>> {
    let mut file = NamedTempFile::new()?;
    let content = b"Hello, Chrono-World!";
    file.write_all(content)?;
    file.flush()?;

    let path = file.path();
    let fixed_mtime = FileTime::from_system_time(SystemTime::UNIX_EPOCH + Duration::from_secs(1234567890));
    set_file_mtime(path, fixed_mtime)?;

    let output1 = Command::cargo_bin("nightly-chrono-hash")?
        .arg(path)
        .output()?;
    assert!(output1.status.success());
    let hash1 = String::from_utf8(output1.stdout)?.trim().to_string();

    // Run again with the exact same file and mtime
    let output2 = Command::cargo_bin("nightly-chrono-hash")?
        .arg(path)
        .output()?;
    assert!(output2.status.success());
    let hash2 = String::from_utf8(output2.stdout)?.trim().to_string();

    assert_eq!(hash1, hash2);
    assert!(!hash1.is_empty());

    Ok(())
}

#[test]
fn test_same_content_different_mtime_produces_different_hash() -> Result<(), Box<dyn std::error::Error>> {
    let mut file = NamedTempFile::new()?;
    let content = b"Temporal Anomaly Detected!";
    file.write_all(content)?;
    file.flush()?;

    let path = file.path();

    // First mtime
    let mtime1 = FileTime::from_system_time(SystemTime::UNIX_EPOCH + Duration::from_secs(1000));
    set_file_mtime(path, mtime1)?;
    let output1 = Command::cargo_bin("nightly-chrono-hash")?
        .arg(path)
        .output()?;
    assert!(output1.status.success());
    let hash1 = String::from_utf8(output1.stdout)?.trim().to_string();

    // Second mtime (different)
    let mtime2 = FileTime::from_system_time(SystemTime::UNIX_EPOCH + Duration::from_secs(2000));
    set_file_mtime(path, mtime2)?;
    let output2 = Command::cargo_bin("nightly-chrono-hash")?
        .arg(path)
        .output()?;
    assert!(output2.status.success());
    let hash2 = String::from_utf8(output2.stdout)?.trim().to_string();

    assert_ne!(hash1, hash2);
    assert!(!hash1.is_empty());
    assert!(!hash2.is_empty());

    Ok(())
}

#[test]
fn test_different_content_same_mtime_produces_different_hash() -> Result<(), Box<dyn std::error::Error>> {
    let mut file1 = NamedTempFile::new()?;
    let content1 = b"First version of the manifest.";
    file1.write_all(content1)?;
    file1.flush()?;

    let mut file2 = NamedTempFile::new()?;
    let content2 = b"Second version of the manifest.";
    file2.write_all(content2)?;
    file2.flush()?;

    let path1 = file1.path();
    let path2 = file2.path();

    let fixed_mtime = FileTime::from_system_time(SystemTime::UNIX_EPOCH + Duration::from_secs(3000));
    set_file_mtime(path1, fixed_mtime)?;
    set_file_mtime(path2, fixed_mtime)?;

    let output1 = Command::cargo_bin("nightly-chrono-hash")?
        .arg(path1)
        .output()?;
    assert!(output1.status.success());
    let hash1 = String::from_utf8(output1.stdout)?.trim().to_string();

    let output2 = Command::cargo_bin("nightly-chrono-hash")?
        .arg(path2)
        .output()?;
    assert!(output2.status.success());
    let hash2 = String::from_utf8(output2.stdout)?.trim().to_string();

    assert_ne!(hash1, hash2);
    assert!(!hash1.is_empty());
    assert!(!hash2.is_empty());

    Ok(())
}

#[test]
fn test_empty_file() -> Result<(), Box<dyn std::error::Error>> {
    let mut file = NamedTempFile::new()?;
    file.flush()?;

    let path = file.path();
    let fixed_mtime = FileTime::from_system_time(SystemTime::UNIX_EPOCH + Duration::from_secs(4000));
    set_file_mtime(path, fixed_mtime)?;

    let output = Command::cargo_bin("nightly-chrono-hash")?
        .arg(path)
        .output()?;
    assert!(output.status.success());
    let hash = String::from_utf8(output.stdout)?.trim().to_string();

    assert!(!hash.is_empty());
    Ok(())
}

#[test]
fn test_file_not_found() -> Result<(), Box<dyn std::error::Error>> {
    let non_existent_path = "/tmp/non_existent_file_12345.txt"; // Should not exist

    let output = Command::cargo_bin("nightly-chrono-hash")?
        .arg(non_existent_path)
        .output()?;

    assert!(!output.status.success());
    assert!(output.stderr.starts_with(b"Error: File not found:"));

    Ok(())
}

#[test]
fn test_path_is_directory() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempfile::tempdir()?;
    let dir_path = temp_dir.path();

    let output = Command::cargo_bin("nightly-chrono-hash")?
        .arg(dir_path)
        .output()?;

    assert!(!output.status.success());
    assert!(output.stderr.starts_with(b"Error: Path is not a file:"));

    Ok(())
}
