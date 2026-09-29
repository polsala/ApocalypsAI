use assert_cmd::Command;
use predicates::prelude::*;
use std::fs;
use std::io::Write;
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use tempfile::tempdir;

// Mock rationale: These tests create temporary directories and files with specific timestamps
// to simulate different scenarios (old files, new files, non-existent paths). This allows
// deterministic testing of file system interactions without relying on actual system state
// or external services. `tempfile` ensures isolation, and `assert_cmd` allows robust CLI testing.

#[test]
fn test_help_message() {
    let mut cmd = Command::cargo_bin("nightly-ephemeral-data-janitor").unwrap();
    cmd.arg("--help").assert().success().stdout(predicate::str::contains("A whimsical Rust CLI tool to sweep away ephemeral files"));
}

#[test]
fn test_version_message() {
    let mut cmd = Command::cargo_bin("nightly-ephemeral-data-janitor").unwrap();
    cmd.arg("--version").assert().success().stdout(predicate::str::contains("nightly-ephemeral-data-janitor 0.1.0"));
}

#[test]
fn test_dry_run_identifies_old_files() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    // Create an old file (e.g., 10 days old)
    let old_file_path = path.join("old_log.txt");
    fs::File::create(&old_file_path).unwrap().write_all(b"old data").unwrap();
    let ten_days_ago = SystemTime::now() - Duration::from_secs(10 * 24 * 60 * 60);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(ten_days_ago)).unwrap();

    // Create a new file (e.g., 1 hour old)
    let new_file_path = path.join("new_report.txt");
    fs::File::create(&new_file_path).unwrap().write_all(b"new data").unwrap();
    let one_hour_ago = SystemTime::now() - Duration::from_secs(60 * 60);
    filetime::set_file_mtime(&new_file_path, filetime::FileTime::from_system_time(one_hour_ago)).unwrap();

    let mut cmd = Command::cargo_bin("nightly-ephemeral-data-janitor").unwrap();
    cmd.args(["--dry-run", "--age", "7d", path.to_str().unwrap()])
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("Would sweep: {}", old_file_path.display())))
        .stdout(predicate::str::contains("Dry run complete! 1 digital dust bunnies"))
        .stdout(predicate::str::does_not_contain(format!("Would sweep: {}", new_file_path.display())));

    assert!(old_file_path.exists()); // Should still exist in dry run
    assert!(new_file_path.exists());
}

#[test]
fn test_deletes_old_files() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    // Create an old file (e.g., 10 days old)
    let old_file_path = path.join("ancient_cache.tmp");
    fs::File::create(&old_file_path).unwrap().write_all(b"ancient data").unwrap();
    let ten_days_ago = SystemTime::now() - Duration::from_secs(10 * 24 * 60 * 60);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(ten_days_ago)).unwrap();

    // Create a new file (e.g., 1 hour old)
    let new_file_path = path.join("current_session.log");
    fs::File::create(&new_file_path).unwrap().write_all(b"current data").unwrap();
    let one_hour_ago = SystemTime::now() - Duration::from_secs(60 * 60);
    filetime::set_file_mtime(&new_file_path, filetime::FileTime::from_system_time(one_hour_ago)).unwrap();

    let mut cmd = Command::cargo_bin("nightly-ephemeral-data-janitor").unwrap();
    cmd.args(["--age", "7d", path.to_str().unwrap()])
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("Swept away: {}", old_file_path.display())))
        .stdout(predicate::str::contains("Janitor duty complete! Swept away 1 digital dust bunnies"))
        .stdout(predicate::str::does_not_contain(format!("Swept away: {}", new_file_path.display())));

    assert!(!old_file_path.exists()); // Old file should be deleted
    assert!(new_file_path.exists()); // New file should remain
}

#[test]
fn test_no_files_to_delete() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    // Create a new file (e.g., 1 hour old)
    let new_file_path = path.join("fresh_data.txt");
    fs::File::create(&new_file_path).unwrap().write_all(b"fresh data").unwrap();
    let one_hour_ago = SystemTime::now() - Duration::from_secs(60 * 60);
    filetime::set_file_mtime(&new_file_path, filetime::FileTime::from_system_time(one_hour_ago)).unwrap();

    let mut cmd = Command::cargo_bin("nightly-ephemeral-data-janitor").unwrap();
    cmd.args(["--age", "7d", path.to_str().unwrap()])
        .assert()
        .success()
        .stdout(predicate::str::contains("All clear! No ancient digital echoes or dust bunnies found."));

    assert!(new_file_path.exists());
}

#[test]
fn test_non_existent_path() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();
    let non_existent_path = path.join("non_existent_dir");

    let mut cmd = Command::cargo_bin("nightly-ephemeral-data-janitor").unwrap();
    cmd.args(["--age", "1d", non_existent_path.to_str().unwrap()])
        .assert()
        .success() // It should still exit successfully, just print a warning
        .stderr(predicate::str::contains(format!("Path does not exist: {}. Skipping.", non_existent_path.display())));
}

