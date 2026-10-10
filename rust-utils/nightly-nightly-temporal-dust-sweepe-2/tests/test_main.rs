use super::*;
use std::fs::{self, File};
use std::io::{Write, Read};
use tempfile::tempdir;
use chrono::{Utc, Duration};
use std::time::SystemTime;
use os_pipe;

// Mock rationale: We use `tempfile` to create a temporary directory and `std::fs` to
// create and manipulate files within it. This allows us to simulate a file system
// state deterministically and offline for testing purposes, without relying on
// actual user files or external network resources. We use the `filetime` crate
// (a dev-dependency) to precisely set file access and modification times, which is
// crucial for time-based file system tests and ensures determinism.

// Helper function to create a file with a specific modification and access time
fn create_file_with_time(dir: &PathBuf, filename: &str, days_ago: i64) -> PathBuf {
    let file_path = dir.join(filename);
    let mut file = File::create(&file_path).expect("Failed to create test file");
    writeln!(file, "test content").expect("Failed to write to test file");

    let past_time = Utc::now() - Duration::days(days_ago);
    let system_time: SystemTime = past_time.into();
    let file_time = filetime::FileTime::from_system_time(system_time);

    filetime::set_file_mtime(&file_path, file_time)
        .expect("Failed to set modification time");
    filetime::set_file_atime(&file_path, file_time)
        .expect("Failed to set access time");

    file_path
}

// Helper to capture stdout
fn capture_stdout<F>(f: F) -> String
where
    F: FnOnce() -> Result<(), DustSweeperError> + std::panic::UnwindSafe,
{
    let original_stdout = std::io::stdout();
    let (pipe_read, pipe_write) = os_pipe::pipe().unwrap();
    let _ = std::io::set_stdout(pipe_write).unwrap();

    let result = std::panic::catch_unwind(f);

    let _ = std::io::set_stdout(original_stdout).unwrap();
    drop(pipe_write); // Close the write end to signal EOF to the read end

    let mut output = Vec::new();
    pipe_read.read_to_end(&mut output).unwrap();
    let output_str = String::from_utf8_lossy(&output).to_string();

    assert!(result.is_ok(), "main_logic panicked: {:?}", result.err());
    output_str
}

#[test]
fn test_finds_old_files_modified() {
    let dir = tempdir().expect("Failed to create temp dir");
    let path = dir.path().to_path_buf();

    create_file_with_time(&path, "old_file.txt", 100);
    create_file_with_time(&path, "recent_file.txt", 50);
    create_file_with_time(&path, "boundary_file.txt", 90);

    let args = Args {
        path: path.clone(),
        days: 90,
        modified: true,
        verbose: false,
    };

    let output_str = capture_stdout(|| main_logic(args));

    assert!(output_str.contains("old_file.txt (100 days ago)"));
    assert!(output_str.contains("boundary_file.txt (90 days ago)"));
    assert!(!output_str.contains("recent_file.txt"));
    assert!(output_str.contains("Found 2 temporal dust bunnies."));

    dir.close().expect("Failed to close temp dir");
}

#[test]
fn test_finds_old_files_accessed() {
    let dir = tempdir().expect("Failed to create temp dir");
    let path = dir.path().to_path_buf();

    create_file_with_time(&path, "old_file_accessed.txt", 100);
    create_file_with_time(&path, "recent_file_accessed.txt", 50);

    let args = Args {
        path: path.clone(),
        days: 90,
        modified: false,
        verbose: false,
    };

    let output_str = capture_stdout(|| main_logic(args));

    assert!(output_str.contains("old_file_accessed.txt (100 days ago)"));
    assert!(!output_str.contains("recent_file_accessed.txt"));
    assert!(output_str.contains("Found 1 temporal dust bunnies."));

    dir.close().expect("Failed to close temp dir");
}

#[test]
fn test_no_files_found() {
    let dir = tempdir().expect("Failed to create temp dir");
    let path = dir.path().to_path_buf();

    create_file_with_time(&path, "recent_file_only.txt", 50);

    let args = Args {
        path: path.clone(),
        days: 90,
        modified: true,
        verbose: false,
    };

    let output_str = capture_stdout(|| main_logic(args));

    assert!(!output_str.contains("recent_file_only.txt"));
    assert!(output_str.contains("Found 0 temporal dust bunnies."));

    dir.close().expect("Failed to close temp dir");
}

#[test]
fn test_verbose_output() {
    let dir = tempdir().expect("Failed to create temp dir");
    let path = dir.path().to_path_buf();

    create_file_with_time(&path, "verbose_old_file.txt", 100);

    let args = Args {
        path: path.clone(),
        days: 90,
        modified: true,
        verbose: true,
    };

    let output_str = capture_stdout(|| main_logic(args));

    assert!(output_str.contains("Path: "));
    assert!(output_str.contains("Last touched: "));
    assert!(output_str.contains("verbose_old_file.txt (100 days ago)"));

    dir.close().expect("Failed to close temp dir");
}

#[test]
fn test_path_does_not_exist() {
    let non_existent_path = PathBuf::from("/non/existent/path_for_test");
    let args = Args {
        path: non_existent_path.clone(),
        days: 90,
        modified: false,
        verbose: false,
    };

    let result = main_logic(args);
    assert!(result.is_err());
    match result.unwrap_err() {
        DustSweeperError::PathDoesNotExist(p) => assert_eq!(p, non_existent_path),
        _ => panic!("Expected PathDoesNotExist error"),
    }
}

#[test]
fn test_path_is_not_directory() {
    let dir = tempdir().expect("Failed to create temp dir");
    let file_path = dir.path().join("a_file.txt");
    File::create(&file_path).expect("Failed to create file");

    let args = Args {
        path: file_path.clone(),
        days: 90,
        modified: false,
        verbose: false,
    };

    let result = main_logic(args);
    assert!(result.is_err());
    match result.unwrap_err() {
        DustSweeperError::PathIsNotDirectory(p) => assert_eq!(p, file_path),
        _ => panic!("Expected PathIsNotDirectory error"),
    }
    dir.close().expect("Failed to close temp dir");
}
