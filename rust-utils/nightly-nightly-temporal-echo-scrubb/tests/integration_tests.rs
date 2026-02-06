use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::{tempdir, TempDir};
use std::fs::{self, File};
use std::path::{Path, PathBuf};
use std::io::Write;

// Helper to create a file with specific content.
// Mock rationale: We can't reliably set arbitrary past modification times
// across all OSes and file systems without external crates like `filetime`.
// For deterministic offline tests, we simulate "old" by setting the `--age`
// parameter to `0`. This means any file not modified *in the current instant*
// will be considered "old enough". This effectively captures all files created
// during the test setup as targets for scrubbing, making the tests reliable
// without complex time manipulation.
fn create_file_with_content(dir: &Path, filename: &str, content: &str) -> PathBuf {
    let file_path = dir.join(filename);
    let mut file = File::create(&file_path).unwrap();
    file.write_all(content.as_bytes()).unwrap();
    file_path
}

// Helper to create a directory
fn create_dir(dir: &Path, dirname: &str) -> PathBuf {
    let path = dir.join(dirname);
    fs::create_dir(&path).unwrap();
    path
}

#[test]
fn test_dry_run_identifies_old_files() {
    let temp_dir = tempdir().unwrap();
    let root = temp_dir.path();

    create_file_with_content(root, "old_log.log", "log content");
    create_file_with_content(root, "new_file.txt", "new content");
    let target_dir = create_dir(root, "target");
    create_file_with_content(&target_dir, "build_artifact.bin", "binary");

    Command::cargo_bin("nightly-temporal-echo-scrubber")
        .unwrap()
        .arg("--path")
        .arg(root)
        .arg("--age")
        .arg("0") // Treat all files as old for testing purposes
        .arg("--patterns")
        .arg("*.log,target/")
        .arg("--dry-run")
        .assert()
        .success()
        .stdout(predicate::str::contains("[DRY RUN] Would scrub:").count(2)) // old_log.log and target/
        .stdout(predicate::str::contains("old_log.log"))
        .stdout(predicate::str::contains("target"));

    // Ensure no files were actually removed in dry run
    assert!(root.join("old_log.log").exists());
    assert!(root.join("new_file.txt").exists());
    assert!(root.join("target").exists());
    assert!(root.join("target/build_artifact.bin").exists());
}

#[test]
fn test_delete_removes_old_files() {
    let temp_dir = tempdir().unwrap();
    let root = temp_dir.path();

    create_file_with_content(root, "old_config.bak", "backup data");
    create_file_with_content(root, "important.txt", "keep this");
    let node_modules_dir = create_dir(root, "node_modules");
    create_file_with_content(&node_modules_dir, "package.js", "js code");

    Command::cargo_bin("nightly-temporal-echo-scrubber")
        .unwrap()
        .arg("--path")
        .arg(root)
        .arg("--age")
        .arg("0") // Treat all files as old for testing purposes
        .arg("--patterns")
        .arg("*.bak,node_modules/")
        .arg("--delete")
        .assert()
        .success()
        .stdout(predicate::str::contains("[DELETED]").count(2)) // old_config.bak and node_modules/
        .stdout(predicate::str::contains("old_config.bak"))
        .stdout(predicate::str::contains("node_modules"));

    // Ensure specified files/dirs are removed, others remain
    assert!(!root.join("old_config.bak").exists());
    assert!(root.join("important.txt").exists());
    assert!(!root.join("node_modules").exists()); // node_modules dir should be gone
}

#[test]
fn test_archive_moves_old_files() {
    let temp_dir = tempdir().unwrap();
    let root = temp_dir.path();

    create_file_with_content(root, "temp_data.csv", "csv content");
    let logs_dir = create_dir(root, "logs");
    create_file_with_content(&logs_dir, "error.log", "error details");
    create_file_with_content(root, "current_report.pdf", "report");

    Command::cargo_bin("nightly-temporal-echo-scrubber")
        .unwrap()
        .arg("--path")
        .arg(root)
        .arg("--age")
        .arg("0") // Treat all files as old for testing purposes
        .arg("--patterns")
        .arg("*.csv,logs/")
        .arg("--archive")
        .assert()
        .success()
        .stdout(predicate::str::contains("[ARCHIVED]").count(2)) // temp_data.csv and logs/
        .stdout(predicate::str::contains("temp_data.csv"))
        .stdout(predicate::str::contains("logs"));

    // Check original paths are gone
    assert!(!root.join("temp_data.csv").exists());
    assert!(!root.join("logs").exists());
    assert!(root.join("current_report.pdf").exists());

    // Check archive paths exist and maintain relative structure
    let archive_path = root.join(".temporal_void");
    assert!(archive_path.exists());
    assert!(archive_path.join("temp_data.csv").exists());
    assert!(archive_path.join("logs").exists());
    assert!(archive_path.join("logs/error.log").exists());
}

#[test]
fn test_no_action_error() {
    let temp_dir = tempdir().unwrap();
    let root = temp_dir.path();

    Command::cargo_bin("nightly-temporal-echo-scrubber")
        .unwrap()
        .arg("--path")
        .arg(root)
        .arg("--age")
        .arg("0")
        .arg("--patterns")
        .arg("*.log")
        .assert()
        .failure()
        .stderr(predicate::str::contains("Error: No action specified. Use --dry-run, --archive, or --delete."));
}

#[test]
fn test_archive_skips_archive_dir() {
    let temp_dir = tempdir().unwrap();
    let root = temp_dir.path();

    create_file_with_content(root, "old_file.txt", "content");
    let archive_dir = create_dir(root, ".temporal_void");
    create_file_with_content(&archive_dir, "archived_item.txt", "archived content");

    Command::cargo_bin("nightly-temporal-echo-scrubber")
        .unwrap()
        .arg("--path")
        .arg(root)
        .arg("--age")
        .arg("0")
        .arg("--patterns")
        .arg("*.txt")
        .arg("--archive")
        .assert()
        .success()
        .stdout(predicate::str::contains("[ARCHIVED]").count(1)) // Only old_file.txt should be archived
        .stdout(predicate::str::contains("old_file.txt"))
        .stdout(predicate::str::contains("archived_item.txt").not()); // Should not try to archive itself

    assert!(!root.join("old_file.txt").exists());
    assert!(root.join(".temporal_void/old_file.txt").exists());
    assert!(root.join(".temporal_void/archived_item.txt").exists()); // This was already there
}
