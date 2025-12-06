use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;
use std::fs::{self, File};
use std::io::Write;
use std::time::{SystemTime, UNIX_EPOCH};
use chrono::{Utc, Duration, DateTime};

// Mock rationale: We need to create a controlled file system environment
// with files of specific ages to test the utility's logic. 
// Using `tempfile` allows us to create temporary directories and files
// that are automatically cleaned up, ensuring deterministic and isolated tests.
// We manipulate file modification times directly using `filetime` to simulate "old" files.

#[test]
fn test_scan_old_files_default_age() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a new file (should not be reported by default 90d age)
    let new_file_path = path.join("new_file.txt");
    File::create(&new_file_path)?.write_all(b"hello")?;

    // Create an old file (should be reported)
    let old_file_path = path.join("old_file.txt");
    File::create(&old_file_path)?.write_all(b"world")?;
    let ninety_one_days_ago = Utc::now() - Duration::days(91);
    set_file_mtime(&old_file_path, ninety_one_days_ago)?;

    Command::cargo_bin("nightly-chrono-scrub")?
        .arg("-p")
        .arg(path.to_str().unwrap())
        .assert()
        .success()
        .stdout(predicate::str::contains("old_file.txt"))
        .stdout(predicate::str::contains("Found 1 old files."))
        .stdout(predicate::str::not(predicate::str::contains("new_file.txt")));

    Ok(())
}

#[test]
fn test_scan_old_files_custom_age() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a file 10 days old (should be reported with age 5d)
    let ten_day_old_file_path = path.join("ten_day_old.txt");
    File::create(&ten_day_old_file_path)?.write_all(b"data")?;
    let ten_days_ago = Utc::now() - Duration::days(10);
    set_file_mtime(&ten_day_old_file_path, ten_days_ago)?;

    // Create a file 3 days old (should not be reported with age 5d)
    let three_day_old_file_path = path.join("three_day_old.txt");
    File::create(&three_day_old_file_path)?.write_all(b"more data")?;
    let three_days_ago = Utc::now() - Duration::days(3);
    set_file_mtime(&three_day_old_file_path, three_days_ago)?;

    Command::cargo_bin("nightly-chrono-scrub")?
        .arg("-p")
        .arg(path.to_str().unwrap())
        .arg("-a")
        .arg("5d") // Custom age: 5 days
        .assert()
        .success()
        .stdout(predicate::str::contains("ten_day_old.txt"))
        .stdout(predicate::str::contains("Found 1 old files."))
        .stdout(predicate::str::not(predicate::str::contains("three_day_old.txt")));

    Ok(())
}

#[test]
fn test_scan_with_exclusion() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let old_log_file = path.join("old.log");
    File::create(&old_log_file)?.write_all(b"log content")?;
    set_file_mtime(&old_log_file, Utc::now() - Duration::days(100))?;

    let old_txt_file = path.join("old.txt");
    File::create(&old_txt_file)?.write_all(b"text content")?;
    set_file_mtime(&old_txt_file, Utc::now() - Duration::days(100))?;

    Command::cargo_bin("nightly-chrono-scrub")?
        .arg("-p")
        .arg(path.to_str().unwrap())
        .arg("-a")
        .arg("50d")
        .arg("-e")
        .arg(".log") // Exclude log files
        .assert()
        .success()
        .stdout(predicate::str::contains("old.txt"))
        .stdout(predicate::str::contains("Found 1 old files."))
        .stdout(predicate::str::not(predicate::str::contains("old.log")));

    Ok(())
}

#[test]
fn test_scan_with_min_size() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let small_old_file = path.join("small_old.txt");
    File::create(&small_old_file)?.write_all(b"a")?; // 1 byte
    set_file_mtime(&small_old_file, Utc::now() - Duration::days(100))?;

    let large_old_file = path.join("large_old.txt");
    File::create(&large_old_file)?.write_all(&vec![0; 1024])?; // 1KB
    set_file_mtime(&large_old_file, Utc::now() - Duration::days(100))?;

    Command::cargo_bin("nightly-chrono-scrub")?
        .arg("-p")
        .arg(path.to_str().unwrap())
        .arg("-a")
        .arg("50d")
        .arg("--min-size")
        .arg("500B") // Only files >= 500 bytes
        .assert()
        .success()
        .stdout(predicate::str::contains("large_old.txt"))
        .stdout(predicate::str::contains("Found 1 old files."))
        .stdout(predicate::str::not(predicate::str::contains("small_old.txt")));

    Ok(())
}

#[test]
fn test_scan_with_max_size() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let small_old_file = path.join("small_old.txt");
    File::create(&small_old_file)?.write_all(b"a")?; // 1 byte
    set_file_mtime(&small_old_file, Utc::now() - Duration::days(100))?;

    let large_old_file = path.join("large_old.txt");
    File::create(&large_old_file)?.write_all(&vec![0; 1024])?; // 1KB
    set_file_mtime(&large_old_file, Utc::now() - Duration::days(100))?;

    Command::cargo_bin("nightly-chrono-scrub")?
        .arg("-p")
        .arg(path.to_str().unwrap())
        .arg("-a")
        .arg("50d")
        .arg("--max-size")
        .arg("500B") // Only files <= 500 bytes
        .assert()
        .success()
        .stdout(predicate::str::contains("small_old.txt"))
        .stdout(predicate::str::contains("Found 1 old files."))
        .stdout(predicate::str::not(predicate::str::contains("large_old.txt")));

    Ok(())
}

#[test]
fn test_invalid_path() -> Result<(), Box<dyn std::error::Error>> {
    Command::cargo_bin("nightly-chrono-scrub")?
        .arg("-p")
        .arg("/nonexistent/path/12345")
        .assert()
        .failure()
        .stderr(predicate::str::contains("Error: Path '/nonexistent/path/12345' does not exist."));
    Ok(())
}

// Helper function to set file modification time
fn set_file_mtime(path: &std::path::Path, datetime: DateTime<Utc>) -> std::io::Result<()> {
    let system_time = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(datetime.timestamp() as u64);
    filetime::set_file_mtime(path, filetime::FileTime::from_system_time(system_time))
}
