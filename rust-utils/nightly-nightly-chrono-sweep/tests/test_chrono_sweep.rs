#![allow(unused_imports)] // Allow unused imports for the `gag` crate if not actively used

use super::*;
use tempfile::tempdir;
use std::fs::{self, File};
use std::io::Write;
use chrono::{Duration, Utc};
use filetime::{set_file_mtime, FileTime};
use std::time::SystemTime;

// Mock rationale: We create temporary files and directories with specific modification times
// to simulate a file system state for testing. This ensures tests are deterministic and offline.
// For stdin confirmation, we rely on the `force` flag to bypass it in tests.

#[test]
fn test_parse_duration_string() {
    assert_eq!(parse_duration_string("30d"), Some(Duration::days(30)));
    assert_eq!(parse_duration_string("2w"), Some(Duration::weeks(2)));
    assert_eq!(parse_duration_string("1m"), Some(Duration::days(30))); // Approximation
    assert_eq!(parse_duration_string("1y"), Some(Duration::days(365))); // Approximation
    assert_eq!(parse_duration_string("5x"), None);
    assert_eq!(parse_duration_string("abc"), None);
    assert_eq!(parse_duration_string(""), None);
}

#[test]
fn test_chrono_sweep_core_dry_run() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let now = Utc::now();
    let old_time = now - Duration::days(60); // 60 days ago
    let recent_time = now - Duration::days(10); // 10 days ago

    // Create an old file
    let old_file_path = path.join("old_log.txt");
    File::create(&old_file_path)?.write_all(b"old data")?;
    set_file_mtime(&old_file_path, FileTime::from_system_time(old_time.into()))?;

    // Create a recent file
    let recent_file_path = path.join("recent_report.csv");
    File::create(&recent_file_path)?.write_all(b"recent data")?;
    set_file_mtime(&recent_file_path, FileTime::from_system_time(recent_time.into()))?;

    // Create a subdirectory with an old file
    let sub_dir = path.join("sub");
    fs::create_dir(&sub_dir)?;
    let sub_old_file_path = sub_dir.join("sub_old.tmp");
    File::create(&sub_old_file_path)?.write_all(b"sub old data")?;
    set_file_mtime(&sub_old_file_path, FileTime::from_system_time(old_time.into()))?;

    let threshold_duration = parse_duration_string("30d").unwrap();
    let cutoff_time = Utc::now() - threshold_duration;

    let identified_paths = chrono_sweep_core(
        &path.to_path_buf(),
        cutoff_time,
        true,  // dry_run
        false, // delete
        false, // force (doesn't matter for dry_run)
    )?;

    // In dry run, chrono_sweep_core returns an empty vec because it doesn't delete anything.
    // We need to check the files exist.
    assert_eq!(identified_paths.len(), 0);

    // Verify files still exist
    assert!(old_file_path.exists());
    assert!(recent_file_path.exists());
    assert!(sub_old_file_path.exists());

    Ok(())
}

#[test]
fn test_chrono_sweep_core_delete_forced() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let now = Utc::now();
    let old_time = now - Duration::days(60); // 60 days ago
    let recent_time = now - Duration::days(10); // 10 days ago

    // Create an old file
    let old_file_path = path.join("old_data.bin");
    File::create(&old_file_path)?.write_all(b"old binary data")?;
    set_file_mtime(&old_file_path, FileTime::from_system_time(old_time.into()))?;

    // Create a recent file
    let recent_file_path = path.join("new_config.json");
    File::create(&recent_file_path)?.write_all(b"{ \"key\": \"value\" }")?;
    set_file_mtime(&recent_file_path, FileTime::from_system_time(recent_time.into()))?;

    let threshold_duration = parse_duration_string("30d").unwrap();
    let cutoff_time = Utc::now() - threshold_duration;

    let deleted_paths = chrono_sweep_core(
        &path.to_path_buf(),
        cutoff_time,
        false, // dry_run
        true,  // delete
        true,  // force (skip confirmation)
    )?;

    assert_eq!(deleted_paths.len(), 1);
    assert!(deleted_paths.contains(&old_file_path));

    // Assert old file is gone, recent file remains
    assert!(!old_file_path.exists());
    assert!(recent_file_path.exists());

    Ok(())
}

#[test]
fn test_no_files_to_delete() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let now = Utc::now();
    let recent_time = now - Duration::days(10); // 10 days ago

    // Create a recent file
    let recent_file_path = path.join("new_config.json");
    File::create(&recent_file_path)?.write_all(b"{ \"key\": \"value\" }")?;
    set_file_mtime(&recent_file_path, FileTime::from_system_time(recent_time.into()))?;

    let threshold_duration = parse_duration_string("30d").unwrap();
    let cutoff_time = Utc::now() - threshold_duration;

    let deleted_paths = chrono_sweep_core(
        &path.to_path_buf(),
        cutoff_time,
        false, // dry_run
        true,  // delete
        true,  // force (skip confirmation)
    )?;

    assert!(deleted_paths.is_empty());
    assert!(recent_file_path.exists()); // Ensure it still exists

    Ok(())
}
