use std::process::Command;
use std::fs::{self, File};
use std::io::Write;
use std::path::{Path, PathBuf};
use tempfile::tempdir;
use chrono::{Utc, Duration, TimeZone};

// Helper function to create a file with content and specific modification time
fn create_test_file(dir: &Path, name: &str, content: &str, modified_ago: Duration) -> PathBuf {
    let file_path = dir.join(name);
    let mut file = File::create(&file_path).expect("Failed to create test file");
    file.write_all(content.as_bytes()).expect("Failed to write to test file");
    file.sync_all().expect("Failed to sync file");

    // Mock rationale: Setting file modification times directly is deterministic and offline.
    // This simulates different file ages without relying on actual system time changes during test execution.
    let past_time = Utc::now() - modified_ago;
    let system_time = std::time::SystemTime::from(past_time);
    file_path.set_mtime(system_time).expect("Failed to set modification time");
    file_path
}

// Helper function to run the void-scout command
fn run_void_scout(args: &[&str], cwd: &Path) -> String {
    let output = Command::new(env!("CARGO_BIN_EXE_void-scout"))
        .current_dir(cwd)
        .args(args)
        .output()
        .expect("Failed to execute void-scout");

    assert!(output.status.success(), "Command failed: {:?}\nStderr: {}", output.status, String::from_utf8_lossy(&output.stderr));
    String::from_utf8_lossy(&output.stdout).to_string()
}

#[test]
fn test_basic_file_search() {
    let dir = tempdir().expect("Failed to create temp dir");
    create_test_file(dir.path(), "test_file.txt", "hello", Duration::days(10));
    create_test_file(dir.path(), "another.log", "world", Duration::days(5));

    let output = run_void_scout(&[".", "--name", "test_file"], dir.path());
    assert!(output.contains("test_file.txt"));
    assert!(!output.contains("another.log"));

    let output = run_void_scout(&[".", "--name", "\.log$"], dir.path());
    assert!(!output.contains("test_file.txt"));
    assert!(output.contains("another.log"));
}

#[test]
fn test_size_filtering() {
    let dir = tempdir().expect("Failed to create temp dir");
    create_test_file(dir.path(), "small.txt", "a", Duration::days(1)); // 1 byte
    create_test_file(dir.path(), "medium.txt", "abcde", Duration::days(1)); // 5 bytes
    create_test_file(dir.path(), "large.txt", &"x".repeat(100), Duration::days(1)); // 100 bytes

    let output = run_void_scout(&[".", "--min-size", "5B"], dir.path());
    assert!(!output.contains("small.txt"));
    assert!(output.contains("medium.txt"));
    assert!(output.contains("large.txt"));

    let output = run_void_scout(&[".", "--max-size", "5B"], dir.path());
    assert!(output.contains("small.txt"));
    assert!(output.contains("medium.txt"));
    assert!(!output.contains("large.txt"));

    let output = run_void_scout(&[".", "--min-size", "2B", "--max-size", "6B"], dir.path());
    assert!(!output.contains("small.txt"));
    assert!(output.contains("medium.txt"));
    assert!(!output.contains("large.txt"));
}

#[test]
fn test_modified_since_filtering() {
    let dir = tempdir().expect("Failed to create temp dir");
    create_test_file(dir.path(), "old.txt", "old", Duration::days(5));
    create_test_file(dir.path(), "recent.txt", "recent", Duration::hours(12));
    create_test_file(dir.path(), "very_recent.txt", "v_recent", Duration::minutes(5));

    let output = run_void_scout(&[".", "--modified-since", "1d"], dir.path());
    assert!(!output.contains("old.txt"));
    assert!(output.contains("recent.txt"));
    assert!(output.contains("very_recent.txt"));

    let output = run_void_scout(&[".", "--modified-since", "1h"], dir.path());
    assert!(!output.contains("old.txt"));
    assert!(!output.contains("recent.txt"));
    assert!(output.contains("very_recent.txt"));
}

#[test]
fn test_directory_and_file_only_filters() {
    let dir = tempdir().expect("Failed to create temp dir");
    let subdir_path = dir.path().join("my_subdir");
    fs::create_dir(&subdir_path).expect("Failed to create subdir");
    create_test_file(&subdir_path, "file_in_subdir.txt", "content", Duration::days(1));
    create_test_file(dir.path(), "root_file.txt", "content", Duration::days(1));

    let output = run_void_scout(&[".", "--directories-only"], dir.path());
    assert!(output.contains("my_subdir"));
    assert!(!output.contains("root_file.txt"));
    assert!(!output.contains("file_in_subdir.txt"));

    let output = run_void_scout(&[".", "--files-only"], dir.path());
    assert!(!output.contains("my_subdir"));
    assert!(output.contains("root_file.txt"));
    assert!(output.contains("file_in_subdir.txt"));

    // Test combined with name filter
    let output = run_void_scout(&[".", "--directories-only", "--name", "my_subdir"], dir.path());
    assert!(output.contains("my_subdir"));
    assert!(!output.contains("root_file.txt"));

    let output = run_void_scout(&[".", "--files-only", "--name", "root_file"], dir.path());
    assert!(!output.contains("my_subdir"));
    assert!(output.contains("root_file.txt"));
}

#[test]
fn test_combined_filters() {
    let dir = tempdir().expect("Failed to create temp dir");
    create_test_file(dir.path(), "report_old.txt", &"a".repeat(20), Duration::days(5));
    create_test_file(dir.path(), "report_recent.log", &"b".repeat(50), Duration::hours(10));
    create_test_file(dir.path(), "data_recent.txt", &"c".repeat(10), Duration::hours(2));

    let output = run_void_scout(&[
        ".",
        "--name", "report",
        "--min-size", "30B",
        "--modified-since", "1d",
    ], dir.path());

    assert!(!output.contains("report_old.txt"));
    assert!(output.contains("report_recent.log"));
    assert!(!output.contains("data_recent.txt"));
}

#[test]
fn test_no_match() {
    let dir = tempdir().expect("Failed to create temp dir");
    create_test_file(dir.path(), "file1.txt", "content", Duration::days(1));

    let output = run_void_scout(&[".", "--name", "nonexistent"], dir.path());
    assert!(output.is_empty());

    let output = run_void_scout(&[".", "--min-size", "1GB"], dir.path());
    assert!(output.is_empty());
}
