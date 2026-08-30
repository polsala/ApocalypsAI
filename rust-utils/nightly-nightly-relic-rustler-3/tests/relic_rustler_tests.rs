use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::{tempdir};
use std::fs::{self, File};
use std::io::Write;
use std::time::{SystemTime};
use chrono::{Utc, Duration, DateTime};

// Mock rationale: We create temporary files and directories to simulate a file system
// for testing. This ensures tests are deterministic and do not rely on the actual
// file system state or external resources. File modification times are explicitly
// set using the `filetime` crate to control the 'age' of test files.

#[test]
fn test_no_relics_found() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a recent file (modified now)
    let mut file = File::create(path.join("recent_file.txt"))?;
    file.write_all(b"hello")?;
    drop(file); // Close the file to ensure modification time is set

    let mut cmd = Command::cargo_bin("relic-rustler")?;
    cmd.arg(path.to_str().unwrap())
       .arg("--age")
       .arg("1"); // Look for files older than 1 day

    cmd.assert()
       .success()
       .stdout(predicate::str::contains("No relics found older than 1 days"));

    Ok(())
}

#[test]
fn test_relics_found_text_output() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a relic file (older than 90 days)
    let relic_path = path.join("old_log.log");
    let mut file = File::create(&relic_path)?;
    file.write_all(b"old log content")?;
    drop(file);

    // Manually set modification time to be old
    let old_time = Utc::now() - Duration::days(100);
    let system_time: SystemTime = old_time.into();
    filetime::set_file_mtime(&relic_path, filetime::FileTime::from_system_time(system_time))?;

    // Create a recent file
    let recent_path = path.join("recent_doc.txt");
    let mut file = File::create(&recent_path)?;
    file.write_all(b"recent doc content")?;
    drop(file);

    let mut cmd = Command::cargo_bin("relic-rustler")?;
    cmd.arg(path.to_str().unwrap())
       .arg("--age")
       .arg("90") // Look for files older than 90 days
       .arg("--output")
       .arg("text");

    cmd.assert()
       .success()
       .stdout(predicate::str::contains("--- Relic Manifest (Older than 90 days) ---"))
       .stdout(predicate::str::contains("Path: "))
       .stdout(predicate::str::contains("old_log.log"))
       .stdout(predicate::str::contains("Type: log"))
       .stdout(predicate::str::contains("100 days ago")) // Check for approximate age
       .stdout(predicate::str::not(predicate::str::contains("recent_doc.txt"))); // Ensure recent file is not listed

    Ok(())
}

#[test]
fn test_relics_found_json_output() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a relic file (older than 90 days)
    let relic_path = path.join("old_archive.zip");
    let mut file = File::create(&relic_path)?;
    file.write_all(b"old archive content")?;
    drop(file);

    let old_time = Utc::now() - Duration::days(120);
    let system_time: SystemTime = old_time.into();
    filetime::set_file_mtime(&relic_path, filetime::FileTime::from_system_time(system_time))?;

    let mut cmd = Command::cargo_bin("relic-rustler")?;
    cmd.arg(path.to_str().unwrap())
       .arg("--age")
       .arg("90")
       .arg("--output")
       .arg("json");

    cmd.assert()
       .success()
       .stdout(predicate::str::contains(format!("\"path\": \"{}"", relic_path.to_string_lossy().replace('\\', "\\"))))
       .stdout(predicate::str::contains("\"file_type\": \"zip\""))
       .stdout(predicate::str::contains("\"age_days\": 120")); // Check for exact age in JSON

    Ok(())
}

#[test]
fn test_different_age_threshold() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // File 1: 50 days old (should be a relic with --age 40, not with --age 60)
    let file_50_days_path = path.join("medium_old.data");
    let mut file = File::create(&file_50_days_path)?;
    file.write_all(b"data")?;
    drop(file);
    let old_time_50 = Utc::now() - Duration::days(50);
    filetime::set_file_mtime(&file_50_days_path, filetime::FileTime::from_system_time(old_time_50.into()))?;

    // File 2: 70 days old (should be a relic with --age 60)
    let file_70_days_path = path.join("older.bak");
    let mut file = File::create(&file_70_days_path)?;
    file.write_all(b"backup")?;
    drop(file);
    let old_time_70 = Utc::now() - Duration::days(70);
    filetime::set_file_mtime(&file_70_days_path, filetime::FileTime::from_system_time(old_time_70.into()))?;

    // Test with age 40: both should be relics
    let mut cmd_40 = Command::cargo_bin("relic-rustler")?;
    cmd_40.arg(path.to_str().unwrap())
          .arg("--age").arg("40")
          .arg("--output").arg("json");
    cmd_40.assert()
          .success()
          .stdout(predicate::str::contains(file_50_days_path.to_string_lossy().replace('\\', "\\")))
          .stdout(predicate::str::contains(file_70_days_path.to_string_lossy().replace('\\', "\\")));

    // Test with age 60: only 70-day-old file should be a relic
    let mut cmd_60 = Command::cargo_bin("relic-rustler")?;
    cmd_60.arg(path.to_str().unwrap())
          .arg("--age").arg("60")
          .arg("--output").arg("json");
    cmd_60.assert()
          .success()
          .stdout(predicate::str::not(predicate::str::contains(file_50_days_path.to_string_lossy().replace('\\', "\\"))))
          .stdout(predicate::str::contains(file_70_days_path.to_string_lossy().replace('\\', "\\")));

    Ok(())
}
