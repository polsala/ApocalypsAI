use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;
use std::fs::{self, File};
use std::io::Write;
use std::path::Path;
use std::time::{SystemTime, Duration};
use chrono::{Utc, Duration as ChronoDuration};

// Mock rationale: We need to create a controlled file system environment
// with specific file sizes, modification times, and directory structures
// to deterministically test the utility's logic. `tempfile` allows us to
// create and clean up these environments reliably without affecting the
// actual file system or relying on external resources.

#[test]
fn test_no_debris_found() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    // Create a recent, large file
    let mut file = File::create(path.join("recent_large.txt"))?;
    file.write_all(&vec![0; 2048])?;

    // Create a recent, non-empty directory
    fs::create_dir(path.join("recent_dir"))?;
    File::create(path.join("recent_dir/file.txt"))?;

    let mut cmd = Command::cargo_bin("nightly-digital-debris-collector")?;
    cmd.arg(path).arg("--age").arg("1").arg("--size").arg("100"); // Very strict criteria

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("No digital debris found"));

    Ok(())
}

#[test]
fn test_old_file_debris() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    let old_file_path = path.join("old_log.txt");
    File::create(&old_file_path)?;

    // Set modification time to 2 years ago
    let two_years_ago = SystemTime::now() - Duration::from_secs(2 * 365 * 24 * 60 * 60);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(two_years_ago))?;

    let mut cmd = Command::cargo_bin("nightly-digital-debris-collector")?;
    cmd.arg(path).arg("--age").arg("365").arg("--size").arg("100");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("old_log.txt"))
        .stdout(predicate::str::contains("Older than 365 days"));

    Ok(())
}

#[test]
fn test_small_file_debris() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    let small_file_path = path.join("tiny_config.cfg");
    let mut file = File::create(&small_file_path)?;
    file.write_all(b"small content")?;

    let mut cmd = Command::cargo_bin("nightly-digital-debris-collector")?;
    cmd.arg(path).arg("--age").arg("365").arg("--size").arg("20"); // File is ~13 bytes

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("tiny_config.cfg"))
        .stdout(predicate::str::contains("Smaller than 20 bytes"));

    Ok(())
}

#[test]
fn test_empty_directory_debris() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    fs::create_dir(path.join("empty_folder"))?;

    let mut cmd = Command::cargo_bin("nightly-digital-debris-collector")?;
    cmd.arg(path).arg("--empty-dirs");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("empty_folder"))
        .stdout(predicate::str::contains("Is empty"));

    Ok(())
}

#[test]
fn test_json_output() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    // Create an old file
    let old_file_path = path.join("json_old_file.txt");
    File::create(&old_file_path)?;
    let two_years_ago = SystemTime::now() - Duration::from_secs(2 * 365 * 24 * 60 * 60);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(two_years_ago))?;

    // Create a small file
    let small_file_path = path.join("json_small_file.txt");
    let mut file = File::create(&small_file_path)?;
    file.write_all(b"tiny")?;

    // Create an empty directory
    fs::create_dir(path.join("json_empty_dir"))?;

    let mut cmd = Command::cargo_bin("nightly-digital-debris-collector")?;
    cmd.arg(path)
        .arg("--json")
        .arg("--age").arg("365")
        .arg("--size").arg("10") // 'tiny' is 4 bytes
        .arg("--empty-dirs");

    let output = cmd.assert().success().stdout(predicate::str::is_json()).get_output().stdout.clone();
    let json_str = String::from_utf8(output)?;
    let items: Vec<serde_json::Value> = serde_json::from_str(&json_str)?;

    assert_eq!(items.len(), 3);

    // Check old file
    let old_file_item = items.iter().find(|item| item["path"].as_str().unwrap().contains("json_old_file.txt")).unwrap();
    assert_eq!(old_file_item["reason"], "older_than_age");
    assert!(old_file_item["details"]["age_days"].as_u64().unwrap() >= 365);

    // Check small file
    let small_file_item = items.iter().find(|item| item["path"].as_str().unwrap().contains("json_small_file.txt")).unwrap();
    assert_eq!(small_file_item["reason"], "smaller_than_size");
    assert_eq!(small_file_item["details"]["size_bytes"], 4);

    // Check empty directory
    let empty_dir_item = items.iter().find(|item| item["path"].as_str().unwrap().contains("json_empty_dir")).unwrap();
    assert_eq!(empty_dir_item["reason"], "is_empty");

    Ok(())
}

#[test]
fn test_path_not_found() -> Result<(), Box<dyn std::error::Error>> {
    let mut cmd = Command::cargo_bin("nightly-digital-debris-collector")?;
    cmd.arg("/non/existent/path/to/nowhere");

    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("Error: Path '/non/existent/path/to/nowhere' does not exist."));

    Ok(())
}

#[test]
fn test_verbose_output() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    let mut cmd = Command::cargo_bin("nightly-digital-debris-collector")?;
    cmd.arg(path).arg("-v").arg("--age").arg("1").arg("--size").arg("100");

    cmd.assert()
        .success()
        .stderr(predicate::str::contains("Scanning for byte-dust"))
        .stderr(predicate::str::contains("Age threshold: 1 days"));

    Ok(())
}
