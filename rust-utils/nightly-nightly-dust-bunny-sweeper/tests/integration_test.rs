use nightly_dust_bunny_sweeper::{run_sweeper, Args};
use std::io::Write;
use tempfile::tempdir;
use chrono::{Utc, Duration};
use std::fs;

// Mock rationale: We create a temporary directory and populate it with files
// having specific modification times to simulate a filesystem state. This ensures
// tests are deterministic, isolated, and do not affect the actual filesystem.

#[test]
fn test_finds_old_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path().to_path_buf();

    // Create a file older than 90 days
    let old_file_path = path.join("old_bunny.txt");
    let mut old_file = fs::File::create(&old_file_path)?;
    old_file.write_all(b"old content")?;
    // Set modification time to 100 days ago
    let old_time = Utc::now() - Duration::days(100);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(old_time.into()))?;

    // Create a file newer than 90 days
    let new_file_path = path.join("new_bunny.txt");
    let mut new_file = fs::File::create(&new_file_path)?;
    new_file.write_all(b"new content")?;
    // Modification time is now, which is recent

    // Create a directory, should be ignored by file sweeper
    let sub_dir_path = path.join("sub_dir");
    fs::create_dir(&sub_dir_path)?;

    // Capture stdout
    let mut buffer = Vec::new();
    let _guard = gag::BufferRedirect::stdout(&mut buffer)?;

    // Simulate CLI arguments
    let args = Args {
        path: path.clone(),
        age_days: 90,
        dry_run: true,
    };

    // Run the sweeper logic
    run_sweeper(args)?;

    let output = String::from_utf8(buffer)?;

    // Assert that the old file is reported
    assert!(output.contains(&old_file_path.display().to_string()));
    // Assert that the new file is NOT reported
    assert!(!output.contains(&new_file_path.display().to_string()));
    // Assert that the summary indicates one dust bunny found
    assert!(output.contains("Found 1 digital dust bunnies."));

    Ok(())
}

#[test]
fn test_no_old_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path().to_path_buf();

    // Create a file newer than 90 days
    let new_file_path = path.join("new_bunny.txt");
    let mut new_file = fs::File::create(&new_file_path)?;
    new_file.write_all(b"new content")?;
    // Modification time is now, which is recent

    // Capture stdout
    let mut buffer = Vec::new();
    let _guard = gag::BufferRedirect::stdout(&mut buffer)?;

    let args = Args {
        path: path.clone(),
        age_days: 90,
        dry_run: true,
    };

    run_sweeper(args)?;

    let output = String::from_utf8(buffer)?;

    // Assert that no files are reported
    assert!(!output.contains(&new_file_path.display().to_string()));
    // Assert that the summary indicates no dust bunnies found
    assert!(output.contains("No digital dust bunnies found!"));

    Ok(())
}

#[test]
fn test_different_age_threshold() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path().to_path_buf();

    // Create a file 40 days old
    let mid_age_file_path = path.join("mid_age_bunny.txt");
    let mut mid_age_file = fs::File::create(&mid_age_file_path)?;
    mid_age_file.write_all(b"mid age content")?;
    let mid_time = Utc::now() - Duration::days(40);
    filetime::set_file_mtime(&mid_age_file_path, filetime::FileTime::from_system_time(mid_time.into()))?;

    // Capture stdout
    let mut buffer = Vec::new();
    let _guard = gag::BufferRedirect::stdout(&mut buffer)?;

    // Test with age_days = 30 (should find the 40-day-old file)
    let args_30 = Args {
        path: path.clone(),
        age_days: 30,
        dry_run: true,
    };
    run_sweeper(args_30)?;
    let output_30 = String::from_utf8(buffer.drain(..).collect())?;
    assert!(output_30.contains(&mid_age_file_path.display().to_string()));
    assert!(output_30.contains("Found 1 digital dust bunnies."));

    // Test with age_days = 50 (should NOT find the 40-day-old file)
    let args_50 = Args {
        path: path.clone(),
        age_days: 50,
        dry_run: true,
    };
    run_sweeper(args_50)?;
    let output_50 = String::from_utf8(buffer.drain(..).collect())?;
    assert!(!output_50.contains(&mid_age_file_path.display().to_string()));
    assert!(output_50.contains("No digital dust bunnies found!"));

    Ok(())
}
