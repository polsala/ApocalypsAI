use std::process::Command;
use std::fs::{self, File};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH, Duration};
use tempfile::tempdir;

// Mock rationale: Creating temporary files and directories is a standard and safe way
// to test file system utilities deterministically without affecting the actual system
// or requiring external resources. It allows full control over file properties like
// modification times and sizes.

#[test]
fn test_no_args_error() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-digital-dust-bunny-sweeper"))
        .output()
        .expect("Failed to execute command");

    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Error: At least one of --age or --size must be specified."));
}

#[test]
fn test_age_detection() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create an old file (older than 10 days)
    let old_file_path = path.join("old_file.txt");
    File::create(&old_file_path)?.write_all(b"old content")?;
    let ten_days_ago = SystemTime::now() - Duration::from_days(11); // Make it 11 days old
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(ten_days_ago))?;

    // Create a recent file (newer than 10 days)
    let recent_file_path = path.join("recent_file.txt");
    File::create(&recent_file_path)?.write_all(b"recent content")?;
    // Default creation time is now, so it's recent

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-digital-dust-bunny-sweeper"))
        .arg(path)
        .arg("--age")
        .arg("10") // Look for files older than 10 days
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    println!("STDOUT: {}", stdout);
    assert!(stdout.contains("old_file.txt"));
    assert!(!stdout.contains("recent_file.txt"));
    assert!(stdout.contains("Found 1 digital dust bunnies."));

    dir.close()?;
    Ok(())
}

#[test]
fn test_size_detection() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a large file (larger than 1 MB)
    let large_file_path = path.join("large_file.bin");
    let mut large_file = File::create(&large_file_path)?;
    large_file.write_all(&vec![0; 2 * 1024 * 1024])?; // 2 MB

    // Create a small file (smaller than 1 MB)
    let small_file_path = path.join("small_file.txt");
    File::create(&small_file_path)?.write_all(b"small content")?;

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-digital-dust-bunny-sweeper"))
        .arg(path)
        .arg("--size")
        .arg("1") // Look for files larger than 1 MB
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    println!("STDOUT: {}", stdout);
    assert!(stdout.contains("large_file.bin"));
    assert!(!stdout.contains("small_file.txt"));
    assert!(stdout.contains("Found 1 digital dust bunnies."));

    dir.close()?;
    Ok(())
}

#[test]
fn test_age_and_size_detection() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create an old and large file (dust bunny)
    let old_large_file_path = path.join("old_large.bin");
    let mut old_large_file = File::create(&old_large_file_path)?;
    old_large_file.write_all(&vec![0; 2 * 1024 * 1024])?; // 2 MB
    let ten_days_ago = SystemTime::now() - Duration::from_days(11);
    filetime::set_file_mtime(&old_large_file_path, filetime::FileTime::from_system_time(ten_days_ago))?;

    // Create an old but small file (not a dust bunny by size)
    let old_small_file_path = path.join("old_small.txt");
    File::create(&old_small_file_path)?.write_all(b"old small content")?;
    filetime::set_file_mtime(&old_small_file_path, filetime::FileTime::from_system_time(ten_days_ago))?;

    // Create a recent but large file (not a dust bunny by age)
    let recent_large_file_path = path.join("recent_large.bin");
    let mut recent_large_file = File::create(&recent_large_file_path)?;
    recent_large_file.write_all(&vec![0; 2 * 1024 * 1024])?; // 2 MB

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-digital-dust-bunny-sweeper"))
        .arg(path)
        .arg("--age")
        .arg("10")
        .arg("--size")
        .arg("1")
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    println!("STDOUT: {}", stdout);
    assert!(stdout.contains("old_large.bin"));
    assert!(!stdout.contains("old_small.txt"));
    assert!(!stdout.contains("recent_large.bin"));
    assert!(stdout.contains("Found 1 digital dust bunnies."));

    dir.close()?;
    Ok(())
}

#[test]
fn test_verbose_output() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let old_file_path = path.join("verbose_old_file.txt");
    File::create(&old_file_path)?.write_all(b"old content")?;
    let ten_days_ago = SystemTime::now() - Duration::from_days(11);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(ten_days_ago))?;

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-digital-dust-bunny-sweeper"))
        .arg(path)
        .arg("--age")
        .arg("10")
        .arg("--verbose")
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    println!("STDOUT: {}", stdout);
    assert!(stdout.contains("verbose_old_file.txt"));
    assert!(stdout.contains("Modified 11 days ago")); // Check for verbose detail
    assert!(stdout.contains("Found 1 digital dust bunnies."));

    dir.close()?;
    Ok(())
}

#[test]
fn test_nested_directories() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let nested_dir = path.join("nested");
    fs::create_dir(&nested_dir)?;

    let old_file_path = nested_dir.join("nested_old_file.txt");
    File::create(&old_file_path)?.write_all(b"nested old content")?;
    let ten_days_ago = SystemTime::now() - Duration::from_days(11);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(ten_days_ago))?;

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-digital-dust-bunny-sweeper"))
        .arg(path)
        .arg("--age")
        .arg("10")
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    println!("STDOUT: {}", stdout);
    assert!(stdout.contains("nested/nested_old_file.txt"));
    assert!(stdout.contains("Found 1 digital dust bunnies."));

    dir.close()?;
    Ok(())
}

// Helper for Duration::from_days, not available in std::time::Duration directly
trait DurationExt {
    fn from_days(days: u64) -> Duration;
}

impl DurationExt for Duration {
    fn from_days(days: u64) -> Duration {
        Duration::from_secs(days * 24 * 60 * 60)
    }
}
