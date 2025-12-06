use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;
use std::fs::{self, File};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};
use chrono::{Utc, Duration};

// Helper to create a file with a specific modification time
fn create_file_with_mtime(dir: &Path, filename: &str, days_ago: u64) -> PathBuf {
    let file_path = dir.join(filename);
    let mut file = File::create(&file_path).unwrap();
    writeln!(file, "test content").unwrap();

    // Set modification time
    let mtime = Utc::now() - Duration::days(days_ago as i64);
    let system_time = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(mtime.timestamp() as u64);
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(system_time)).unwrap();

    file_path
}

#[test]
fn test_dry_run_identifies_old_files() {
    // Mock rationale: Create a temporary directory and files with controlled timestamps
    // to simulate a file system state for deterministic testing.
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    // Create an old file (older than default 30 days)
    let old_file = create_file_with_mtime(path, "old_log.log", 35);
    // Create a recent file
    let recent_file = create_file_with_mtime(path, "recent_data.txt", 5);
    // Create another old file with a different extension
    let old_config = create_file_with_mtime(path, "old_config.conf", 40);

    let mut cmd = Command::cargo_bin("nightly-temporal-dust-sweeper").unwrap();
    cmd.arg("--path").arg(path)
       .arg("--dry-run")
       .assert()
       .success()
       .stdout(predicate::str::contains(old_file.to_string_lossy().as_ref()))
       .stdout(predicate::str::contains(old_config.to_string_lossy().as_ref()))
       .stdout(predicate::str::contains("Identified 2 pieces of temporal dust:"))
       .stdout(predicate::str::contains("This was a dry run. No files were swept."))
       .stdout(predicate::str::does_not_contain(recent_file.to_string_lossy().as_ref()));

    // Ensure files still exist after dry run
    assert!(old_file.exists());
    assert!(recent_file.exists());
    assert!(old_config.exists());
}

#[test]
fn test_sweep_deletes_old_files() {
    // Mock rationale: Create a temporary directory and files with controlled timestamps
    // to simulate a file system state for deterministic testing of deletion.
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    let old_file = create_file_with_mtime(path, "old_temp.tmp", 45);
    let recent_file = create_file_with_mtime(path, "current_project.rs", 10);

    let mut cmd = Command::cargo_bin("nightly-temporal-dust-sweeper").unwrap();
    cmd.arg("--path").arg(path)
       .arg("--sweep")
       .assert()
       .success()
       .stdout(predicate::str::contains(old_file.to_string_lossy().as_ref()))
       .stdout(predicate::str::contains("[SWEPT]"))
       .stdout(predicate::str::contains("Identified 1 pieces of temporal dust:"))
       .stdout(predicate::str::does_not_contain(recent_file.to_string_lossy().as_ref()));

    // Ensure old file is deleted and recent file still exists
    assert!(!old_file.exists());
    assert!(recent_file.exists());
}

#[test]
fn test_age_days_parameter() {
    // Mock rationale: Create files with specific ages to test the age_days filter.
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    let very_old_file = create_file_with_mtime(path, "v_old.txt", 60);
    let moderately_old_file = create_file_with_mtime(path, "m_old.txt", 20);
    let recent_file = create_file_with_mtime(path, "recent.txt", 5);

    // Test with age_days = 25 (should catch very_old and moderately_old)
    let mut cmd = Command::cargo_bin("nightly-temporal-dust-sweeper").unwrap();
    cmd.arg("--path").arg(path)
       .arg("--age-days").arg("25")
       .arg("--dry-run")
       .assert()
       .success()
       .stdout(predicate::str::contains(very_old_file.to_string_lossy().as_ref()))
       .stdout(predicate::str::contains(moderately_old_file.to_string_lossy().as_ref()))
       .stdout(predicate::str::contains("Identified 2 pieces of temporal dust:"))
       .stdout(predicate::str::does_not_contain(recent_file.to_string_lossy().as_ref()));

    // Test with age_days = 40 (should only catch very_old)
    let mut cmd2 = Command::cargo_bin("nightly-temporal-dust-sweeper").unwrap();
    cmd2.arg("--path").arg(path)
        .arg("--age-days").arg("40")
        .arg("--dry-run")
        .assert()
        .success()
        .stdout(predicate::str::contains(very_old_file.to_string_lossy().as_ref()))
        .stdout(predicate::str::contains("Identified 1 pieces of temporal dust:"))
        .stdout(predicate::str::does_not_contain(moderately_old_file.to_string_lossy().as_ref()))
        .stdout(predicate::str::does_not_contain(recent_file.to_string_lossy().as_ref()));
}

#[test]
fn test_extension_filter() {
    // Mock rationale: Create files with different extensions to test the extension filter.
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    let old_log = create_file_with_mtime(path, "old.log", 35);
    let old_txt = create_file_with_mtime(path, "old.txt", 35);
    let old_json = create_file_with_mtime(path, "old.json", 35);

    let mut cmd = Command::cargo_bin("nightly-temporal-dust-sweeper").unwrap();
    cmd.arg("--path").arg(path)
       .arg("--dry-run")
       .arg("--extension").arg("log")
       .assert()
       .success()
       .stdout(predicate::str::contains(old_log.to_string_lossy().as_ref()))
       .stdout(predicate::str::contains("Identified 1 pieces of temporal dust:"))
       .stdout(predicate::str::does_not_contain(old_txt.to_string_lossy().as_ref()))
       .stdout(predicate::str::does_not_contain(old_json.to_string_lossy().as_ref()));
}

#[test]
fn test_pattern_filter() {
    // Mock rationale: Create files with names matching/not matching a regex pattern.
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    let old_error_log = create_file_with_mtime(path, "error_2023.log", 35);
    let old_access_log = create_file_with_mtime(path, "access_2023.log", 35);
    let old_data_file = create_file_with_mtime(path, "data.txt", 35);

    let mut cmd = Command::cargo_bin("nightly-temporal-dust-sweeper").unwrap();
    cmd.arg("--path").arg(path)
       .arg("--dry-run")
       .arg("--pattern").arg("error_.*\\.log$")
       .assert()
       .success()
       .stdout(predicate::str::contains(old_error_log.to_string_lossy().as_ref()))
       .stdout(predicate::str::contains("Identified 1 pieces of temporal dust:"))
       .stdout(predicate::str::does_not_contain(old_access_log.to_string_lossy().as_ref()))
       .stdout(predicate::str::does_not_contain(old_data_file.to_string_lossy().as_ref()));
}

#[test]
fn test_no_dust_found() {
    // Mock rationale: Create a temporary directory with only recent files.
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    create_file_with_mtime(path, "recent_file_1.txt", 5);
    create_file_with_mtime(path, "recent_file_2.log", 10);

    let mut cmd = Command::cargo_bin("nightly-temporal-dust-sweeper").unwrap();
    cmd.arg("--path").arg(path)
       .arg("--dry-run")
       .assert()
       .success()
       .stdout(predicate::str::contains("No temporal dust found in"))
       .stdout(predicate::str::contains("The wasteland is clean!"));
}

#[test]
fn test_sweep_and_dry_run_conflict() {
    let mut cmd = Command::cargo_bin("nightly-temporal-dust-sweeper").unwrap();
    cmd.arg("--sweep")
       .arg("--dry-run")
       .assert()
       .failure()
       .stderr(predicate::str::contains("Error: Cannot use --sweep and --dry-run simultaneously. Choose one."));
}
