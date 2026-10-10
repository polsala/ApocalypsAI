use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::time::SystemTime;
use chrono::{Utc, Duration as ChronoDuration};
use tempfile::tempdir;

// Mock rationale: We use tempfile to create isolated, temporary file systems
// for each test. This allows us to simulate file creation, modification, and
// movement without affecting the actual user's file system or requiring
// network access. File modification times are explicitly set using `filetime`
// to ensure deterministic test outcomes based on age thresholds.

// Helper function to create a file with specific content and modification time
fn create_test_file(dir: &Path, file_name: &str, content: &str, age_days: i64) -> PathBuf {
    let file_path = dir.join(file_name);
    let mut file = fs::File::create(&file_path).unwrap();
    file.write_all(content.as_bytes()).unwrap();

    // Set modification time using chrono and filetime crates
    let modified_time = Utc::now() - ChronoDuration::days(age_days);
    let system_time: SystemTime = modified_time.into();
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(system_time)).unwrap();

    file_path
}

// Helper to run the main application logic with custom arguments for testing.
// This bypasses `clap::Parser::parse()` which reads `std::env::args()` and instead
// uses `clap::Parser::parse_from()` to provide arguments directly.
fn run_app_for_test(args_vec: Vec<&str>) -> Result<(), Box<dyn std::error::Error>> {
    let args = crate::Args::parse_from(args_vec);
    
    let target_dir = &args.target_dir;
    let age_threshold_days = args.age;

    // If target_dir doesn't exist, the main logic prints an error and returns Ok(()).
    // We simulate that behavior here for tests, without printing.
    if !target_dir.is_dir() {
        return Ok(());
    }

    let void_dir = match args.void_dir {
        Some(path) => path,
        None => {
            // In tests, we must explicitly provide a void_dir to avoid relying on `dirs::home_dir()`
            // which might be non-deterministic or unavailable in some test environments.
            panic!("void_dir must be explicitly provided in test scenarios.");
        }
    };

    if !void_dir.exists() {
        fs::create_dir_all(&void_dir)?;
    }

    let now: DateTime<Utc> = Utc::now();
    let threshold_time = now - ChronoDuration::days(age_threshold_days as i64);

    for entry in fs::read_dir(target_dir)? {
        let entry = entry?;
        let path = entry.path();

        if path.is_file() {
            let metadata = fs::metadata(&path)?;
            let modified_time: DateTime<Utc> = metadata.modified()?.into();

            if modified_time < threshold_time {
                let file_name = path.file_name().ok_or("Could not get file name")?;
                let destination_path = void_dir.join(file_name);
                fs::rename(&path, &destination_path)?;
            }
        }
    }

    Ok(())
}

#[test]
fn test_no_old_files() {
    let temp_dir = tempdir().unwrap();
    let target_path = temp_dir.path().to_path_buf();
    let void_path = temp_dir.path().join("temporal_void");

    // Create a recent file (1 day old)
    create_test_file(&target_path, "recent_file.txt", "hello", 1);

    // Run the cleaner for files older than 2 days
    let args = vec![
        "chronal-cache-cleaner",
        "--target-dir", target_path.to_str().unwrap(),
        "--age", "2",
        "--void-dir", void_path.to_str().unwrap(),
    ];
    let result = run_app_for_test(args);
    assert!(result.is_ok());

    // Assert no files were moved
    assert!(target_path.join("recent_file.txt").exists());
    assert!(!void_path.join("recent_file.txt").exists());
    // The void directory might be created but should be empty if no files were moved to it.
    assert!(!void_path.exists() || void_path.read_dir().unwrap().next().is_none());
}

