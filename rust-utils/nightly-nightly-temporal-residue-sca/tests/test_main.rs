use std::process::Command;
use std::fs::{self, File};
use std::io::Write;
use std::path::Path;
use tempfile::tempdir;
use chrono::{Utc, Duration};
use filetime::{set_file_times, FileTime};

// Helper to create a file with specific modification/access times
fn create_test_file(dir: &Path, name: &str, age_days: i64) -> std::io::Result<()> {
    let file_path = dir.join(name);
    let mut file = File::create(&file_path)?;
    writeln!(file, "test content")?;

    let now = Utc::now();
    let past_time = now - Duration::days(age_days);
    let file_time = FileTime::from_system_time(past_time.into());

    set_file_times(&file_path, file_time, file_time)?; // Set both access and modification
    Ok(())
}

#[test]
fn test_temporal_residue_scanner_modified_time() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Creating temporary files with controlled timestamps allows for deterministic
    // testing of file system traversal and age-based filtering without interacting with the actual,
    // unpredictable file system state of the running environment. This ensures tests are
    // self-contained and offline.
    let dir = tempdir()?;
    let path = dir.path();

    // Create files with different ages relative to a 365-day threshold
    create_test_file(path, "old_echo.txt", 400)?; // Older than 365 days
    create_test_file(path, "recent_whisper.txt", 10)?; // Newer than 365 days
    create_test_file(path, "just_under_threshold.txt", 360)?; // Just under 365 days

    // Run the command with default (modified time) and 365-day age
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-temporal-residue-scanner"))
        .arg(path.to_str().unwrap())
        .arg("--age")
        .arg("365")
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("old_echo.txt"));
    assert!(!stdout.contains("recent_whisper.txt"));
    assert!(!stdout.contains("just_under_threshold.txt"));
    assert!(stdout.contains("Temporal residue scan complete."));

    Ok(())
}

#[test]
fn test_temporal_residue_scanner_access_time() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Creating temporary files with controlled timestamps allows for deterministic
    // testing of file system traversal and age-based filtering without interacting with the actual,
    // unpredictable file system state of the running environment. This ensures tests are
    // self-contained and offline.
    let dir = tempdir()?;
    let path = dir.path();

    // Create files with different ages relative to a 365-day threshold
    create_test_file(path, "old_accessed_echo.txt", 400)?; // Older than 365 days
    create_test_file(path, "recent_accessed_whisper.txt", 10)?; // Newer than 365 days

    // Run the command using --access flag and 365-day age
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-temporal-residue-scanner"))
        .arg(path.to_str().unwrap())
        .arg("--age")
        .arg("365")
        .arg("--access")
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("old_accessed_echo.txt"));
    assert!(!stdout.contains("recent_accessed_whisper.txt"));
    assert!(stdout.contains("Temporal residue scan complete."));

    Ok(())
}

#[test]
fn test_no_residue_found() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Creating temporary files with controlled timestamps allows for deterministic
    // testing of file system traversal and age-based filtering without interacting with the actual,
    // unpredictable file system state of the running environment. This ensures tests are
    // self-contained and offline.
    let dir = tempdir()?;
    let path = dir.path();

    // Create only recent files
    create_test_file(path, "recent_file_1.txt", 50)?; // Newer than 365 days
    create_test_file(path, "recent_file_2.txt", 100)?; // Newer than 365 days

    // Run the command with default (modified time) and 365-day age
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-temporal-residue-scanner"))
        .arg(path.to_str().unwrap())
        .arg("--age")
        .arg("365")
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(!stdout.contains("recent_file_1.txt"));
    assert!(!stdout.contains("recent_file_2.txt"));
    assert!(stdout.contains("No significant temporal residue detected."));

    Ok(())
}
