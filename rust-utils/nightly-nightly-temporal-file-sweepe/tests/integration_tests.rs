use std::process::Command;
use std::fs;
use std::path::{Path, PathBuf};
use tempfile::tempdir;
use filetime::{set_file_mtime, FileTime};
use chrono::{Utc, Duration};

// Helper to run the CLI tool
fn run_cli(args: &[&str]) -> String {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-temporal-file-sweeper"))
        .args(args)
        .output()
        .expect("Failed to execute command");
    String::from_utf8_lossy(&output.stdout).to_string()
}

// Helper to create a file with specific modification time
fn create_file_with_mtime(dir: &Path, filename: &str, mtime_offset_days: i64) -> PathBuf {
    let file_path = dir.join(filename);
    fs::write(&file_path, "test content").unwrap();
    let mtime = Utc::now() - Duration::days(mtime_offset_days);
    let file_time = FileTime::from_unix_timestamp(mtime.timestamp(), 0);
    set_file_mtime(&file_path, file_time).unwrap();
    file_path
}

#[test]
fn test_list_dry_run() {
    // Mock rationale: We create a temporary directory and files with controlled modification times
    // to simulate a real filesystem without affecting the actual system. This ensures deterministic
    // and offline testing of the utility's logic.
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    create_file_with_mtime(path, "old_file_1.txt", 60); // 60 days old
    create_file_with_mtime(path, "old_file_2.txt", 40); // 40 days old
    create_file_with_mtime(path, "new_file.txt", 10);  // 10 days old

    let output = run_cli(&[
        "-p", path.to_str().unwrap(),
        "-a", "30d", // Older than 30 days
        "--dry-run",
        "--verbose",
    ]);

    assert!(output.contains("Found 2 temporal dust bunnies:"));
    assert!(output.contains("old_file_1.txt"));
    assert!(output.contains("old_file_2.txt"));
    assert!(!output.contains("new_file.txt"));
    assert!(output.contains("Dry run complete. No changes were made."));

    // Verify files still exist
    assert!(path.join("old_file_1.txt").exists());
    assert!(path.join("old_file_2.txt").exists());
    assert!(path.join("new_file.txt").exists());
}

#[test]
fn test_move_action() {
    // Mock rationale: Similar to list_dry_run, temporary directories and files are used
    // to control the test environment and ensure isolation and determinism.
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();
    let archive_dir = tempdir().unwrap();
    let archive_path = archive_dir.path();

    let old_file_path = create_file_with_mtime(path, "old_to_move.txt", 60);
    let new_file_path = create_file_with_mtime(path, "new_not_to_move.txt", 10);

    let output = run_cli(&[
        "-p", path.to_str().unwrap(),
        "-a", "30d",
        "--action", "move",
        "--archive-dir", archive_path.to_str().unwrap(),
        "--verbose",
    ]);

    assert!(output.contains("Found 1 temporal dust bunny:"));
    assert!(output.contains("old_to_move.txt"));
    assert!(output.contains(&format!("Moving temporal dust bunnies to {:?}", archive_path)));
    assert!(output.contains(&format!("Moved {:?} to {:?}", old_file_path, archive_path.join("old_to_move.txt"))));

    // Verify old file is moved, new file remains
    assert!(!old_file_path.exists());
    assert!(archive_path.join("old_to_move.txt").exists());
    assert!(new_file_path.exists());
}

#[test]
fn test_delete_action() {
    // Mock rationale: Similar to previous tests, temporary directories and files are used
    // to control the test environment and ensure isolation and determinism.
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    let old_file_path = create_file_with_mtime(path, "old_to_delete.txt", 60);
    let new_file_path = create_file_with_mtime(path, "new_not_to_delete.txt", 10);

    let output = run_cli(&[
        "-p", path.to_str().unwrap(),
        "-a", "30d",
        "--action", "delete",
        "--verbose",
    ]);

    assert!(output.contains("Found 1 temporal dust bunny:"));
    assert!(output.contains("old_to_delete.txt"));
    assert!(output.contains("Deleting temporal dust bunnies..."));
    assert!(output.contains(&format!("Deleted {:?}", old_file_path)));

    // Verify old file is deleted, new file remains
    assert!(!old_file_path.exists());
    assert!(new_file_path.exists());
}

#[test]
fn test_recursive_scan() {
    // Mock rationale: Temporary directories and files are used to create a nested filesystem
    // structure for testing recursive scanning, ensuring isolation and determinism.
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();
    let sub_dir = path.join("sub_dir");
    fs::create_dir(&sub_dir).unwrap();

    create_file_with_mtime(path, "root_old.txt", 60);
    create_file_with_mtime(&sub_dir, "sub_old.txt", 70);
    create_file_with_mtime(path, "root_new.txt", 5);

    let output = run_cli(&[
        "-p", path.to_str().unwrap(),
        "-a", "30d",
        "-r", // Recursive
        "--dry-run",
        "--verbose",
    ]);

    assert!(output.contains("Found 2 temporal dust bunnies:"));
    assert!(output.contains("root_old.txt"));
    assert!(output.contains("sub_old.txt"));
    assert!(!output.contains("root_new.txt"));
}

#[test]
fn test_non_recursive_scan() {
    // Mock rationale: Temporary directories and files are used to create a nested filesystem
    // structure for testing non-recursive scanning, ensuring isolation and determinism.
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();
    let sub_dir = path.join("sub_dir");
    fs::create_dir(&sub_dir).unwrap();

    create_file_with_mtime(path, "root_old.txt", 60);
    create_file_with_mtime(&sub_dir, "sub_old.txt", 70);
    create_file_with_mtime(path, "root_new.txt", 5);

    let output = run_cli(&[
        "-p", path.to_str().unwrap(),
        "-a", "30d",
        // No -r flag
        "--dry-run",
        "--verbose",
    ]);

    assert!(output.contains("Found 1 temporal dust bunny:"));
    assert!(output.contains("root_old.txt"));
    assert!(!output.contains("sub_old.txt")); // Should not find this one
    assert!(!output.contains("root_new.txt"));
}

#[test]
fn test_invalid_path() {
    // Mock rationale: Testing with a non-existent path is an offline, deterministic check
    // of input validation.
    let output = run_cli(&[
        "-p", "/non/existent/path/12345",
        "-a", "1d",
        "--dry-run",
    ]);
    assert!(output.contains("Error: Scan path does not exist"));
}

#[test]
fn test_invalid_age_format() {
    // Mock rationale: Testing with invalid age strings is an offline, deterministic check
    // of input validation.
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    let output = run_cli(&[
        "-p", path.to_str().unwrap(),
        "-a", "30x", // Invalid unit
        "--dry-run",
    ]);
    assert!(output.contains("Invalid age unit. Use 'd' (days), 'w' (weeks), 'm' (months), or 'y' (years)."));

    let output_no_num = run_cli(&[
        "-p", path.to_str().unwrap(),
        "-a", "d", // No number
        "--dry-run",
    ]);
    assert!(output_no_num.contains("Invalid age number format"));
}
