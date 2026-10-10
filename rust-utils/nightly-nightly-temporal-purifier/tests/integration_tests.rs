use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;
use std::fs::{self, File};
use std::io::Write;
use std::path::Path;
use filetime::{set_file_mtime, FileTime};
use chrono::{Utc, Duration};

// Mock rationale: We use `tempfile` to create isolated, temporary directories
// and `filetime` to precisely control file modification times. This ensures
// tests are deterministic, self-contained, and do not interact with the actual
// filesystem outside the temporary test environment. `assert_cmd` allows
// running the compiled binary and asserting its output and exit status offline.

#[test]
fn test_dry_run_lists_old_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create files with specific modification times
    let now = Utc::now();
    let old_file_path = path.join("old_log.txt");
    let new_file_path = path.join("new_data.bin");
    let subdir_path = path.join("subdir");
    fs::create_dir(&subdir_path)?;
    let another_old_file_path = subdir_path.join("another_old.tmp");

    File::create(&old_file_path)?.write_all(b"old content")?;
    File::create(&new_file_path)?.write_all(b"new content")?;
    File::create(&another_old_file_path)?.write_all(b"subdir old content")?;

    // Set modification times
    set_file_mtime(&old_file_path, FileTime::from_system_time((now - Duration::days(2)).into()))?;
    set_file_mtime(&new_file_path, FileTime::from_system_time((now - Duration::hours(1)).into()))?;
    set_file_mtime(&another_old_file_path, FileTime::from_system_time((now - Duration::days(3)).into()))?;

    // Test with a 1-day duration threshold (should list old_log.txt and another_old.tmp)
    Command::cargo_bin("nightly-temporal-purifier")?
        .arg(path.to_str().unwrap())
        .arg("--duration")
        .arg("1d")
        .assert()
        .success()
        .stdout(predicate::str::contains("[DRY-RUN] Would purge").count(2))
        .stdout(predicate::str::contains(old_file_path.to_str().unwrap()))
        .stdout(predicate::str::contains(another_old_file_path.to_str().unwrap()))
        .stdout(predicate::str::contains(new_file_path.to_str().unwrap()).not())
        .stdout(predicate::str::contains("Identified 2 files for potential purging."));

    Ok(())
}

#[test]
fn test_delete_removes_old_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let now = Utc::now();
    let old_file_path = path.join("to_delete.txt");
    let new_file_path = path.join("keep_me.log");
    let subdir_path = path.join("nested");
    fs::create_dir(&subdir_path)?;
    let another_old_file_path = subdir_path.join("nested_old.data");

    File::create(&old_file_path)?.write_all(b"delete this")?;
    File::create(&new_file_path)?.write_all(b"keep this")?;
    File::create(&another_old_file_path)?.write_all(b"delete this too")?;

    set_file_mtime(&old_file_path, FileTime::from_system_time((now - Duration::days(5)).into()))?;
    set_file_mtime(&new_file_path, FileTime::from_system_time((now - Duration::minutes(30)).into()))?;
    set_file_mtime(&another_old_file_path, FileTime::from_system_time((now - Duration::days(10)).into()))?;

    // Test with a 1-day duration threshold and --delete flag
    Command::cargo_bin("nightly-temporal-purifier")?
        .arg(path.to_str().unwrap())
        .arg("--duration")
        .arg("1d")
        .arg("--delete")
        .assert()
        .success()
        .stdout(predicate::str::contains("[PURGED]").count(2))
        .stdout(predicate::str::contains(old_file_path.to_str().unwrap()))
        .stdout(predicate::str::contains(another_old_file_path.to_str().unwrap()))
        .stdout(predicate::str::contains(new_file_path.to_str().unwrap()).not())
        .stdout(predicate::str::contains("Purged 2 files."));

    // Assert files are actually gone
    assert!(!old_file_path.exists());
    assert!(!another_old_file_path.exists());
    assert!(new_file_path.exists());

    Ok(())
}

#[test]
fn test_no_files_purged_if_too_new() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let now = Utc::now();
    let file_path = path.join("recent.txt");
    File::create(&file_path)?.write_all(b"recent content")?;
    set_file_mtime(&file_path, FileTime::from_system_time((now - Duration::hours(1)).into()))?;

    // Test with a 2-hour duration threshold (file is only 1 hour old)
    Command::cargo_bin("nightly-temporal-purifier")?
        .arg(path.to_str().unwrap())
        .arg("--duration")
        .arg("2h")
        .assert()
        .success()
        .stdout(predicate::str::contains("[DRY-RUN]").not())
        .stdout(predicate::str::contains("Identified 0 files for potential purging."));

    Ok(())
}

#[test]
fn test_invalid_duration_format() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    Command::cargo_bin("nightly-temporal-purifier")?
        .arg(path.to_str().unwrap())
        .arg("--duration")
        .arg("invalid")
        .assert()
        .failure()
        .stderr(predicate::str::contains("Invalid duration format: invalid"));

    Command::cargo_bin("nightly-temporal-purifier")?
        .arg(path.to_str().unwrap())
        .arg("--duration")
        .arg("10x") // Unknown unit
        .assert()
        .failure()
        .stderr(predicate::str::contains("Unknown duration unit: x"));

    Ok(())
}

#[test]
fn test_empty_directory() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    Command::cargo_bin("nightly-temporal-purifier")?
        .arg(path.to_str().unwrap())
        .arg("--duration")
        .arg("1d")
        .assert()
        .success()
        .stdout(predicate::str::contains("Identified 0 files for potential purging."));

    Ok(())
}

#[test]
fn test_path_does_not_exist() -> Result<(), Box<dyn std::error::Error>> {
    let non_existent_path = Path::new("/non/existent/path/for/test");

    Command::cargo_bin("nightly-temporal-purifier")?
        .arg(non_existent_path.to_str().unwrap())
        .arg("--duration")
        .arg("1d")
        .assert()
        .failure()
        .stderr(predicate::str::contains("No such file or directory")); // walkdir error message

    Ok(())
}
