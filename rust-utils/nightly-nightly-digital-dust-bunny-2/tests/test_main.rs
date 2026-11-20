use super::*;
use tempfile::tempdir;
use std::{fs, io::Write, thread, time::Duration};

// Mock rationale: Using `tempfile` allows creating a temporary, isolated file system
// for tests, making them deterministic and offline without relying on the actual
// user's file system or external resources. This effectively "mocks" the file system
// interactions within a controlled environment.

// Helper function to capture stdout
fn run_app_and_capture_output(args: Args) -> Result<String, Box<dyn std::error::Error>> {
    let original_stdout = std::io::stdout();
    let (pipe_read, mut pipe_write) = os_pipe::pipe()?;
    let _ = std::io::set_stdout(pipe_write.try_clone().unwrap());

    let result = std::panic::catch_unwind(move || {
        super::run_app(args)
    });

    drop(pipe_write); // Close the write end to signal EOF to the read end
    let _ = std::io::set_stdout(original_stdout);

    let mut buffer = String::new();
    std::io::read_to_string(pipe_read, &mut buffer)?;

    match result {
        Ok(r) => r.map(|_| buffer),
        Err(e) => Err(format!("Application panicked: {:?}", e).into()),
    }
}

#[test]
fn test_no_flags_no_output() {
    let dir = tempdir().unwrap();
    let path = dir.path().to_path_buf();

    // Create a dummy file to ensure scan runs
    fs::write(path.join("dummy.txt"), "content").unwrap();

    let args = Args {
        path: path.clone(),
        age: 0, // Age 0 means report all files as old
        duplicates: false, // No duplicate checking
    };
    let output = run_app_and_capture_output(args).unwrap();

    assert!(output.contains(&format!("Scanning '{}'", path.display())));
    assert!(output.contains("Scan complete."));
    assert!(output.contains("[OLD]   ")); // Should report dummy.txt as old due to age=0
    assert!(!output.contains("Duplicate Files Found:"));
    assert!(!output.contains("No duplicate files found.")); // Because --duplicates was not set
}

#[test]
fn test_age_filter_positive_age_no_old_files() {
    let dir = tempdir().unwrap();
    let path = dir.path().to_path_buf();

    // Create a recent file
    let recent_file_path = path.join("recent_document.txt");
    fs::write(&recent_file_path, "This is a recent document.").unwrap();

    // Test with age = 1 (meaning older than 1 day). File is recent, so should not be reported as [OLD].
    let args = Args {
        path: path.clone(),
        age: 1,
        duplicates: false,
    };
    let output = run_app_and_capture_output(args).unwrap();

    assert!(output.contains(&format!("Scanning '{}'", path.display())));
    assert!(output.contains("Scan complete."));
    assert!(!output.contains("[OLD]")); // Should not report as old with age > 0 for a recent file
}

#[test]
fn test_age_detection_all_files_with_age_zero() {
    let dir = tempdir().unwrap();
    let path = dir.path().to_path_buf();

    let file1_path = path.join("file1.txt");
    fs::write(&file1_path, "content1").unwrap();

    let file2_path = path.join("file2.txt");
    fs::write(&file2_path, "content2").unwrap();

    // Test with --age 0 (should report both as old)
    let args = Args {
        path: path.clone(),
        age: 0,
        duplicates: false,
    };
    let output = run_app_and_capture_output(args).unwrap();

    assert!(output.contains(&format!("[OLD]   {}", file1_path.display())));
    assert!(output.contains(&format!("[OLD]   {}", file2_path.display())));
}

#[test]
fn test_duplicate_detection() {
    let dir = tempdir().unwrap();
    let path = dir.path().to_path_buf();

    let content = "duplicate content";
    let unique_content = "unique content";

    let file1_path = path.join("file_a.txt");
    fs::write(&file1_path, content).unwrap();

    let file2_path = path.join("file_b.txt");
    fs::write(&file2_path, content).unwrap();

    let file3_path = path.join("file_c.txt");
    fs::write(&file3_path, unique_content).unwrap();

    let args = Args {
        path: path.clone(),
        age: 0, // No age filtering, but still reports all as old
        duplicates: true,
    };
    let output = run_app_and_capture_output(args).unwrap();

    assert!(output.contains("Duplicate Files Found:"));
    assert!(output.contains(&format!("    - {}", file1_path.display())));
    assert!(output.contains(&format!("    - {}", file2_path.display())));
    assert!(!output.contains(&format!("    - {}", file3_path.display()))); // Unique file should not be listed as duplicate
    assert!(!output.contains("No duplicate files found."));
}

#[test]
fn test_mixed_detection() {
    let dir = tempdir().unwrap();
    let path = dir.path().to_path_buf();

    let old_duplicate_content = "old duplicate";
    let old_unique_content = "old unique";
    let recent_content = "recent content";

    // Old duplicate files
    let old_dup1_path = path.join("old_dup1.txt");
    fs::write(&old_dup1_path, old_duplicate_content).unwrap();
    thread::sleep(Duration::from_millis(100));

    let old_dup2_path = path.join("old_dup2.txt");
    fs::write(&old_dup2_path, old_duplicate_content).unwrap();
    thread::sleep(Duration::from_millis(100));

    // Old unique file
    let old_unique_path = path.join("old_unique.txt");
    fs::write(&old_unique_path, old_unique_content).unwrap();
    thread::sleep(Duration::from_millis(100));

    // Recent file
    let recent_file_path = path.join("recent_file.txt");
    fs::write(&recent_file_path, recent_content).unwrap();

    let args = Args {
        path: path.clone(),
        age: 0, // All files should be considered old
        duplicates: true,
    };
    let output = run_app_and_capture_output(args).unwrap();

    // Check for old files (all should be reported with age=0)
    assert!(output.contains(&format!("[OLD]   {}", old_dup1_path.display())));
    assert!(output.contains(&format!("[OLD]   {}", old_dup2_path.display())));
    assert!(output.contains(&format!("[OLD]   {}", old_unique_path.display())));
    assert!(output.contains(&format!("[OLD]   {}", recent_file_path.display())));

    // Check for duplicates
    assert!(output.contains("Duplicate Files Found:"));
    assert!(output.contains(&format!("    - {}", old_dup1_path.display())));
    assert!(output.contains(&format!("    - {}", old_dup2_path.display())));
    assert!(!output.contains(&format!("    - {}", old_unique_path.display())));
    assert!(!output.contains(&format!("    - {}", recent_file_path.display())));
}
