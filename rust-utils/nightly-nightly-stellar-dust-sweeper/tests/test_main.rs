use super::*;
use std::io::Cursor;
use tempfile::tempdir;
use filetime::{set_file_times, FileTime};
use std::fs::{self, File};
use std::time::{SystemTime, UNIX_EPOCH};

// Mock rationale: We use `tempfile` to create an isolated, temporary filesystem
// environment for our tests. This ensures that tests are deterministic,
// do not affect the actual filesystem, and run offline without external dependencies.
// `filetime` is used to precisely control file modification times, which is crucial
// for testing the age-based filtering logic. `std::io::Cursor` is used to capture
// stdout, making the CLI output testable without actual console interaction.

#[test]
fn test_finds_old_files_only() -> io::Result<()> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    // Create an old file (e.g., 100 days old)
    let old_file_path = path.join("old_file.txt");
    File::create(&old_file_path)?;
    let old_time = SystemTime::now() - std::time::Duration::from_days(100);
    set_file_times(&old_file_path, FileTime::from_system_time(old_time), FileTime::from_system_time(old_time))?;

    // Create a new file (e.g., 10 days old)
    let new_file_path = path.join("new_file.txt");
    File::create(&new_file_path)?;
    let new_time = SystemTime::now() - std::time::Duration::from_days(10);
    set_file_times(&new_file_path, FileTime::from_system_time(new_time), FileTime::from_system_time(new_time))?;

    // Create a subdirectory with another old file
    let subdir_path = path.join("subdir");
    fs::create_dir(&subdir_path)?;
    let another_old_file_path = subdir_path.join("another_old_file.log");
    File::create(&another_old_file_path)?;
    set_file_times(&another_old_file_path, FileTime::from_system_time(old_time), FileTime::from_system_time(old_time))?;

    let args = Args {
        path: path.to_path_buf(),
        days: Some(90), // Threshold: 90 days
        months: None,
        years: None,
        sort_by: "age".to_string(),
        reverse: false,
    };

    let mut output_buffer = Vec::new();
    run_app_and_print(args, &mut output_buffer)?;
    let output = String::from_utf8(output_buffer).unwrap();

    // Assertions
    assert!(output.contains(old_file_path.to_str().unwrap()));
    assert!(output.contains(another_old_file_path.to_str().unwrap()));
    assert!(!output.contains(new_file_path.to_str().unwrap()));
    assert!(output.contains("Stellar Dust Report"));
    assert!(output.contains("Consider sweeping these files away"));

    Ok(())
}

#[test]
fn test_no_dust_found() -> io::Result<()> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    // Create a new file (e.g., 10 days old)
    let new_file_path = path.join("new_file.txt");
    File::create(&new_file_path)?;
    let new_time = SystemTime::now() - std::time::Duration::from_days(10);
    set_file_times(&new_file_path, FileTime::from_system_time(new_time), FileTime::from_system_time(new_time))?;

    let args = Args {
        path: path.to_path_buf(),
        days: Some(90), // Threshold: 90 days
        months: None,
        years: None,
        sort_by: "age".to_string(),
        reverse: false,
    };

    let mut output_buffer = Vec::new();
    run_app_and_print(args, &mut output_buffer)?;
    let output = String::from_utf8(output_buffer).unwrap();

    // Assertions
    assert!(!output.contains(new_file_path.to_str().unwrap()));
    assert!(output.contains("No stellar dust found"));

    Ok(())
}

#[test]
fn test_sort_by_size() -> io::Result<()> {
    let temp_dir = tempdir()?;
    let path = temp_dir.path();

    let old_time = SystemTime::now() - std::time::Duration::from_days(100);

    // Create file A (smaller)
    let file_a_path = path.join("file_a.txt");
    fs::write(&file_a_path, "small content")?; // 13 bytes
    set_file_times(&file_a_path, FileTime::from_system_time(old_time), FileTime::from_system_time(old_time))?;

    // Create file B (larger)
    let file_b_path = path.join("file_b.txt");
    fs::write(&file_b_path, "much larger content that spans multiple bytes")?; // 46 bytes
    set_file_times(&file_b_path, FileTime::from_system_time(old_time), FileTime::from_system_time(old_time))?;

    let args = Args {
        path: path.to_path_buf(),
        days: Some(90),
        months: None,
        years: None,
        sort_by: "size".to_string(),
        reverse: false,
    };

    let mut output_buffer = Vec::new();
    run_app_and_print(args, &mut output_buffer)?;
    let output = String::from_utf8(output_buffer).unwrap();

    // Expect file_a before file_b if not reversed (smaller first)
    let pos_a = output.find(file_a_path.to_str().unwrap()).unwrap();
    let pos_b = output.find(file_b_path.to_str().unwrap()).unwrap();
    assert!(pos_a < pos_b, "File A should come before File B when sorting by size (ascending)");

    // Test reverse sort
    let args_reverse = Args {
        path: path.to_path_buf(),
        days: Some(90),
        months: None,
        years: None,
        sort_by: "size".to_string(),
        reverse: true,
    };
    let mut output_buffer_reverse = Vec::new();
    run_app_and_print(args_reverse, &mut output_buffer_reverse)?;
    let output_reverse = String::from_utf8(output_buffer_reverse).unwrap();

    // Expect file_b before file_a if reversed (larger first)
    let pos_a_rev = output_reverse.find(file_a_path.to_str().unwrap()).unwrap();
    let pos_b_rev = output_reverse.find(file_b_path.to_str().unwrap()).unwrap();
    assert!(pos_b_rev < pos_a_rev, "File B should come before File A when sorting by size (descending)");

    Ok(())
}
