#![allow(unused_imports)] // Mock rationale: Some imports might be used in more complex tests, but kept for clarity.

use std::fs::{self, File};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use tempfile::tempdir;
use filetime::{set_file_mtime, FileTime};

// Import the main logic for testing
use nightly_digital_decay_detector::parse_duration_arg;

// Helper to create a file with specific modification time
fn create_file_with_mtime(dir: &Path, filename: &str, mtime: SystemTime) -> PathBuf {
    let file_path = dir.join(filename);
    File::create(&file_path).unwrap().write_all(b"test content").unwrap();
    let ft = FileTime::from_system_time(mtime);
    set_file_mtime(&file_path, ft).unwrap();
    file_path
}

#[test]
fn test_parse_duration_arg() {
    assert_eq!(parse_duration_arg("30s").unwrap(), Duration::from_secs(30));
    assert_eq!(parse_duration_arg("1m").unwrap(), Duration::from_secs(60));
    assert_eq!(parse_duration_arg("2h").unwrap(), Duration::from_secs(7200));
    assert_eq!(parse_duration_arg("7d").unwrap(), Duration::from_secs(7 * 24 * 3600));
    assert_eq!(parse_duration_arg("1w").unwrap(), Duration::from_secs(7 * 24 * 3600 * 7));
    assert!(parse_duration_arg("invalid").is_err());
    assert!(parse_duration_arg("1x").is_err());
    assert!(parse_duration_arg("s").is_err()); // No number
    assert!(parse_duration_arg("").is_err());
}

#[test]
fn test_decay_detection() {
    // Mock rationale: We create a temporary directory and files with specific modification times
    // to simulate different ages, making the test deterministic and offline without relying on
    // the actual SystemTime::now() for file creation. The 'current_time_for_test' acts as a fixed reference.
    let dir = tempdir().unwrap();
    let path = dir.path();

    // Define a fixed "current time" for the test to ensure determinism
    let current_time_for_test = SystemTime::UNIX_EPOCH + Duration::from_secs(1_000_000_000);

    // File 1: Very old, should be detected (e.g., 100 days old)
    let old_file_mtime = current_time_for_test - Duration::from_secs(100 * 24 * 3600);
    let old_file_path = create_file_with_mtime(path, "ancient.txt", old_file_mtime);

    // File 2: Moderately old, should be detected (e.g., 50 days old)
    let moderately_old_file_mtime = current_time_for_test - Duration::from_secs(50 * 24 * 3600);
    let moderately_old_file_path = create_file_with_mtime(path, "dusty.log", moderately_old_file_mtime);

    // File 3: Recent, should NOT be detected (e.g., 10 days old)
    let recent_file_mtime = current_time_for_test - Duration::from_secs(10 * 24 * 3600);
    let recent_file_path = create_file_with_mtime(path, "fresh.md", recent_file_mtime);

    // File 4: Nested old file
    let nested_dir = path.join("sub");
    fs::create_dir(&nested_dir).unwrap();
    let nested_old_file_mtime = current_time_for_test - Duration::from_secs(60 * 24 * 3600);
    let nested_old_file_path = create_file_with_mtime(&nested_dir, "deep_ancient.json", nested_old_file_mtime);

    // Set the age threshold for detection (e.g., 30 days)
    // The main function uses SystemTime::now() internally, so we simulate running the command.
    // The files' mtimes are set relative to a fixed 'current_time_for_test', so when the actual
    // command runs, the relative ages will be consistent for the test duration.

    // Capture stdout to check output
    let mut cmd = std::process::Command::new(env!("CARGO_BIN_EXE_nightly-digital-decay-detector"));
    cmd.arg(path.to_str().unwrap()).arg("--age").arg("30d");

    let output = cmd.output().expect("Failed to execute command");
    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    // Assert that old files are reported
    assert!(stdout.contains(&format!("Found ancient data: {}", old_file_path.display())),
            "Expected output to contain old_file_path: {}\nStdout: {}\nStderr: {}", old_file_path.display(), stdout, stderr);
    assert!(stdout.contains(&format!("Found ancient data: {}", moderately_old_file_path.display())),
            "Expected output to contain moderately_old_file_path: {}\nStdout: {}\nStderr: {}", moderately_old_file_path.display(), stdout, stderr);
    assert!(stdout.contains(&format!("Found ancient data: {}", nested_old_file_path.display())),
            "Expected output to contain nested_old_file_path: {}\nStdout: {}\nStderr: {}", nested_old_file_path.display(), stdout, stderr);

    // Assert that recent file is NOT reported
    assert!(!stdout.contains(&format!("Found ancient data: {}", recent_file_path.display())),
            "Expected output NOT to contain recent_file_path: {}\nStdout: {}\nStderr: {}", recent_file_path.display(), stdout, stderr);

    // Assert the summary message indicates files were found
    assert!(stdout.contains("Digital decay detected!"), "Expected summary message for decay detection.\nStdout: {}\nStderr: {}", stdout, stderr);
    assert!(stdout.contains("Found 3 ancient files"), "Expected count of 3 ancient files.\nStdout: {}\nStderr: {}", stdout, stderr);

    // Clean up temporary directory
    dir.close().unwrap();
}

