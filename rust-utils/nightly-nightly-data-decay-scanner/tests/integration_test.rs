use std::fs;
use std::io::Write;
use std::time::{SystemTime, Duration};
use tempfile::tempdir;
use filetime::{set_file_times, FileTime};

// Mock rationale: These tests create temporary files and explicitly set their modification and access times
// using the `filetime` crate. This ensures deterministic behavior by controlling the file system state
// and timestamps, making the tests independent of the actual system's current time or file access patterns.
// Without this, tests would be non-deterministic due to varying file metadata.

#[test]
fn test_decay_calculation_and_suggestions() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create files with specific timestamps
    let now = SystemTime::now();

    // File 1: Very recent (Active Data)
    let file1_path = path.join("recent_file.txt");
    fs::File::create(&file1_path)?.write_all(b"hello")?;
    let recent_time = FileTime::from_system_time(now - Duration::from_secs(60 * 60)); // 1 hour ago
    set_file_times(&file1_path, recent_time, recent_time)?;

    // File 2: Archival Candidate (e.g., 100 days old, with default threshold 365)
    let file2_path = path.join("archive_candidate.log");
    fs::File::create(&file2_path)?.write_all(b"log data")?;
    let archive_time = FileTime::from_system_time(now - Duration::from_secs(100 * 24 * 60 * 60)); // 100 days ago
    set_file_times(&file2_path, archive_time, archive_time)?;

    // File 3: Deletion Candidate (e.g., 400 days old, with default threshold 365)
    let file3_path = path.join("delete_me.bak");
    fs::File::create(&file3_path)?.write_all(b"backup data")?;
    let delete_time = FileTime::from_system_time(now - Duration::from_secs(400 * 24 * 60 * 60)); // 400 days ago
    set_file_times(&file3_path, delete_time, delete_time)?;

    // File 4: Another recent file in a subdirectory
    let subdir_path = path.join("subdir");
    fs::create_dir(&subdir_path)?;
    let file4_path = subdir_path.join("another_recent.md");
    fs::File::create(&file4_path)?.write_all(b"markdown")?;
    let another_recent_time = FileTime::from_system_time(now - Duration::from_secs(2 * 24 * 60 * 60)); // 2 days ago
    set_file_times(&file4_path, another_recent_time, another_recent_time)?;

    // Capture stdout
    let mut cmd = assert_cmd::Command::cargo_bin("nightly-data-decay-scanner")?;
    cmd.arg(path.to_str().unwrap()).arg("--threshold").arg("365");

    let output = cmd.output()?;
    let stdout = String::from_utf8(output.stdout)?;

    // Assertions
    assert!(output.status.success());
    assert!(stdout.contains("--- Data Decay Scan Results"));
    assert!(stdout.contains("Deletion Threshold: 365 days, Archival Threshold: 182 days"));

    // Check for expected classifications (order might vary based on exact decay days if very close)
    assert!(stdout.contains(&format!("[Deletion Candidate  ] {}", file3_path.display())));
    assert!(stdout.contains(&format!("[Archival Candidate  ] {}", file2_path.display())));
    assert!(stdout.contains(&format!("[Active Data         ] {}", file1_path.display())));
    assert!(stdout.contains(&format!("[Active Data         ] {}", file4_path.display())));

    // Test verbose output
    let mut cmd_verbose = assert_cmd::Command::cargo_bin("nightly-data-decay-scanner")?;
    cmd_verbose.arg(path.to_str().unwrap()).arg("-v").arg("-t").arg("365");
    let output_verbose = cmd_verbose.output()?;
    let stdout_verbose = String::from_utf8(output_verbose.stdout)?;

    assert!(output_verbose.status.success());
    assert!(stdout_verbose.contains(&format!("[Deletion Candidate  ] 400 days: {}", file3_path.display())));
    assert!(stdout_verbose.contains(&format!("[Archival Candidate  ] 100 days: {}", file2_path.display())));
    assert!(stdout_verbose.contains(&format!("[Active Data         ] 0 days: {}", file1_path.display()))); // 1 hour is 0 days
    assert!(stdout_verbose.contains(&format!("[Active Data         ] 2 days: {}", file4_path.display())));

    Ok(())
}

#[test]
fn test_empty_directory() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let mut cmd = assert_cmd::Command::cargo_bin("nightly-data-decay-scanner")?;
    cmd.arg(path.to_str().unwrap());

    let output = cmd.output()?;
    let stdout = String::from_utf8(output.stdout)?;

    assert!(output.status.success());
    assert!(stdout.contains("No files found or no decay information available."));

    Ok(())
}

#[test]
fn test_non_existent_path() -> Result<(), Box<dyn std::error::Error>> {
    let non_existent_path = "/this/path/does/not/exist_12345";

    let mut cmd = assert_cmd::Command::cargo_bin("nightly-data-decay-scanner")?;
    cmd.arg(non_existent_path);

    let output = cmd.output()?;
    let stderr = String::from_utf8(output.stderr)?;

    assert!(!output.status.success());
    assert!(stderr.contains("Error: Provided path is not a directory"));

    Ok(())
}
