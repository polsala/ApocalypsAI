use nightly_digital_dust_bunny_sweeper::{run_app, Args}; // Import from the crate root
use tempfile::{tempdir, NamedTempFile};
use std::fs;
use std::path::{Path, PathBuf};
use std::io::{self, Write};
use std::error::Error;

// Mock rationale: For testing file system operations, `tempfile` is used to create isolated,
// temporary directories and files. This avoids modifying the actual file system and ensures
// tests are deterministic and offline. File modification times are implicitly handled by
// creating files at different points in time during the test, or by relying on the system's
// default behavior for newly created files. We cannot reliably set arbitrary past modification
// times for files using standard Rust library functions across all OSes, so we simulate "old"
// by creating files early in the test and "new" by creating them just before the scan.
// For `older_than: 0`, any file created before the scan is considered "old".

#[test]
fn test_dry_run_lists_old_files() -> Result<(), Box<dyn Error>> {
    let temp_dir = tempdir()?;
    let scan_path = temp_dir.path().to_path_buf();
    let archive_path = temp_dir.path().join("archive");

    // Create an old file (will be considered old with older_than: 0)
    let old_file_path = scan_path.join("old_bunny.txt");
    fs::write(&old_file_path, "old content")?;

    // Create another file (also old with older_than: 0)
    let another_old_file_path = scan_path.join("another_old_bunny.txt");
    fs::write(&another_old_file_path, "more old content")?;

    let args = Args {
        path: scan_path.clone(),
        older_than: 0, // All files created before scan are "old"
        archive_to: Some(archive_path.clone()),
        dry_run: true,
    };

    // Capture stdout
    let mut output = Vec::new();
    let original_stdout = io::stdout();
    let mut writer = io::Cursor::new(&mut output);
    io::set_stdout(Box::new(&mut writer))?; // Redirect stdout

    let result = run_app(args);

    io::set_stdout(original_stdout)?; // Restore stdout

    assert!(result.is_ok());
    let output_str = String::from_utf8(output)?;

    println!("Test Output:\n{}", output_str);

    assert!(output_str.contains("Found dust bunny:"));
    assert!(output_str.contains(&format!("{}", old_file_path.display())));
    assert!(output_str.contains(&format!("{}", another_old_file_path.display())));
    assert!(output_str.contains("(Dry run, not moving)"));
    assert!(!archive_path.exists()); // Archive dir should not be created if dry run and no actual move

    Ok(())
}

#[test]
fn test_archive_moves_old_files() -> Result<(), Box<dyn Error>> {
    let temp_dir = tempdir()?;
    let scan_path = temp_dir.path().to_path_buf();
    let archive_path = temp_dir.path().join("archive");

    // Create an old file
    let old_file_path = scan_path.join("old_bunny_to_move.txt");
    fs::write(&old_file_path, "old content")?;

    // Create another old file
    let another_old_file_path = scan_path.join("another_old_bunny_to_move.txt");
    fs::write(&another_old_file_path, "more old content")?;

    let args = Args {
        path: scan_path.clone(),
        older_than: 0, // All files created before scan are "old"
        archive_to: Some(archive_path.clone()),
        dry_run: false,
    };

    let result = run_app(args);
    assert!(result.is_ok());

    // Verify files were moved
    assert!(!old_file_path.exists());
    assert!(archive_path.join("old_bunny_to_move.txt").exists());

    assert!(!another_old_file_path.exists());
    assert!(archive_path.join("another_old_bunny_to_move.txt").exists());

    Ok(())
}

#[test]
fn test_no_archive_dir_specified_does_not_move() -> Result<(), Box<dyn Error>> {
    let temp_dir = tempdir()?;
    let scan_path = temp_dir.path().to_path_buf();

    let old_file_path = scan_path.join("old_bunny_no_move.txt");
    fs::write(&old_file_path, "old content")?;

    let args = Args {
        path: scan_path.clone(),
        older_than: 0,
        archive_to: None, // No archive directory
        dry_run: false,
    };

    let result = run_app(args);
    assert!(result.is_ok());

    // File should still exist in original location
    assert!(old_file_path.exists());

    // Capture stdout to ensure the message is printed
    let mut output = Vec::new();
    let original_stdout = io::stdout();
    let mut writer = io::Cursor::new(&mut output);
    io::set_stdout(Box::new(&mut writer))?; // Redirect stdout

    let result_check_output = run_app(args); // Re-run to capture output
    io::set_stdout(original_stdout)?; // Restore stdout
    assert!(result_check_output.is_ok());
    let output_str = String::from_utf8(output)?;
    assert!(output_str.contains("(No archive directory specified, skipping move)"));

    Ok(())
}

#[test]
fn test_invalid_path_error() -> Result<(), Box<dyn Error>> {
    let non_existent_path = PathBuf::from("/this/path/does/not/exist/definitely");

    let args = Args {
        path: non_existent_path.clone(),
        older_than: 1,
        archive_to: None,
        dry_run: true,
    };

    let result = run_app(args);
    assert!(result.is_err());
    let error_msg = result.unwrap_err().to_string();
    assert!(error_msg.contains(&format!("Path '{}' does not exist.", non_existent_path.display())));

    Ok(())
}

#[test]
fn test_path_is_file_error() -> Result<(), Box<dyn Error>> {
    let temp_file = NamedTempFile::new()?;
    let file_path = temp_file.path().to_path_buf();

    let args = Args {
        path: file_path.clone(),
        older_than: 1,
        archive_to: None,
        dry_run: true,
    };

    let result = run_app(args);
    assert!(result.is_err());
    let error_msg = result.unwrap_err().to_string();
    assert!(error_msg.contains(&format!("Path '{}' is not a directory.", file_path.display())));

    Ok(())
}
