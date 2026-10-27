use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;
use std::fs::{self, File};
use std::io::Write;
use std::time::SystemTime;
use filetime::{FileTime, set_file_times};
use chrono::{Utc, Duration};

// Mock rationale: Tests create temporary directories and files with specific, controlled timestamps
// using `tempfile` and `filetime`. This ensures deterministic and isolated testing of the file
// scanning and deletion logic without relying on the actual system's file state or external services.

#[test]
fn test_dry_run_older_than() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a file older than 10 days
    let old_file_path = path.join("old_echo.txt");
    File::create(&old_file_path)?.write_all(b"old data")?;
    let ten_days_ago_sys = SystemTime::now() - std::time::Duration::from_secs(Duration::days(10).num_seconds() as u64);
    let ft = FileTime::from_system_time(ten_days_ago_sys);
    set_file_times(&old_file_path, ft, ft)?;

    // Create a recent file
    let recent_file_path = path.join("recent_data.txt");
    File::create(&recent_file_path)?.write_all(b"recent data")?;
    // Default timestamp is recent, no need to set explicitly

    Command::cargo_bin("nightly-chronal-cleaner")?
        .arg("--path")
        .arg(path.to_str().unwrap())
        .arg("--older-than")
        .arg("5") // Should detect files older than 5 days
        .arg("--dry-run") // Default, but explicit
        .assert()
        .success()
        .stdout(predicate::str::contains("Temporal echoes detected (1 files):"))
        .stdout(predicate::str::contains(old_file_path.to_str().unwrap()))
        .stdout(predicate::str::contains("This was a dry run. No files were deleted."));

    assert!(old_file_path.exists()); // Should still exist after dry run
    assert!(recent_file_path.exists());

    Ok(())
}

#[test]
fn test_delete_older_than() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a file older than 10 days
    let old_file_path = path.join("old_echo_to_delete.txt");
    File::create(&old_file_path)?.write_all(b"old data")?;
    let ten_days_ago_sys = SystemTime::now() - std::time::Duration::from_secs(Duration::days(10).num_seconds() as u64);
    let ft = FileTime::from_system_time(ten_days_ago_sys);
    set_file_times(&old_file_path, ft, ft)?;

    // Create a recent file
    let recent_file_path = path.join("recent_data_to_keep.txt");
    File::create(&recent_file_path)?.write_all(b"recent data")?;

    let mut cmd = Command::cargo_bin("nightly-chronal-cleaner")?;
    cmd.arg("--path")
        .arg(path.to_str().unwrap())
        .arg("--older-than")
        .arg("5")
        .arg("--delete")
        .write_stdin("y\n") // Confirm deletion
        .assert()
        .success()
        .stdout(predicate::str::contains("Temporal echoes detected (1 files):"))
        .stdout(predicate::str::contains(old_file_path.to_str().unwrap()))
        .stdout(predicate::str::contains("Successfully purged 1 temporal echoes."));

    assert!(!old_file_path.exists()); // Should be deleted
    assert!(recent_file_path.exists()); // Should still exist

    Ok(())
}

#[test]
fn test_not_accessed_in() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a file not accessed in 10 days
    let unaccessed_file_path = path.join("unaccessed_echo.txt");
    File::create(&unaccessed_file_path)?.write_all(b"unaccessed data")?;
    let ten_days_ago_sys = SystemTime::now() - std::time::Duration::from_secs(Duration::days(10).num_seconds() as u64);
    let ft_access = FileTime::from_system_time(ten_days_ago_sys);
    let ft_modify = FileTime::from_system_time(SystemTime::now()); // Keep modification recent
    set_file_times(&unaccessed_file_path, ft_access, ft_modify)?;

    // Create a recently accessed file
    let recently_accessed_file_path = path.join("recently_accessed.txt");
    File::create(&recently_accessed_file_path)?.write_all(b"recent access")?;
    // Default access time is recent

    Command::cargo_bin("nightly-chronal-cleaner")?
        .arg("--path")
        .arg(path.to_str().unwrap())
        .arg("--not-accessed-in")
        .arg("5") // Should detect files not accessed in 5 days
        .assert()
        .success()
        .stdout(predicate::str::contains("Temporal echoes detected (1 files):"))
        .stdout(predicate::str::contains(unaccessed_file_path.to_str().unwrap()))
        .stdout(predicate::str::contains("This was a dry run. No files were deleted."));

    assert!(unaccessed_file_path.exists());
    assert!(recently_accessed_file_path.exists());

    Ok(())
}

#[test]
fn test_no_echoes() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a recent file
    let recent_file_path = path.join("recent_data.txt");
    File::create(&recent_file_path)?.write_all(b"recent data")?;

    Command::cargo_bin("nightly-chronal-cleaner")?
        .arg("--path")
        .arg(path.to_str().unwrap())
        .arg("--older-than")
        .arg("5")
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("No temporal echoes detected in '{}'. Your filesystem is stable.", path.display())))
        .stdout(predicate::str::contains("No files were deleted.").not()); // Ensure it doesn't say "no files were deleted" if nothing was found

    assert!(recent_file_path.exists());

    Ok(())
}

#[test]
fn test_delete_confirmation_no() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let old_file_path = path.join("old_echo_not_deleted.txt");
    File::create(&old_file_path)?.write_all(b"old data")?;
    let ten_days_ago_sys = SystemTime::now() - std::time::Duration::from_secs(Duration::days(10).num_seconds() as u64);
    let ft = FileTime::from_system_time(ten_days_ago_sys);
    set_file_times(&old_file_path, ft, ft)?;

    let mut cmd = Command::cargo_bin("nightly-chronal-cleaner")?;
    cmd.arg("--path")
        .arg(path.to_str().unwrap())
        .arg("--older-than")
        .arg("5")
        .arg("--delete")
        .write_stdin("n\n") // Decline deletion
        .assert()
        .success()
        .stdout(predicate::str::contains("Purge aborted. Temporal echoes remain."));

    assert!(old_file_path.exists()); // Should still exist

    Ok(())
}

#[test]
fn test_delete_without_criteria_fails() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    Command::cargo_bin("nightly-chronal-cleaner")?
        .arg("--path")
        .arg(path.to_str().unwrap())
        .arg("--delete")
        .assert()
        .failure()
        .stderr(predicate::str::contains("Error: --delete requires either --older-than or --not-accessed-in to be specified."));

    Ok(())
}

#[test]
fn test_dry_run_and_delete_fails() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    Command::cargo_bin("nightly-chronal-cleaner")?
        .arg("--path")
        .arg(path.to_str().unwrap())
        .arg("--older-than")
        .arg("5")
        .arg("--dry-run")
        .arg("--delete")
        .assert()
        .failure()
        .stderr(predicate::str::contains("Error: Cannot use --delete with --dry-run. Please choose one."));

    Ok(())
}