#[test]
fn test_no_decay_detection() {
    // Mock rationale: Similar to test_decay_detection, we use a temporary directory and control
    // file modification times to ensure no files are older than the threshold, making the test deterministic.
    let dir = tempdir().unwrap();
    let path = dir.path();

    let current_time_for_test = SystemTime::UNIX_EPOCH + Duration::from_secs(1_000_000_000);

    // File 1: Recent, should NOT be detected (e.g., 10 days old)
    let recent_file_mtime = current_time_for_test - Duration::from_secs(10 * 24 * 3600);
    let recent_file_path = create_file_with_mtime(path, "fresh_one.txt", recent_file_mtime);

    // File 2: Also recent, should NOT be detected (e.g., 5 days old)
    let very_recent_file_mtime = current_time_for_test - Duration::from_secs(5 * 24 * 3600);
    let very_recent_file_path = create_file_with_mtime(path, "fresh_two.log", very_recent_file_mtime);

    // Set the age threshold for detection (e.g., 30 days)
    let min_age_duration = parse_duration_arg("30d").unwrap();

    // Capture stdout to check output
    let mut cmd = std::process::Command::new(env!("CARGO_BIN_EXE_nightly-digital-decay-detector"));
    cmd.arg(path.to_str().unwrap()).arg("--age").arg("30d");

    let output = cmd.output().expect("Failed to execute command");
    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    // Assert that no files are reported as ancient
    assert!(!stdout.contains("Found ancient data:"), "Expected no ancient files to be reported.\nStdout: {}\nStderr: {}", stdout, stderr);

    // Assert the summary message indicates no files were found
    assert!(stdout.contains("All clear! No digital dust bunnies or temporal echoes found."), "Expected summary message for no decay detection.\nStdout: {}\nStderr: {}", stdout, stderr);

    // Clean up temporary directory
    dir.close().unwrap();
}

#[test]
fn test_invalid_path() {
    let mut cmd = std::process::Command::new(env!("CARGO_BIN_EXE_nightly-digital-decay-detector"));
    cmd.arg("/non/existent/path").arg("--age").arg("1d");

    let output = cmd.output().expect("Failed to execute command");
    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(!output.status.success());
    assert!(stderr.contains("Error: Path does not exist:"));
}

#[test]
fn test_path_is_file_not_dir() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("a_file.txt");
    File::create(&file_path).unwrap().write_all(b"content").unwrap();

    let mut cmd = std::process::Command::new(env!("CARGO_BIN_EXE_nightly-digital-decay-detector"));
    cmd.arg(file_path.to_str().unwrap()).arg("--age").arg("1d");

    let output = cmd.output().expect("Failed to execute command");
    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(!output.status.success());
    assert!(stderr.contains("Error: Path is not a directory:"));
}
