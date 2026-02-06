use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;
use std::fs::{self, File};
use std::io::Write;
use std::time::{SystemTime, UNIX_EPOCH};
use chrono::{Utc, Duration};

// Mock rationale: We create a temporary directory and populate it with files
// of specific ages and sizes to ensure deterministic testing. This avoids
// relying on the actual filesystem state, which would make tests non-deterministic.

#[test]
fn test_no_dust_bunnies_found() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a new, small file
    let new_file_path = path.join("new_small_file.txt");
    File::create(&new_file_path)?.write_all(b"hello")?;

    // Create an old, small file (should not match size threshold)
    let old_small_file_path = path.join("old_small_file.txt");
    File::create(&old_small_file_path)?.write_all(b"old_data")?;
    let two_years_ago = Utc::now() - Duration::days(730);
    let system_time_two_years_ago = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(two_years_ago.timestamp() as u64);
    filetime::set_file_mtime(&old_small_file_path, filetime::FileTime::from_system_time(system_time_two_years_ago))?;

    let mut cmd = Command::cargo_bin("nightly-digital-dust-duster")?;
    cmd.arg("--path").arg(path)
       .arg("--age").arg("30") // 30 days
       .arg("--size").arg("100"); // 100 bytes

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("No digital dust bunnies found"));

    Ok(())
}

#[test]
fn test_dust_bunnies_found() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create an old, large file (should be found)
    let old_large_file_path = path.join("dusty_relic.log");
    let mut file = File::create(&old_large_file_path)?;
    file.write_all(&vec![0; 200])?; // 200 bytes
    let two_years_ago = Utc::now() - Duration::days(730);
    let system_time_two_years_ago = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(two_years_ago.timestamp() as u64);
    filetime::set_file_mtime(&old_large_file_path, filetime::FileTime::from_system_time(system_time_two_years_ago))?;

    // Create a new, large file (should not be found by age)
    let new_large_file_path = path.join("fresh_data.bin");
    File::create(&new_large_file_path)?.write_all(&vec![0; 300])?;

    let mut cmd = Command::cargo_bin("nightly-digital-dust-duster")?;
    cmd.arg("--path").arg(path)
       .arg("--age").arg("30") // 30 days
       .arg("--size").arg("100"); // 100 bytes

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Found 1 digital dust bunnies:"))
        .stdout(predicate::str::contains("dusty_relic.log"))
        .stdout(predicate::str::contains("Size: 200 bytes"));

    Ok(())
}

#[test]
fn test_json_output() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create an old, large file (should be found)
    let old_large_file_path = path.join("json_dusty_relic.log");
    let mut file = File::create(&old_large_file_path)?;
    file.write_all(&vec![0; 200])?; // 200 bytes
    let two_years_ago = Utc::now() - Duration::days(730);
    let system_time_two_years_ago = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(two_years_ago.timestamp() as u64);
    filetime::set_file_mtime(&old_large_file_path, filetime::FileTime::from_system_time(system_time_two_years_ago))?;

    let mut cmd = Command::cargo_bin("nightly-digital-dust-duster")?;
    cmd.arg("--path").arg(path)
       .arg("--age").arg("30") // 30 days
       .arg("--size").arg("100") // 100 bytes
       .arg("--format").arg("json");

    let output = cmd.assert().success().stdout(predicate::str::is_json()).get_output().stdout.clone();
    let json_str = String::from_utf8(output)?;
    let json_val: serde_json::Value = serde_json::from_str(&json_str)?;

    assert!(json_val.as_array().is_some());
    assert_eq!(json_val.as_array().unwrap().len(), 1);
    let bunny = &json_val.as_array().unwrap()[0];
    assert!(bunny["path"].as_str().unwrap().contains("json_dusty_relic.log"));
    assert_eq!(bunny["size_bytes"].as_u64().unwrap(), 200);
    assert!(bunny["age_days"].as_i64().unwrap() >= 730); // At least 2 years old

    Ok(())
}

#[test]
fn test_dry_run_output() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let old_large_file_path = path.join("dry_run_relic.log");
    let mut file = File::create(&old_large_file_path)?;
    file.write_all(&vec![0; 200])?; // 200 bytes
    let two_years_ago = Utc::now() - Duration::days(730);
    let system_time_two_years_ago = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(two_years_ago.timestamp() as u64);
    filetime::set_file_mtime(&old_large_file_path, filetime::FileTime::from_system_time(system_time_two_years_ago))?;

    let mut cmd = Command::cargo_bin("nightly-digital-dust-duster")?;
    cmd.arg("--path").arg(path)
       .arg("--age").arg("30")
       .arg("--size").arg("100")
       .arg("--dry-run");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("dry_run_relic.log"))
        .stdout(predicate::str::contains("Dry run: No actions suggested. Remove --dry-run for suggestions."));

    Ok(())
}

#[test]
fn test_unsupported_format() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let mut cmd = Command::cargo_bin("nightly-digital-dust-duster")?;
    cmd.arg("--path").arg(path)
       .arg("--format").arg("xml");

    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("Unsupported format: xml"));

    Ok(())
}