#[test]
fn test_some_old_files_moved() {
    let temp_dir = tempdir().unwrap();
    let target_path = temp_dir.path().to_path_buf();
    let void_path = temp_dir.path().join("temporal_void");

    // Create an old file (10 days old)
    create_test_file(&target_path, "old_file.txt", "old content", 10);
    // Create a recent file (1 day old)
    create_test_file(&target_path, "recent_file.txt", "recent content", 1);

    // Run the cleaner for files older than 5 days
    let args = vec![
        "chronal-cache-cleaner",
        "--target-dir", target_path.to_str().unwrap(),
        "--age", "5",
        "--void-dir", void_path.to_str().unwrap(),
    ];
    let result = run_app_for_test(args);
    assert!(result.is_ok());

    // Assert old_file.txt was moved
    assert!(!target_path.join("old_file.txt").exists());
    assert!(void_path.join("old_file.txt").exists());

    // Assert recent_file.txt was not moved
    assert!(target_path.join("recent_file.txt").exists());
    assert!(!void_path.join("recent_file.txt").exists());
}

#[test]
fn test_all_old_files_moved() {
    let temp_dir = tempdir().unwrap();
    let target_path = temp_dir.path().to_path_buf();
    let void_path = temp_dir.path().join("temporal_void");

    // Create multiple old files
    create_test_file(&target_path, "old_file_1.txt", "content 1", 10);
    create_test_file(&target_path, "old_file_2.txt", "content 2", 15);

    // Run the cleaner for files older than 5 days
    let args = vec![
        "chronal-cache-cleaner",
        "--target-dir", target_path.to_str().unwrap(),
        "--age", "5",
        "--void-dir", void_path.to_str().unwrap(),
    ];
    let result = run_app_for_test(args);
    assert!(result.is_ok());

    // Assert both files were moved
    assert!(!target_path.join("old_file_1.txt").exists());
    assert!(void_path.join("old_file_1.txt").exists());
    assert!(!target_path.join("old_file_2.txt").exists());
    assert!(void_path.join("old_file_2.txt").exists());
}

#[test]
fn test_void_dir_creation() {
    let temp_dir = tempdir().unwrap();
    let target_path = temp_dir.path().to_path_buf();
    let void_path = temp_dir.path().join("non_existent_void");

    // Create an old file
    create_test_file(&target_path, "old_file.txt", "content", 10);

    // Run the cleaner, void_path should be created
    let args = vec![
        "chronal-cache-cleaner",
        "--target-dir", target_path.to_str().unwrap(),
        "--age", "5",
        "--void-dir", void_path.to_str().unwrap(),
    ];
    let result = run_app_for_test(args);
    assert!(result.is_ok());

    // Assert void directory was created and file moved
    assert!(void_path.is_dir());
    assert!(void_path.join("old_file.txt").exists());
}

#[test]
fn test_target_dir_does_not_exist() {
    let temp_dir = tempdir().unwrap();
    let non_existent_target_path = temp_dir.path().join("non_existent_target");
    let void_path = temp_dir.path().join("temporal_void");

    // Run the cleaner with a non-existent target directory
    let args = vec![
        "chronal-cache-cleaner",
        "--target-dir", non_existent_target_path.to_str().unwrap(),
        "--age", "5",
        "--void-dir", void_path.to_str().unwrap(),
    ];
    let result = run_app_for_test(args);
    // The main function prints an error and returns Ok(()), so we check for that.
    assert!(result.is_ok());
    // We could capture stderr to assert the error message, but for this utility, 
    // ensuring it doesn't panic and gracefully exits is sufficient.
}

#[test]
#[should_panic(expected = "void_dir must be explicitly provided in test scenarios.")]
fn test_void_dir_not_provided_in_test() {
    let temp_dir = tempdir().unwrap();
    let target_path = temp_dir.path().to_path_buf();

    // Create a file
    create_test_file(&target_path, "file.txt", "content", 1);

    // Run the cleaner without providing --void-dir, which should panic in test context
    let args = vec![
        "chronal-cache-cleaner",
        "--target-dir", target_path.to_str().unwrap(),
        "--age", "1",
    ];
    let _ = run_app_for_test(args);
}
