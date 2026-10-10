use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;
use std::fs::{self, File};
use std::io::Write;
use std::time::{Duration, SystemTime};

// Mock rationale: We create a temporary directory and files with specific timestamps
// to simulate a filesystem state. This allows deterministic testing without
// interacting with the actual filesystem or external services.

#[test]
fn test_help_message() {
    let mut cmd = Command::cargo_bin("nightly-digital-echo-scrubber").unwrap();
    cmd.arg("--help").assert().success().stdout(predicate::str::contains("Usage: nightly-digital-echo-scrubber"));
}

#[test]
fn test_version_message() {
    let mut cmd = Command::cargo_bin("nightly-digital-echo-scrubber").unwrap();
    cmd.arg("--version").assert().success().stdout(predicate::str::contains("nightly-digital-echo-scrubber 0.1.0"));
}

#[test]
fn test_dry_run_finds_old_files() {
    let dir = tempdir().unwrap();
    let path = dir.path();

    // Create an old file (older than default 30 days)
    let old_file_path = path.join("old_echo.txt");
    File::create(&old_file_path).unwrap().write_all(b"old data").unwrap();
    // Set modified time to 60 days ago
    let sixty_days_ago = SystemTime::now() - Duration::from_secs(60 * 24 * 60 * 60);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(sixty_days_ago)).unwrap();

    // Create a recent file (newer than default 30 days)
    let recent_file_path = path.join("recent_data.txt");
    File::create(&recent_file_path).unwrap().write_all(b"recent data").unwrap();
    // Modified time is now, which is recent enough

    let mut cmd = Command::cargo_bin("nightly-digital-echo-scrubber").unwrap();
    cmd.arg(path)
        .arg("--dry-run")
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("Found echo: '{}'", old_file_path.display())))
        .stdout(predicate::str::contains("(Dry run mode: no files will be deleted.)"))
        .stdout(predicate::str::contains("Total digital echoes found: 1"))
        .stdout(predicate::str::contains("(In dry run mode, 1 echoes would have been scrubbed.)"))
        .stderr(predicate::str::is_empty());

    // Assert that the old file still exists after dry run
    assert!(old_file_path.exists());
    assert!(recent_file_path.exists());
}

#[test]
fn test_live_run_deletes_old_files() {
    let dir = tempdir().unwrap();
    let path = dir.path();

    // Create an old file (older than default 30 days)
    let old_file_path = path.join("old_echo_to_delete.txt");
    File::create(&old_file_path).unwrap().write_all(b"old data").unwrap();
    let sixty_days_ago = SystemTime::now() - Duration::from_secs(60 * 24 * 60 * 60);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(sixty_days_ago)).unwrap();

    // Create a recent file
    let recent_file_path = path.join("recent_data_to_keep.txt");
    File::create(&recent_file_path).unwrap().write_all(b"recent data").unwrap();

    let mut cmd = Command::cargo_bin("nightly-digital-echo-scrubber").unwrap();
    cmd.arg(path)
        .timeout(Duration::from_secs(10)) // Give it time for the 5-sec delay
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("Found echo: '{}'", old_file_path.display())))
        .stdout(predicate::str::contains("-> Scrubbed!"))
        .stdout(predicate::str::contains("Total digital echoes found: 1"))
        .stdout(predicate::str::contains("Total digital echoes scrubbed: 1"))
        .stderr(predicate::str::is_empty());

    // Assert that the old file is deleted
    assert!(!old_file_path.exists());
    // Assert that the recent file still exists
    assert!(recent_file_path.exists());
}

#[test]
fn test_custom_age_threshold() {
    let dir = tempdir().unwrap();
    let path = dir.path();

    // File 1: 10 days old (should NOT be scrubbed with --age 5, as 10 days ago is older than 5 days ago)
    let file_10_days_old = path.join("file_10_days.txt");
    File::create(&file_10_days_old).unwrap().write_all(b"data").unwrap();
    let ten_days_ago = SystemTime::now() - Duration::from_secs(10 * 24 * 60 * 60);
    filetime::set_file_mtime(&file_10_days_old, filetime::FileTime::from_system_time(ten_days_ago)).unwrap();

    // File 2: 2 days old (should NOT be scrubbed with --age 5, as 2 days ago is NOT older than 5 days ago)
    let file_2_days_old = path.join("file_2_days.txt");
    File::create(&file_2_days_old).unwrap().write_all(b"data").unwrap();
    let two_days_ago = SystemTime::now() - Duration::from_secs(2 * 24 * 60 * 60);
    filetime::set_file_mtime(&file_2_days_old, filetime::FileTime::from_system_time(two_days_ago)).unwrap();

    // File 3: 6 days old (should be scrubbed with --age 5)
    let file_6_days_old = path.join("file_6_days.txt");
    File::create(&file_6_days_old).unwrap().write_all(b"data").unwrap();
    let six_days_ago = SystemTime::now() - Duration::from_secs(6 * 24 * 60 * 60);
    filetime::set_file_mtime(&file_6_days_old, filetime::FileTime::from_system_time(six_days_ago)).unwrap();

    let mut cmd = Command::cargo_bin("nightly-digital-echo-scrubber").unwrap();
    cmd.arg(path)
        .arg("--age")
        .arg("5") // Set age threshold to 5 days
        .arg("--dry-run")
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("Found echo: '{}'", file_10_days_old.display())))
        .stdout(predicate::str::contains(format!("Found echo: '{}'", file_2_days_old.display())).not())
        .stdout(predicate::str::contains(format!("Found echo: '{}'", file_6_days_old.display())))
        .stdout(predicate::str::contains("Total digital echoes found: 2"))
        .stderr(predicate::str::is_empty());

    assert!(file_10_days_old.exists());
    assert!(file_2_days_old.exists());
    assert!(file_6_days_old.exists()); // Still exists due to dry-run
}

#[test]
fn test_non_existent_path() {
    let mut cmd = Command::cargo_bin("nightly-digital-echo-scrubber").unwrap();
    cmd.arg("/non/existent/path/to/nowhere")
        .assert()
        .failure()
        .stderr(predicate::str::contains("Error: Path '/non/existent/path/to/nowhere' does not exist."));
}

#[test]
fn test_path_is_file_not_dir() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("a_file.txt");
    File::create(&file_path).unwrap().write_all(b"content").unwrap();

    let mut cmd = Command::cargo_bin("nightly-digital-echo-scrubber").unwrap();
    cmd.arg(&file_path)
        .assert()
        .failure()
        .stderr(predicate::str::contains(format!("Error: Path '{}' is not a directory.", file_path.display())));
}
