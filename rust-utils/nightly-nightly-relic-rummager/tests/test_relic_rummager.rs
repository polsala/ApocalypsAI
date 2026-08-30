use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use tempfile::tempdir;

// Mock rationale: For testing file system utilities, creating temporary files and directories
// is a standard and deterministic way to simulate real-world scenarios without relying on
// external resources or modifying the actual file system. The `tempfile` crate provides
// robust cross-platform temporary file/directory creation and automatic cleanup.

// Helper function to run the main logic with a given directory and capture output
fn run_main_and_capture_output(directory: &PathBuf) -> String {
    let mut cmd = std::process::Command::new(env!("CARGO_BIN_EXE_nightly-relic-rummager"));
    cmd.arg(directory.to_str().unwrap());
    let output = cmd.output().expect("Failed to execute command");
    
    // Combine stdout and stderr for easier assertion, as warnings might go to stderr
    let stdout = String::from_utf8_lossy(&output.stdout).to_string();
    let stderr = String::from_utf8_lossy(&output.stderr).to_string();
    format!("{}{}", stdout, stderr)
}

#[test]
fn test_empty_directory() {
    let dir = tempdir().expect("Failed to create temp dir");
    let output = run_main_and_capture_output(&dir.path().to_path_buf());

    assert!(output.contains("Total files scanned: 0"));
    assert!(output.contains("Total unique relics found: 0"));
    assert!(output.contains("Total common junk (duplicates): 0"));
    assert!(!output.contains("Precious Artifacts"));
    assert!(!output.contains("Common Junk"));
    assert!(!output.contains("File Type Manifest"));
}

#[test]
fn test_unique_files() {
    let dir = tempdir().expect("Failed to create temp dir");
    let file1_path = dir.path().join("relic1.txt");
    let file2_path = dir.path().join("artifact.log");

    File::create(&file1_path).unwrap().write_all(b"unique content 1").unwrap();
    File::create(&file2_path).unwrap().write_all(b"unique content 2").unwrap();

    let output = run_main_and_capture_output(&dir.path().to_path_buf());

    assert!(output.contains("Total files scanned: 2"));
    assert!(output.contains("Total unique relics found: 2"));
    assert!(output.contains("Total common junk (duplicates): 0"));
    assert!(output.contains("relic1.txt"));
    assert!(output.contains("artifact.log"));
    assert!(output.contains(".txt: 1 files"));
    assert!(output.contains(".log: 1 files"));
}

#[test]
fn test_duplicate_files() {
    let dir = tempdir().expect("Failed to create temp dir");
    let file1_path = dir.path().join("duplicate_a.txt");
    let file2_path = dir.path().join("duplicate_b.txt");
    let file3_path = dir.path().join("unique.txt");

    let common_content = b"shared content";
    File::create(&file1_path).unwrap().write_all(common_content).unwrap();
    File::create(&file2_path).unwrap().write_all(common_content).unwrap();
    File::create(&file3_path).unwrap().write_all(b"different content").unwrap();

    let output = run_main_and_capture_output(&dir.path().to_path_buf());

    assert!(output.contains("Total files scanned: 3"));
    assert!(output.contains("Total unique relics found: 1"));
    assert!(output.contains("Total common junk (duplicates): 2"));
    assert!(output.contains("unique.txt"));
    assert!(output.contains("Common Junk (Duplicate Groups)"));
    assert!(output.contains("duplicate_a.txt"));
    assert!(output.contains("duplicate_b.txt"));
    assert!(output.contains(".txt: 3 files"));
}

#[test]
fn test_mixed_files_and_subdirectories() {
    let dir = tempdir().expect("Failed to create temp dir");
    let subdir = dir.path().join("subdir");
    fs::create_dir(&subdir).unwrap();

    let file1_path = dir.path().join("unique_root.md");
    let file2_path = subdir.join("unique_sub.json");
    let file3_path = dir.path().join("dup_1.log");
    let file4_path = subdir.join("dup_2.log");
    let file5_path = dir.path().join("empty_file.txt"); // Empty files have same hash
    let file6_path = subdir.join("another_empty.txt");

    let common_log_content = b"log data";
    File::create(&file1_path).unwrap().write_all(b"markdown content").unwrap();
    File::create(&file2_path).unwrap().write_all(b"json content").unwrap();
    File::create(&file3_path).unwrap().write_all(common_log_content).unwrap();
    File::create(&file4_path).unwrap().write_all(common_log_content).unwrap();
    File::create(&file5_path).unwrap().write_all(b"").unwrap();
    File::create(&file6_path).unwrap().write_all(b"").unwrap();

    let output = run_main_and_capture_output(&dir.path().to_path_buf());

    assert!(output.contains("Total files scanned: 6"));
    assert!(output.contains("Total unique relics found: 2")); // markdown, json
    assert!(output.contains("Total common junk (duplicates): 4")); // 2 logs, 2 empty files

    assert!(output.contains("unique_root.md"));
    assert!(output.contains("unique_sub.json"));

    assert!(output.contains("dup_1.log"));
    assert!(output.contains("dup_2.log"));
    assert!(output.contains("empty_file.txt"));
    assert!(output.contains("another_empty.txt"));

    assert!(output.contains(".md: 1 files"));
    assert!(output.contains(".json: 1 files"));
    assert!(output.contains(".log: 2 files"));
    assert!(output.contains(".txt: 2 files"));
}

#[test]
fn test_non_existent_directory() {
    let non_existent_path = PathBuf::from("non_existent_dir_12345");
    let output = run_main_and_capture_output(&non_existent_path);

    assert!(output.contains(&format!("Error: Provided path is not a directory: {}", non_existent_path.display())));
    // The process should exit with an error code, but capturing stdout/stderr is enough for this test.
}

#[test]
fn test_file_as_directory_input() {
    let dir = tempdir().expect("Failed to create temp dir");
    let file_path = dir.path().join("a_file.txt");
    File::create(&file_path).unwrap().write_all(b"content").unwrap();

    let output = run_main_and_capture_output(&file_path);

    assert!(output.contains(&format!("Error: Provided path is not a directory: {}", file_path.display())));
}
