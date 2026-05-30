use tempfile::{tempdir, NamedTempFile};
use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};
use chrono::{Utc, Duration};

// Mock rationale: We create temporary files and directories to simulate a file system
// for testing. This ensures tests are deterministic, isolated, and do not affect
// the actual file system. It's an offline test as no network or external services are involved.

// Helper function to create a file with a specific modification time
fn create_file_with_mtime(dir: &PathBuf, filename: &str, mtime_offset_days: i64) -> PathBuf {
    let file_path = dir.join(filename);
    let mut file = File::create(&file_path).unwrap();
    writeln!(file, "test content").unwrap();

    // Set modification time
    let past_time = Utc::now() - Duration::days(mtime_offset_days);
    let system_time: SystemTime = past_time.into();
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(system_time)).unwrap();
    file_path
}

#[test]
fn test_dry_run_finds_old_files() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path().to_path_buf();

    // Create a file that should be found (older than 1 day)
    let old_log_path = create_file_with_mtime(&path, "old_log.txt", 2);
    // Create a file that should not be found (newer than 1 day)
    let new_report_path = create_file_with_mtime(&path, "new_report.txt", 0);
    // Create another old file
    let ancient_data_path = create_file_with_mtime(&path, "ancient_data.bak", 5);

    let args = crate::Args {
        path: path.clone(),
        age_days: 1,
        dry_run: true,
        delete: false,
    };

    let (found_count, _reclaimed_bytes) = crate::run_sweeper(args)?;

    assert_eq!(found_count, 2, "Should find 2 old files in dry run.");
    assert!(old_log_path.exists(), "Old log file should still exist after dry run.");
    assert!(new_report_path.exists(), "New report file should still exist after dry run.");
    assert!(ancient_data_path.exists(), "Ancient data file should still exist after dry run.");

    Ok(())
}

#[test]
fn test_delete_removes_old_files() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path().to_path_buf();

    let old_file_path = create_file_with_mtime(&path, "old_config.conf", 3);
    let new_file_path = create_file_with_mtime(&path, "current_settings.json", 0);

    let args = crate::Args {
        path: path.clone(),
        age_days: 1,
        dry_run: false,
        delete: true,
    };

    let (found_count, _reclaimed_bytes) = crate::run_sweeper(args)?;

    assert_eq!(found_count, 1, "Should delete 1 old file.");
    assert!(!old_file_path.exists(), "Old config file should be deleted.");
    assert!(new_file_path.exists(), "Current settings file should not be deleted.");

    Ok(())
}

#[test]
fn test_no_action_mode() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path().to_path_buf();

    let old_file_path = create_file_with_mtime(&path, "temp_cache.tmp", 10);
    let new_file_path = create_file_with_mtime(&path, "active_session.log", 0);

    let args = crate::Args {
        path: path.clone(),
        age_days: 5,
        dry_run: false,
        delete: false,
    };

    let (found_count, _reclaimed_bytes) = crate::run_sweeper(args)?;

    assert_eq!(found_count, 1, "Should find 1 old file.");
    assert!(old_file_path.exists(), "Old file should still exist in no-action mode.");
    assert!(new_file_path.exists(), "New file should still exist in no-action mode.");

    Ok(())
}

#[test]
fn test_invalid_path_returns_error() {
    let args = crate::Args {
        path: PathBuf::from("/non/existent/path/12345"),
        age_days: 30,
        dry_run: false,
        delete: false,
    };

    let result = crate::run_sweeper(args);
    assert!(result.is_err(), "Should return an error for a non-existent path.");
    assert!(result.unwrap_err().to_string().contains("not a directory or does not exist"));
}

#[test]
fn test_delete_and_dry_run_returns_error() {
    let temp_dir = tempdir().unwrap(); // Use unwrap for test setup that should not fail
    let path = temp_dir.path().to_path_buf();

    let args = crate::Args {
        path: path.clone(),
        age_days: 30,
        dry_run: true,
        delete: true,
    };

    let result = crate::run_sweeper(args);
    assert!(result.is_err(), "Should return an error when both --delete and --dry-run are used.");
    assert!(result.unwrap_err().to_string().contains("Cannot use --delete and --dry-run simultaneously"));
}
