use assert_cmd::prelude::*;
use predicates::prelude::*;
use std::process::Command;
use std::fs;
use std::io::Write;
use tempfile::tempdir;
use filetime::{set_file_times, FileTime};
use chrono::{Utc, Duration};

// Mock rationale: The `filetime` crate is used to deterministically set file modification and creation times.
// This allows simulating various temporal drift scenarios without relying on actual system clock changes
// or real-world filesystem events, making tests reproducible and offline.

#[test]
fn test_no_anomalies() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("normal_file.txt");
    fs::write(&file_path, "hello")?;

    let mut cmd = Command::cargo_bin("nightly-temporal-drift-detect")?;
    cmd.arg(dir.path());

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Scanning for temporal drifts"))
        .stdout(predicate::str::does_not_contain("Temporal Anomaly Detected"));

    Ok(())
}

#[test]
fn test_future_mtime_anomaly() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("future_file.txt");
    fs::write(&file_path, "future content")?;

    let future_time = Utc::now() + Duration::days(1);
    let future_filetime = FileTime::from_unix_timestamp(future_time.timestamp(), 0);

    // Set mtime to future, ctime to now
    set_file_times(&file_path, FileTime::now(), future_filetime)?;

    let mut cmd = Command::cargo_bin("nightly-temporal-drift-detect")?;
    cmd.arg(dir.path());

    cmd.assert()
        .success()
        .stdout(predicate::str::contains(
            format!("Temporal Anomaly Detected: \"{}\" - mtime is in the future", file_path.display())
        ));

    Ok(())
}

#[test]
fn test_mtime_older_than_ctime_anomaly() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("past_mtime_file.txt");
    fs::write(&file_path, "past content")?;

    let past_mtime = Utc::now() - Duration::days(365);
    let recent_ctime = Utc::now() - Duration::hours(1);

    let past_filetime = FileTime::from_unix_timestamp(past_mtime.timestamp(), 0);
    let recent_filetime = FileTime::from_unix_timestamp(recent_ctime.timestamp(), 0);

    // Set mtime to past, ctime to recent
    set_file_times(&file_path, recent_filetime, past_filetime)?;

    let mut cmd = Command::cargo_bin("nightly-temporal-drift-detect")?;
    cmd.arg(dir.path());

    cmd.assert()
        .success()
        .stdout(predicate::str::contains(
            format!("Temporal Anomaly Detected: \"{}\" - mtime", file_path.display())
        ))
        .stdout(predicate::str::contains("is older than ctime"));

    Ok(())
}

#[test]
fn test_future_mtime_with_threshold() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("slightly_future_file.txt");
    fs::write(&file_path, "slightly future content")?;

    // Set mtime 1 second in the future
    let future_time = Utc::now() + Duration::seconds(1);
    let future_filetime = FileTime::from_unix_timestamp(future_time.timestamp(), 0);
    set_file_times(&file_path, FileTime::now(), future_filetime)?;

    let mut cmd = Command::cargo_bin("nightly-temporal-drift-detect")?;
    cmd.arg(dir.path()).arg("--future-threshold").arg("2"); // Threshold of 2 seconds

    cmd.assert()
        .success()
        .stdout(predicate::str::does_not_contain("Temporal Anomaly Detected"));

    Ok(())
}

#[test]
fn test_future_mtime_above_threshold() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("very_future_file.txt");
    fs::write(&file_path, "very future content")?;

    // Set mtime 3 seconds in the future
    let future_time = Utc::now() + Duration::seconds(3);
    let future_filetime = FileTime::from_unix_timestamp(future_time.timestamp(), 0);
    set_file_times(&file_path, FileTime::now(), future_filetime)?;

    let mut cmd = Command::cargo_bin("nightly-temporal-drift-detect")?;
    cmd.arg(dir.path()).arg("--future-threshold").arg("2"); // Threshold of 2 seconds

    cmd.assert()
        .success()
        .stdout(predicate::str::contains(
            format!("Temporal Anomaly Detected: \"{}\" - mtime is in the future", file_path.display())
        ));

    Ok(())
}

#[test]
fn test_verbose_output() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("verbose_file.txt");
    fs::write(&file_path, "verbose content")?;

    let mut cmd = Command::cargo_bin("nightly-temporal-drift-detect")?;
    cmd.arg(dir.path()).arg("-v");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains(
            format!("Scanning file: {}", file_path.display())
        ));

    Ok(())
}

#[test]
fn test_subdir_scan() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let subdir = dir.path().join("subdir");
    fs::create_dir(&subdir)?;
    let file_path = subdir.join("subdir_file.txt");
    fs::write(&file_path, "subdir content")?;

    let future_time = Utc::now() + Duration::days(1);
    let future_filetime = FileTime::from_unix_timestamp(future_time.timestamp(), 0);
    set_file_times(&file_path, FileTime::now(), future_filetime)?;

    let mut cmd = Command::cargo_bin("nightly-temporal-drift-detect")?;
    cmd.arg(dir.path());

    cmd.assert()
        .success()
        .stdout(predicate::str::contains(
            format!("Temporal Anomaly Detected: \"{}\" - mtime is in the future", file_path.display())
        ));

    Ok(())
}
