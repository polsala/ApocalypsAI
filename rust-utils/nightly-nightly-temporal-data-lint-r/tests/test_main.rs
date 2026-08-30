use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;
use std::fs::{self, File};
use std::io::Write;
use std::time::SystemTime;
use filetime::{set_file_mtime, FileTime};

// Mock rationale: We use tempfile to create an isolated, temporary directory
// and programmatically create files within it with specific modification times.
// This allows for deterministic testing of the utility's logic without
// affecting the actual filesystem or relying on external resources.
// `filetime` crate is used to precisely control file modification times.

#[test]
fn test_dry_run_identifies_old_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a file older than 30 days
    let old_file_path = path.join("old_log.txt");
    File::create(&old_file_path)?.write_all(b"old data")?;
    let thirty_days_ago = SystemTime::now() - std::time::Duration::from_secs(30 * 24 * 3600 + 100);
    set_file_mtime(&old_file_path, FileTime::from_system_time(thirty_days_ago))?;

    // Create a file newer than 30 days
    let new_file_path = path.join("new_report.txt");
    File::create(&new_file_path)?.write_all(b"new data")?;
    let ten_days_ago = SystemTime::now() - std::time::Duration::from_secs(10 * 24 * 3600);
    set_file_mtime(&new_file_path, FileTime::from_system_time(ten_days_ago))?;

    let mut cmd = Command::cargo_bin("nightly-temporal-data-lint-roller")?;
    cmd.arg("--path").arg(path)
       .arg("--age").arg("30d")
       .arg("--dry-run"); // Explicitly dry-run, though it's default

    cmd.assert()
        .success()
        .stdout(predicate::str::contains(format!("Lint found: {}", old_file_path.display())))
        .stdout(predicate::str::contains("Total temporal lint identified: 1"))
        .stdout(predicate::str::contains("Run with --delete to remove these files."))
        .stdout(predicate::str::does_not_contain(format!("{}", new_file_path.display())));

    assert!(old_file_path.exists()); // Should still exist in dry run
    assert!(new_file_path.exists());

    Ok(())
}

#[test]
fn test_delete_removes_old_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a file older than 30 days
    let old_file_path = path.join("old_cache.tmp");
    File::create(&old_file_path)?.write_all(b"cache data")?;
    let thirty_days_ago = SystemTime::now() - std::time::Duration::from_secs(30 * 24 * 3600 + 100);
    set_file_mtime(&old_file_path, FileTime::from_system_time(thirty_days_ago))?;

    // Create a file newer than 30 days
    let new_file_path = path.join("current_data.json");
    File::create(&new_file_path)?.write_all(b"{}")?;
    let ten_days_ago = SystemTime::now() - std::time::Duration::from_secs(10 * 24 * 3600);
    set_file_mtime(&new_file_path, FileTime::from_system_time(ten_days_ago))?;

    let mut cmd = Command::cargo_bin("nightly-temporal-data-lint-roller")?;
    cmd.arg("--path").arg(path)
       .arg("--age").arg("30d")
       .arg("--delete");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains(format!("Lint found: {}", old_file_path.display())))
        .stdout(predicate::str::contains("-> DELETED"))
        .stdout(predicate::str::contains("Total temporal lint identified: 1"))
        .stdout(predicate::str::contains("Total temporal lint deleted: 1"))
        .stdout(predicate::str::does_not_contain(format!("{}", new_file_path.display())));

    assert!(!old_file_path.exists()); // Should be deleted
    assert!(new_file_path.exists()); // Should still exist

    Ok(())
}

#[test]
fn test_no_files_match_criteria() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a file newer than 30 days
    let new_file_path = path.join("recent_file.txt");
    File::create(&new_file_path)?.write_all(b"recent data")?;
    let five_days_ago = SystemTime::now() - std::time::Duration::from_secs(5 * 24 * 3600);
    set_file_mtime(&new_file_path, FileTime::from_system_time(five_days_ago))?;

    let mut cmd = Command::cargo_bin("nightly-temporal-data-lint-roller")?;
    cmd.arg("--path").arg(path)
       .arg("--age").arg("30d")
       .arg("--dry-run");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Total temporal lint identified: 0"))
        .stdout(predicate::str::does_not_contain("Lint found:"));

    assert!(new_file_path.exists());

    Ok(())
}

#[test]
fn test_invalid_age_format() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let mut cmd = Command::cargo_bin("nightly-temporal-data-lint-roller")?;
    cmd.arg("--path").arg(path)
       .arg("--age").arg("30months"); // Invalid format

    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("Invalid duration format. Use '30d', '1w', '1y' etc."));

    Ok(())
}
