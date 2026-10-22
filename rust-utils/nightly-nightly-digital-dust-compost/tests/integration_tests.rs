use std::fs;
use std::io::Write;
use std::path::PathBuf;
use std::process::Command;
use std::time::{SystemTime, Duration};
use tempfile::tempdir;

// Mock rationale: Using `tempfile` crate to create isolated, temporary directories and files
// for testing file system interactions without affecting the actual file system. This ensures
// deterministic and offline tests.

#[test]
fn test_scan_no_dust_bunnies() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path().to_path_buf();

    // Create a fresh file (should not be considered dust)
    let fresh_file = path.join("fresh.txt");
    fs::write(&fresh_file, "content")?;

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-digital-dust-composter"))
        .arg(&path)
        .arg("-a")
        .arg("1") // Look for files older than 1 day
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("No digital dust bunnies found older than 1 days. Your digital garden is pristine!"));
    assert!(!stdout.contains("fresh.txt"));
    assert!(output.status.success());

    dir.close()?;
    Ok(())
}

#[test]
fn test_scan_with_dust_bunnies() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path().to_path_buf();

    // Create an old file (older than 30 days default age)
    let old_file = path.join("old_bunny.txt");
    fs::write(&old_file, "old content")?;
    let thirty_one_days_ago = SystemTime::now() - Duration::from_secs(31 * 24 * 3600);
    filetime::set_file_mtime(&old_file, filetime::FileTime::from_system_time(thirty_one_days_ago))?;

    // Create a very old file (older than 90 days)
    let very_old_file = path.join("petrified_relic.log");
    fs::write(&very_old_file, "ancient logs")?;
    let ninety_one_days_ago = SystemTime::now() - Duration::from_secs(91 * 24 * 3600);
    filetime::set_file_mtime(&very_old_file, filetime::FileTime::from_system_time(ninety_one_days_ago))?;

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-digital-dust-composter"))
        .arg(&path)
        .arg("-a")
        .arg("1") // Look for files older than 1 day
        .arg("-v") // Verbose output to see individual files
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    // println!("Output: {}\nStderr: {}", stdout, String::from_utf8_lossy(&output.stderr)); // Uncomment for debugging

    assert!(stdout.contains("Scanning"));
    assert!(stdout.contains("--- Ancient Compost ---"));
    assert!(stdout.contains(&format!("old_bunny.txt")));
    assert!(stdout.contains("--- Petrified Relics ---"));
    assert!(stdout.contains(&format!("petrified_relic.log")));
    assert!(stdout.contains("Total digital dust bunnies found: 2"));
    assert!(output.status.success());

    dir.close()?;
    Ok(())
}

#[test]
fn test_delete_dust_bunnies() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path().to_path_buf();

    let file_to_delete = path.join("delete_me.tmp");
    fs::write(&file_to_delete, "ephemeral content")?;
    let thirty_one_days_ago = SystemTime::now() - Duration::from_secs(31 * 24 * 3600);
    filetime::set_file_mtime(&file_to_delete, filetime::FileTime::from_system_time(thirty_one_days_ago))?;

    assert!(file_to_delete.exists());

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-digital-dust-composter"))
        .arg(&path)
        .arg("-a")
        .arg("1") // Look for files older than 1 day
        .arg("-d") // Delete the files
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    // println!("Output: {}\nStderr: {}", stdout, String::from_utf8_lossy(&output.stderr)); // Uncomment for debugging

    assert!(stdout.contains("Initiating composting process..."));
    assert!(stdout.contains(&format!("Composted: {}", file_to_delete.display())));
    assert!(stdout.contains("Composting complete!"));
    assert!(!file_to_delete.exists()); // File should be deleted
    assert!(output.status.success());

    dir.close()?;
    Ok(())
}

#[test]
fn test_invalid_path() -> Result<(), Box<dyn std::error::Error>> {
    let non_existent_path = PathBuf::from("/non/existent/path/for/testing");

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-digital-dust-composter"))
        .arg(&non_existent_path)
        .output()?;

    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains(&format!("Error: Provided path is not a directory: {}", non_existent_path.display())));
    assert!(!output.status.success()); // Should exit with an error status

    Ok(())
}
