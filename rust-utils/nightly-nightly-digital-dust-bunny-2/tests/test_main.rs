use super::{Args, run_sweeper_logic}; // Import the necessary items from the parent module
use std::fs;
use std::io::Write;
use tempfile::tempdir;
use chrono::Duration;
use std::time::SystemTime;

// Mock rationale: We create a temporary directory and populate it with files
// whose modification times are explicitly set. This allows for deterministic
// testing of the `run_sweeper_logic` function's ability to identify and
// optionally delete files based on their age, without interacting with the
// actual file system outside the test's control. The `gag` crate is used
// to capture stdout for asserting output messages.

#[test]
fn test_dry_run_finds_old_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a file older than 30 days
    let old_file_path = path.join("old_log.txt");
    {
        let mut file = fs::File::create(&old_file_path)?;
        file.write_all(b"old content")?;
    }
    // Set modification time to 60 days ago
    let sixty_days_ago = SystemTime::now() - Duration::days(60).to_std()?;
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(sixty_days_ago))?;

    // Create a file newer than 30 days
    let new_file_path = path.join("new_report.txt");
    {
        let mut file = fs::File::create(&new_file_path)?;
        file.write_all(b"new content")?;
    }
    // Set modification time to 10 days ago
    let ten_days_ago = SystemTime::now() - Duration::days(10).to_std()?;
    filetime::set_file_mtime(&new_file_path, filetime::FileTime::from_system_time(ten_days_ago))?;

    // Capture stdout
    let mut buffer: Vec<u8> = Vec::new();
    let _guard = gag::BufferRedirect::stdout(&mut buffer)?;

    let args = Args {
        path: path.to_path_buf(),
        age_days: 30,
        dry_run: true,
        delete: false,
    };

    let found_count = run_sweeper_logic(&args)?;

    let output = String::from_utf8_lossy(&buffer);

    assert_eq!(found_count, 1);
    assert!(output.contains(&format!("Found dust bunny: {}", old_file_path.display())));
    assert!(!output.contains(&format!("Found dust bunny: {}", new_file_path.display())));
    assert!(old_file_path.exists()); // Should still exist in dry run

    Ok(())
}

#[test]
fn test_delete_removes_old_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a file older than 30 days
    let old_file_path = path.join("old_data.bak");
    {
        let mut file = fs::File::create(&old_file_path)?;
        file.write_all(b"old backup data")?;
    }
    let sixty_days_ago = SystemTime::now() - Duration::days(60).to_std()?;
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(sixty_days_ago))?;

    // Create a file newer than 30 days
    let new_file_path = path.join("current_config.toml");
    {
        let mut file = fs::File::create(&new_file_path)?;
        file.write_all(b"current config")?;
    }
    let ten_days_ago = SystemTime::now() - Duration::days(10).to_std()?;
    filetime::set_file_mtime(&new_file_path, filetime::FileTime::from_system_time(ten_days_ago))?;

    // Capture stdout
    let mut buffer: Vec<u8> = Vec::new();
    let _guard = gag::BufferRedirect::stdout(&mut buffer)?;

    let args = Args {
        path: path.to_path_buf(),
        age_days: 30,
        dry_run: false,
        delete: true,
    };

    let found_count = run_sweeper_logic(&args)?;

    let output = String::from_utf8_lossy(&buffer);

    assert_eq!(found_count, 1);
    assert!(output.contains(&format!("Found dust bunny: {}", old_file_path.display())));
    assert!(output.contains("-> Swept away!"));
    assert!(!output.contains(&format!("Found dust bunny: {}", new_file_path.display())));

    assert!(!old_file_path.exists()); // Should be deleted
    assert!(new_file_path.exists()); // Should still exist

    Ok(())
}

#[test]
fn test_no_old_files_found() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a file newer than 30 days
    let new_file_path = path.join("recent_doc.md");
    {
        let mut file = fs::File::create(&new_file_path)?;
        file.write_all(b"recent content")?;
    }
    let five_days_ago = SystemTime::now() - Duration::days(5).to_std()?;
    filetime::set_file_mtime(&new_file_path, filetime::FileTime::from_system_time(five_days_ago))?;

    // Capture stdout
    let mut buffer: Vec<u8> = Vec::new();
    let _guard = gag::BufferRedirect::stdout(&mut buffer)?;

    let args = Args {
        path: path.to_path_buf(),
        age_days: 30,
        dry_run: true,
        delete: false,
    };

    let found_count = run_sweeper_logic(&args)?;

    let output = String::from_utf8_lossy(&buffer);

    assert_eq!(found_count, 0);
    assert!(!output.contains("Found dust bunny:"));
    assert!(new_file_path.exists());

    Ok(())
}