#[test]
fn test_recursive_deletion() {
    let temp_dir = tempdir().unwrap();
    let root_path = temp_dir.path();

    let sub_dir = root_path.join("sub_dir");
    fs::create_dir(&sub_dir).unwrap();

    let old_file_root = root_path.join("old_root.txt");
    fs::File::create(&old_file_root).unwrap().write_all(b"root old").unwrap();
    let ten_days_ago = SystemTime::now() - Duration::from_secs(10 * 24 * 60 * 60);
    filetime::set_file_mtime(&old_file_root, filetime::FileTime::from_system_time(ten_days_ago)).unwrap();

    let old_file_sub = sub_dir.join("old_sub.txt");
    fs::File::create(&old_file_sub).unwrap().write_all(b"sub old").unwrap();
    filetime::set_file_mtime(&old_file_sub, filetime::FileTime::from_system_time(ten_days_ago)).unwrap();

    let new_file_root = root_path.join("new_root.txt");
    fs::File::create(&new_file_root).unwrap().write_all(b"root new").unwrap();

    let mut cmd = Command::cargo_bin("nightly-ephemeral-data-janitor").unwrap();
    cmd.args(["--age", "7d", root_path.to_str().unwrap()])
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("Swept away: {}", old_file_root.display())))
        .stdout(predicate::str::contains(format!("Swept away: {}", old_file_sub.display())))
        .stdout(predicate::str::contains("Janitor duty complete! Swept away 2 digital dust bunnies"));

    assert!(!old_file_root.exists());
    assert!(!old_file_sub.exists());
    assert!(new_file_root.exists());
}

#[test]
fn test_verbose_output() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    let old_file_path = path.join("old_verbose.txt");
    fs::File::create(&old_file_path).unwrap().write_all(b"old data").unwrap();
    let ten_days_ago = SystemTime::now() - Duration::from_secs(10 * 24 * 60 * 60);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(ten_days_ago)).unwrap();

    let new_file_path = path.join("new_verbose.txt");
    fs::File::create(&new_file_path).unwrap().write_all(b"new data").unwrap();
    let one_hour_ago = SystemTime::now() - Duration::from_secs(60 * 60);
    filetime::set_file_mtime(&new_file_path, filetime::FileTime::from_system_time(one_hour_ago)).unwrap();

    let mut cmd = Command::cargo_bin("nightly-ephemeral-data-janitor").unwrap();
    cmd.args(["--dry-run", "--verbose", "--age", "7d", path.to_str().unwrap()])
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("Would sweep: {}", old_file_path.display())))
        .stdout(predicate::str::contains(format!("Keeping: {}", new_file_path.display())))
        .stdout(predicate::str::contains("Scanning:"));
}

#[test]
fn test_age_parsing_hours() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    let old_file_path = path.join("old_hours.txt");
    fs::File::create(&old_file_path).unwrap().write_all(b"old data").unwrap();
    let three_hours_ago = SystemTime::now() - Duration::from_secs(3 * 60 * 60);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(three_hours_ago)).unwrap();

    let new_file_path = path.join("new_hours.txt");
    fs::File::create(&new_file_path).unwrap().write_all(b"new data").unwrap();
    let one_hour_ago = SystemTime::now() - Duration::from_secs(1 * 60 * 60);
    filetime::set_file_mtime(&new_file_path, filetime::FileTime::from_system_time(one_hour_ago)).unwrap();

    let mut cmd = Command::cargo_bin("nightly-ephemeral-data-janitor").unwrap();
    cmd.args(["--dry-run", "--age", "2h", path.to_str().unwrap()])
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("Would sweep: {}", old_file_path.display())))
        .stdout(predicate::str::does_not_contain(format!("Would sweep: {}", new_file_path.display())));
}

#[test]
fn test_age_parsing_minutes() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    let old_file_path = path.join("old_minutes.txt");
    fs::File::create(&old_file_path).unwrap().write_all(b"old data").unwrap();
    let three_minutes_ago = SystemTime::now() - Duration::from_secs(3 * 60);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(three_minutes_ago)).unwrap();

    let new_file_path = path.join("new_minutes.txt");
    fs::File::create(&new_file_path).unwrap().write_all(b"new data").unwrap();
    let one_minute_ago = SystemTime::now() - Duration::from_secs(1 * 60);
    filetime::set_file_mtime(&new_file_path, filetime::FileTime::from_system_time(one_minute_ago)).unwrap();

    let mut cmd = Command::cargo_bin("nightly-ephemeral-data-janitor").unwrap();
    cmd.args(["--dry-run", "--age", "2m", path.to_str().unwrap()])
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("Would sweep: {}", old_file_path.display())))
        .stdout(predicate::str::does_not_contain(format!("Would sweep: {}", new_file_path.display())));
}
