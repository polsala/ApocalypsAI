use nightly_chrono_cache_cleaner::find_stale_files; // Import from our lib
use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use tempfile::tempdir;
use chrono::{Utc, Duration};
use filetime::{set_file_times, FileTime};

// Mock rationale: We need to create a controlled file system environment
// to test the file scanning logic without affecting the actual system.
// `tempfile` allows us to create temporary directories and files that are
// automatically cleaned up. `filetime` allows us to precisely set access
// and modification times for deterministic testing of age-based logic.

#[test]
fn test_find_stale_files_basic() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let root_path = dir.path();

    // Create a fresh file
    let fresh_file_path = root_path.join("fresh_file.txt");
    File::create(&fresh_file_path)?.write_all(b"fresh content")?;
    // Set access time to now
    let now = Utc::now();
    set_file_times(&fresh_file_path, FileTime::from_system_time(now.into()), FileTime::from_system_time(now.into()))?;

    // Create a stale file (e.g., 100 days old)
    let stale_file_path = root_path.join("stale_file.txt");
    File::create(&stale_file_path)?.write_all(b"stale content")?;
    // Set access time to 100 days ago
    let hundred_days_ago = now - Duration::days(100);
    set_file_times(&stale_file_path, FileTime::from_system_time(hundred_days_ago.into()), FileTime::from_system_time(hundred_days_ago.into()))?;

    // Create another fresh file in a subdirectory
    fs::create_dir_all(root_path.join("subdir"))?;
    let fresh_subdir_file_path = root_path.join("subdir/fresh_subdir_file.txt");
    File::create(&fresh_subdir_file_path)?.write_all(b"fresh subdir content")?;
    set_file_times(&fresh_subdir_file_path, FileTime::from_system_time(now.into()), FileTime::from_system_time(now.into()))?;

    // Create another stale file in a subdirectory
    let stale_subdir_file_path = root_path.join("subdir/stale_subdir_file.txt");
    File::create(&stale_subdir_file_path)?.write_all(b"stale subdir content")?;
    let one_twenty_days_ago = now - Duration::days(120);
    set_file_times(&stale_subdir_file_path, FileTime::from_system_time(one_twenty_days_ago.into()), FileTime::from_system_time(one_twenty_days_ago.into()))?;

    // Run the function with a stale_days threshold of 90
    let results = find_stale_files(root_path, 90)?;

    // Assert that only the stale files are found
    assert_eq!(results.len(), 2);
    assert!(results.contains(&stale_file_path));
    assert!(results.contains(&stale_subdir_file_path));
    assert!(!results.contains(&fresh_file_path));
    assert!(!results.contains(&fresh_subdir_file_path));

    Ok(())
}

#[test]
fn test_find_stale_files_empty_dir() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let root_path = dir.path();

    let results = find_stale_files(root_path, 90)?;
    assert!(results.is_empty());

    Ok(())
}

#[test]
fn test_find_stale_files_no_stale() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let root_path = dir.path();

    let fresh_file_path = root_path.join("fresh_file.txt");
    File::create(&fresh_file_path)?.write_all(b"fresh content")?;
    let now = Utc::now();
    set_file_times(&fresh_file_path, FileTime::from_system_time(now.into()), FileTime::from_system_time(now.into()))?;

    let results = find_stale_files(root_path, 90)?;
    assert!(results.is_empty());

    Ok(())
}
