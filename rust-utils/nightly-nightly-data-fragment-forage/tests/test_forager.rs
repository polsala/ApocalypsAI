use std::fs::{self, File};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, Duration};
use tempfile::tempdir;

// Helper function to create a file with content and optional modification time
fn create_test_file(dir: &Path, name: &str, content: &str, modified_offset_days: Option<u64>) -> PathBuf {
    let file_path = dir.join(name);
    let mut file = File::create(&file_path).unwrap();
    file.write_all(content.as_bytes()).unwrap();
    file.sync_all().unwrap();

    if let Some(days) = modified_offset_days {
        // Mock rationale: We set the modification time explicitly for deterministic testing of 'ancient' files.
        // In a real scenario, this would be the actual file's modification time.
        let past_time = SystemTime::now() - Duration::from_secs(days * 24 * 60 * 60);
        filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(past_time)).unwrap();
    }
    file_path
}

// Helper to run the compiled binary and capture stdout
fn run_main_and_capture_output(args: Vec<&str>) -> String {
    let mut cmd = std::process::Command::new(env!("CARGO_BIN_EXE_nightly-data-fragment-forager"));
    cmd.args(args);
    let output = cmd.output().expect("Failed to execute command");
    String::from_utf8(output.stdout).unwrap()
}

#[test]
fn test_empty_file_detection() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    create_test_file(path, "empty.txt", "", None);
    create_test_file(path, "not_empty.txt", "some content", None);

    let output = run_main_and_capture_output(vec![path.to_str().unwrap(), "--empty"]);

    assert!(output.contains("--- Empty Files (Digital Voids) ---"));
    assert!(output.contains("empty.txt"));
    assert!(!output.contains("not_empty.txt"));
    assert!(!output.contains("No significant digital debris found"));
}

#[test]
fn test_duplicate_file_detection() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    create_test_file(path, "file1.txt", "duplicate content", None);
    create_test_file(path, "file2.txt", "duplicate content", None);
    create_test_file(path, "unique.txt", "unique content", None);

    let output = run_main_and_capture_output(vec![path.to_str().unwrap(), "--duplicates"]);

    assert!(output.contains("--- Duplicate Fragments (Echoes in the Data Stream) ---"));
    assert!(output.contains("file1.txt"));
    assert!(output.contains("file2.txt"));
    assert!(!output.contains("unique.txt"));
    assert!(!output.contains("No significant digital debris found"));
}

#[test]
fn test_ancient_file_detection() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    // Create a file that is 60 days old
    create_test_file(path, "ancient.log", "old data", Some(60));
    // Create a file that is 10 days old
    create_test_file(path, "recent.log", "new data", Some(10));

    let output = run_main_and_capture_output(vec![path.to_str().unwrap(), "--ancient", "30"]);

    assert!(output.contains("--- Ancient Relics (Forgotten Data) ---"));
    assert!(output.contains("ancient.log"));
    assert!(!output.contains("recent.log"));
    assert!(!output.contains("No significant digital debris found"));
}

#[test]
fn test_no_issues_found() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    create_test_file(path, "normal1.txt", "content A", None);
    create_test_file(path, "normal2.txt", "content B", None);

    let output = run_main_and_capture_output(vec![path.to_str().unwrap(), "--empty", "--duplicates", "--ancient", "1"]);

    assert!(output.contains("No significant digital debris found. Your data stream is clear!"));
    assert!(!output.contains("--- Empty Files"));
    assert!(!output.contains("--- Duplicate Fragments"));
    assert!(!output.contains("--- Ancient Relics"));
}

#[test]
fn test_mixed_issues() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    create_test_file(path, "empty.txt", "", None);
    create_test_file(path, "dup1.txt", "shared content", None);
    create_test_file(path, "dup2.txt", "shared content", None);
    create_test_file(path, "old.log", "very old", Some(90));
    create_test_file(path, "recent.log", "new", Some(5));

    let output = run_main_and_capture_output(vec![path.to_str().unwrap(), "--empty", "--duplicates", "--ancient", "30"]);

    assert!(output.contains("--- Empty Files (Digital Voids) ---"));
    assert!(output.contains("empty.txt"));

    assert!(output.contains("--- Duplicate Fragments (Echoes in the Data Stream) ---"));
    assert!(output.contains("dup1.txt"));
    assert!(output.contains("dup2.txt"));

    assert!(output.contains("--- Ancient Relics (Forgotten Data) ---"));
    assert!(output.contains("old.log"));
    assert!(!output.contains("recent.log"));

    assert!(!output.contains("No significant digital debris found"));
}

#[test]
fn test_multiple_paths() {
    let temp_dir1 = tempdir().unwrap();
    let path1 = temp_dir1.path();
    let temp_dir2 = tempdir().unwrap();
    let path2 = temp_dir2.path();

    create_test_file(path1, "empty1.txt", "", None);
    create_test_file(path2, "empty2.txt", "", None);
    create_test_file(path1, "dup.txt", "content", None);
    create_test_file(path2, "dup.txt", "content", None); // Duplicate across directories

    let output = run_main_and_capture_output(vec![path1.to_str().unwrap(), path2.to_str().unwrap(), "--empty", "--duplicates"]);

    assert!(output.contains("empty1.txt"));
    assert!(output.contains("empty2.txt"));
    assert!(output.contains("dup.txt")); // Should list both paths for dup.txt
}

#[test]
fn test_no_checks_specified() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    create_test_file(path, "file.txt", "content", None);

    let output = run_main_and_capture_output(vec![path.to_str().unwrap()]);

    assert!(output.contains("No checks were specified. Use --empty, --duplicates, or --ancient <DAYS>."));
    assert!(!output.contains("No significant digital debris found"));
}
