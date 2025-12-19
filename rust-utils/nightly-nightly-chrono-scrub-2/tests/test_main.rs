use assert_cmd::prelude::*;
use predicates::prelude::*;
use std::process::Command;
use tempfile::tempdir;
use std::fs;
use std::time::{SystemTime, UNIX_EPOCH};
use filetime::{set_file_times, FileTime};
use chrono::{Utc, Duration};

// Mock rationale: These tests create a temporary directory and manipulate file timestamps
// using the `filetime` crate. This ensures deterministic and offline testing without
// relying on the actual system's file state or real-time clock, which can vary.

#[test]
fn test_no_anomalies() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("normal_file.txt");
    fs::write(&file_path, "content")?;

    Command::cargo_bin("chrono-scrub")?
        .arg(dir.path())
        .assert()
        .success()
        .stdout(predicate::str::is_empty()); // No output expected for no anomalies

    Ok(())
}

#[test]
fn test_stale_file_detection() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("stale_file.txt");
    fs::write(&file_path, "content")?;

    // Set modified time to 100 days ago
    let past_time = Utc::now() - Duration::days(100);
    let ft = FileTime::from_system_time(SystemTime::from(past_time));
    set_file_times(&file_path, ft, ft)?;

    Command::cargo_bin("chrono-scrub")?
        .arg(dir.path())
        .arg("--stale-days")
        .arg("90")
        .assert()
        .success()
        .stdout(predicate::str::contains("Stale").and(predicate::str::contains("stale_file.txt")));

    Ok(())
}

#[test]
fn test_future_dated_file_detection() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("future_file.txt");
    fs::write(&file_path, "content")?;

    // Set modified time to 5 minutes in the future
    let future_time = Utc::now() + Duration::minutes(5);
    let ft = FileTime::from_system_time(SystemTime::from(future_time));
    set_file_times(&file_path, ft, ft)?;

    Command::cargo_bin("chrono-scrub")?
        .arg(dir.path())
        .arg("--future-tolerance")
        .arg("60") // 60 seconds tolerance
        .assert()
        .success()
        .stdout(predicate::str::contains("Future-dated").and(predicate::str::contains("future_file.txt")));

    Ok(())
}

#[test]
fn test_inconsistent_timestamps_detection() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("inconsistent_file.txt");
    fs::write(&file_path, "content")?;

    // Set creation time to now, then modification time to 1 hour ago
    let now_sys = SystemTime::now();
    let past_sys = now_sys - std::time::Duration::from_secs(3600);

    let ft_created = FileTime::from_system_time(now_sys);
    let ft_modified = FileTime::from_system_time(past_sys);

    // Note: set_file_times takes atime, mtime. We need to set ctime separately if possible
    // or rely on the OS's default ctime behavior and then set mtime.
    // For robust testing of mtime < ctime, we'll set mtime to a past value
    // and assume ctime is set by file creation to 'now' or later than mtime.
    // A more direct way would be to use platform-specific APIs for ctime.
    // For this test, we'll create the file, then set its mtime to be older than its ctime (which is usually creation time).

    // Create file, ctime will be ~now
    let initial_metadata = fs::metadata(&file_path)?;
    let initial_ctime = initial_metadata.created().unwrap_or(UNIX_EPOCH);

    // Set mtime to be significantly before initial_ctime
    let very_past_time = initial_ctime - std::time::Duration::from_secs(7200); // 2 hours before creation
    let ft_mtime_past = FileTime::from_system_time(very_past_time);
    set_file_times(&file_path, FileTime::from_system_time(initial_ctime), ft_mtime_past)?;

    Command::cargo_bin("chrono-scrub")?
        .arg(dir.path())
        .arg("--inconsistent")
        .assert()
        .success()
        .stdout(predicate::str::contains("Inconsistent").and(predicate::str::contains("inconsistent_file.txt")));

    Ok(())
}

#[test]
fn test_multiple_anomalies_verbose() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("multi_anomaly_file.txt");
    fs::write(&file_path, "content")?;

    // Set modified time to 100 days ago (stale)
    let stale_time = Utc::now() - Duration::days(100);
    // Set creation time to 5 minutes in the future (future-dated)
    let future_time = Utc::now() + Duration::minutes(5);

    let ft_stale = FileTime::from_system_time(SystemTime::from(stale_time));
    let ft_future = FileTime::from_system_time(SystemTime::from(future_time));

    // Set mtime to stale_time, atime to future_time (to influence ctime if possible, though ctime is tricky)
    // For this test, we'll set mtime to be stale, and then try to make ctime appear future-dated.
    // The `filetime` crate primarily controls atime and mtime. ctime is often set by OS on creation.
    // To simulate mtime < ctime, we'll create the file, then set mtime to be older than its creation time.

    // Create file, ctime will be ~now
    let initial_metadata = fs::metadata(&file_path)?;
    let initial_ctime = initial_metadata.created().unwrap_or(UNIX_EPOCH);

    // Set mtime to be stale (older than 90 days) AND older than ctime (inconsistent)
    let very_past_mtime = initial_ctime - std::time::Duration::from_secs(3600 * 24 * 100); // 100 days before ctime
    let ft_very_past_mtime = FileTime::from_system_time(very_past_mtime);

    // Set atime to be in the future (future-dated)
    let future_atime = Utc::now() + Duration::minutes(10);
    let ft_future_atime = FileTime::from_system_time(SystemTime::from(future_atime));

    set_file_times(&file_path, ft_future_atime, ft_very_past_mtime)?;

    Command::cargo_bin("chrono-scrub")?
        .arg(dir.path())
        .arg("--stale-days")
        .arg("90")
        .arg("--future-tolerance")
        .arg("60")
        .arg("--inconsistent")
        .arg("-v")
        .assert()
        .success()
        .stdout(predicate::str::contains("multi_anomaly_file.txt")
            .and(predicate::str::contains("Stale"))
            .and(predicate::str::contains("Future-dated")) // This will likely come from atime if ctime isn't directly settable
            .and(predicate::str::contains("Inconsistent")));

    Ok(())
}

#[test]
fn test_path_argument() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let subdir = dir.path().join("subdir");
    fs::create_dir(&subdir)?;
    let file_path = subdir.join("file_in_subdir.txt");
    fs::write(&file_path, "content")?;

    // Set modified time to 100 days ago
    let past_time = Utc::now() - Duration::days(100);
    let ft = FileTime::from_system_time(SystemTime::from(past_time));
    set_file_times(&file_path, ft, ft)?;

    Command::cargo_bin("chrono-scrub")?
        .arg(&subdir) // Scan only the subdir
        .arg("--stale-days")
        .arg("90")
        .assert()
        .success()
        .stdout(predicate::str::contains("Stale").and(predicate::str::contains("file_in_subdir.txt")));

    Ok(())
}
