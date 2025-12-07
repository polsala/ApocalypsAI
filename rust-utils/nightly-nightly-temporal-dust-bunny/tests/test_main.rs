use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;
use std::fs::{self, File};
use std::path::Path;
use std::time::{SystemTime, Duration};
use filetime::{set_file_times, FileTime};

// Mock rationale: We create a controlled temporary file system with specific,
// predetermined access and modification times using `tempfile` and `filetime`
// to ensure tests are deterministic and do not depend on the actual system's
// current time or existing file states. This allows for reliable and repeatable testing.

// Helper trait to add `from_days` to `std::time::Duration` for test setup
trait DurationExt {
    fn from_days(days: u64) -> Self;
}

impl DurationExt for Duration {
    fn from_days(days: u64) -> Self {
        Duration::from_secs(days * 24 * 60 * 60)
    }
}

#[test]
fn test_no_dust_bunnies() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    let recent_file = path.join("recent_file.txt");
    File::create(&recent_file)?;

    // Set file times to be very recent (1 second ago to ensure it's < now)
    let now = SystemTime::now();
    let recent_time = now - Duration::from_secs(1);
    let recent_ft = FileTime::from_system_time(recent_time);
    set_file_times(&recent_file, recent_ft, recent_ft)?;

    let mut cmd = Command::cargo_bin("nightly-temporal-dust-bunny-sweeper")?;
    cmd.arg("-p").arg(path).arg("-a").arg("90"); // 90 days age

    cmd.assert()
        .success()
        .stdout(predicates::str::contains("Found 0 temporal dust bunnies."));

    Ok(())
}

#[test]
fn test_some_dust_bunnies() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    // Create a recent file
    let recent_file = path.join("recent_file.txt");
    File::create(&recent_file)?;
    let now = SystemTime::now();
    let recent_time = now - Duration::from_secs(1);
    let recent_ft = FileTime::from_system_time(recent_time);
    set_file_times(&recent_file, recent_ft, recent_ft)?;

    // Create an old file (dust bunny)
    let old_file = path.join("old_file.txt");
    File::create(&old_file)?;
    let old_time = now - Duration::from_days(100); // 100 days ago
    let old_ft = FileTime::from_system_time(old_time);
    set_file_times(&old_file, old_ft, old_ft)?;

    let mut cmd = Command::cargo_bin("nightly-temporal-dust-bunny-sweeper")?;
    cmd.arg("-p").arg(path).arg("-a").arg("90"); // 90 days age

    cmd.assert()
        .success()
        .stdout(predicates::str::contains(old_file.display().to_string()))
        .stdout(predicates::str::contains("Found 1 temporal dust bunnies."));

    Ok(())
}

#[test]
fn test_dust_bunnies_in_subdir() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    let subdir = path.join("subdir");
    fs::create_dir(&subdir)?;

    // Create an old file in subdir
    let old_file_subdir = subdir.join("another_old_file.txt");
    File::create(&old_file_subdir)?;
    let now = SystemTime::now();
    let old_time = now - Duration::from_days(100); // 100 days ago
    let old_ft = FileTime::from_system_time(old_time);
    set_file_times(&old_file_subdir, old_ft, old_ft)?;

    let mut cmd = Command::cargo_bin("nightly-temporal-dust-bunny-sweeper")?;
    cmd.arg("-p").arg(path).arg("-a").arg("90"); // 90 days age

    cmd.assert()
        .success()
        .stdout(predicates::str::contains(old_file_subdir.display().to_string()))
        .stdout(predicates::str::contains("Found 1 temporal dust bunnies."));

    Ok(())
}

#[test]
fn test_age_zero_finds_all_files() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    let file1 = path.join("file1.txt");
    File::create(&file1)?;
    let file2 = path.join("file2.txt");
    File::create(&file2)?;

    // Set times to be slightly in the past to ensure they are < SystemTime::now()
    let now = SystemTime::now();
    let slightly_past = now - Duration::from_secs(1);
    let slightly_past_ft = FileTime::from_system_time(slightly_past);
    set_file_times(&file1, slightly_past_ft, slightly_past_ft)?;
    set_file_times(&file2, slightly_past_ft, slightly_past_ft)?;

    let mut cmd = Command::cargo_bin("nightly-temporal-dust-bunny-sweeper")?;
    cmd.arg("-p").arg(path).arg("-a").arg("0"); // 0 days age

    cmd.assert()
        .success()
        .stdout(predicates::str::contains(file1.display().to_string()))
        .stdout(predicates::str::contains(file2.display().to_string()))
        .stdout(predicates::str::contains("Found 2 temporal dust bunnies."));

    Ok(())
}

#[test]
fn test_only_modified_old_not_a_dust_bunny() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    let file = path.join("file_modified_old_accessed_recent.txt");
    File::create(&file)?;

    let now = SystemTime::now();
    let old_time = now - Duration::from_days(100);
    let recent_time = now - Duration::from_secs(1);

    // Modified old, accessed recent
    set_file_times(&file, FileTime::from_system_time(old_time), FileTime::from_system_time(recent_time))?;

    let mut cmd = Command::cargo_bin("nightly-temporal-dust-bunny-sweeper")?;
    cmd.arg("-p").arg(path).arg("-a").arg("90"); // 90 days age

    cmd.assert()
        .success()
        .stdout(predicates::str::contains("Found 0 temporal dust bunnies."));

    Ok(())
}

#[test]
fn test_only_accessed_old_not_a_dust_bunny() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    let file = path.join("file_accessed_old_modified_recent.txt");
    File::create(&file)?;

    let now = SystemTime::now();
    let old_time = now - Duration::from_days(100);
    let recent_time = now - Duration::from_secs(1);

    // Accessed old, modified recent
    set_file_times(&file, FileTime::from_system_time(recent_time), FileTime::from_system_time(old_time))?;

    let mut cmd = Command::cargo_bin("nightly-temporal-dust-bunny-sweeper")?;
    cmd.arg("-p").arg(path).arg("-a").arg("90"); // 90 days age

    cmd.assert()
        .success()
        .stdout(predicates::str::contains("Found 0 temporal dust bunnies."));

    Ok(())
}
