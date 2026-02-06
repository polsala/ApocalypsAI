use super::{find_dust_bunnies, parse_age_string, parse_size_string, DustBunny};
use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use std::time::SystemTime;
use chrono::Duration as ChronoDuration;
use tempfile::tempdir; // For creating temporary directories

// Mock rationale: These tests create temporary files and directories
// to simulate a file system without interacting with the actual user's
// file system, ensuring determinism and isolation. File modification
// times are explicitly set for predictable age calculations.

#[test]
fn test_parse_size_string() {
    assert_eq!(parse_size_string("100"), Some(100));
    assert_eq!(parse_size_string("10KB"), Some(10 * 1024));
    assert_eq!(parse_size_string("1MB"), Some(1 * 1024 * 1024));
    assert_eq!(parse_size_string("2.5GB"), Some((2.5 * 1024.0 * 1024.0 * 1024.0) as u64));
    assert_eq!(parse_size_string("5tB"), Some((5.0 * 1024.0 * 1024.0 * 1024.0 * 1024.0) as u64));
    assert_eq!(parse_size_string("invalid"), None);
}

#[test]
fn test_parse_age_string() {
    assert_eq!(parse_age_string("10d"), Some(ChronoDuration::days(10)));
    assert_eq!(parse_age_string("2w"), Some(ChronoDuration::weeks(2)));
    assert_eq!(parse_age_string("1m"), Some(ChronoDuration::days(30))); // Approx month
    assert_eq!(parse_age_string("1y"), Some(ChronoDuration::days(365))); // Approx year
    assert_eq!(parse_age_string("invalid"), None);
    assert_eq!(parse_age_string("5"), Some(ChronoDuration::days(5))); // Default to days
}

#[test]
fn test_find_dust_bunnies_no_match() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let root_path = dir.path().to_path_buf();

    // Create a small, recent file
    let file_path = root_path.join("small_recent.txt");
    File::create(&file_path)?.write_all(b"hello")?;
    // Set modified time to now
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(SystemTime::now()))?;

    let min_size = 10 * 1024 * 1024; // 10MB
    let min_age = ChronoDuration::days(30);

    let bunnies = find_dust_bunnies(&root_path, min_size, min_age);
    assert!(bunnies.is_empty());

    Ok(())
}

#[test]
fn test_find_dust_bunnies_match_size_but_not_age() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let root_path = dir.path().to_path_buf();

    // Create a large, recent file
    let file_path = root_path.join("large_recent.txt");
    let mut file = File::create(&file_path)?;
    file.write_all(&vec![0; 15 * 1024 * 1024])?; // 15MB
    // Set modified time to now
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(SystemTime::now()))?;

    let min_size = 10 * 1024 * 1024; // 10MB
    let min_age = ChronoDuration::days(30);

    let bunnies = find_dust_bunnies(&root_path, min_size, min_age);
    // Should not match because it's recent
    assert!(bunnies.is_empty());

    Ok(())
}

#[test]
fn test_find_dust_bunnies_match_age_but_not_size() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let root_path = dir.path().to_path_buf();

    // Create a small, old file
    let file_path = root_path.join("small_old.txt");
    File::create(&file_path)?.write_all(b"hello")?;
    // Set modified time to 60 days ago
    let old_time = SystemTime::now() - std::time::Duration::from_secs(ChronoDuration::days(60).num_seconds() as u64);
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(old_time))?;

    let min_size = 10 * 1024 * 1024; // 10MB
    let min_age = ChronoDuration::days(30);

    let bunnies = find_dust_bunnies(&root_path, min_size, min_age);
    // Should not match because it's small
    assert!(bunnies.is_empty());

    Ok(())
}

#[test]
fn test_find_dust_bunnies_match_both() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let root_path = dir.path().to_path_buf();

    // Create a large, old file
    let file_path = root_path.join("large_old.txt");
    let mut file = File::create(&file_path)?;
    file.write_all(&vec![0; 15 * 1024 * 1024])?; // 15MB
    // Set modified time to 60 days ago
    let old_time = SystemTime::now() - std::time::Duration::from_secs(ChronoDuration::days(60).num_seconds() as u64);
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(old_time))?;

    let min_size = 10 * 1024 * 1024; // 10MB
    let min_age = ChronoDuration::days(30);

    let bunnies = find_dust_bunnies(&root_path, min_size, min_age);
    assert_eq!(bunnies.len(), 1);
    assert_eq!(bunnies[0].path, file_path);
    assert_eq!(bunnies[0].size, 15 * 1024 * 1024);
    assert!(bunnies[0].age_days >= 30); // Should be around 60 days

    Ok(())
}

#[test]
fn test_find_dust_bunnies_multiple_matches() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let root_path = dir.path().to_path_buf();

    // Create first match
    let file1_path = root_path.join("bunny1.log");
    let mut file1 = File::create(&file1_path)?;
    file1.write_all(&vec![0; 20 * 1024 * 1024])?; // 20MB
    let old_time1 = SystemTime::now() - std::time::Duration::from_secs(ChronoDuration::days(90).num_seconds() as u64);
    filetime::set_file_mtime(&file1_path, filetime::FileTime::from_system_time(old_time1))?;

    // Create second match in a subdirectory
    fs::create_dir_all(root_path.join("subdir"))?;
    let file2_path = root_path.join("subdir").join("bunny2.data");
    let mut file2 = File::create(&file2_path)?;
    file2.write_all(&vec![0; 12 * 1024 * 1024])?; // 12MB
    let old_time2 = SystemTime::now() - std::time::Duration::from_secs(ChronoDuration::days(45).num_seconds() as u64);
    filetime::set_file_mtime(&file2_path, filetime::FileTime::from_system_time(old_time2))?;

    // Create a non-matching file
    let file3_path = root_path.join("recent_small.txt");
    File::create(&file3_path)?.write_all(b"small")?;
    filetime::set_file_mtime(&file3_path, filetime::FileTime::from_system_time(SystemTime::now()))?;

    let min_size = 10 * 1024 * 1024; // 10MB
    let min_age = ChronoDuration::days(30);

    let bunnies = find_dust_bunnies(&root_path, min_size, min_age);
    assert_eq!(bunnies.len(), 2);

    let paths: Vec<PathBuf> = bunnies.into_iter().map(|b| b.path).collect();
    assert!(paths.contains(&file1_path));
    assert!(paths.contains(&file2_path));

    Ok(())
}

#[test]
fn test_find_dust_bunnies_directory_ignored() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let root_path = dir.path().to_path_buf();

    // Create a subdirectory
    let subdir_path = root_path.join("a_big_old_dir");
    fs::create_dir_all(&subdir_path)?;
    // Set modified time to 60 days ago
    let old_time = SystemTime::now() - std::time::Duration::from_secs(ChronoDuration::days(60).num_seconds() as u64);
    filetime::set_file_mtime(&subdir_path, filetime::FileTime::from_system_time(old_time))?;

    let min_size = 10 * 1024 * 1024; // 10MB
    let min_age = ChronoDuration::days(30);

    let bunnies = find_dust_bunnies(&root_path, min_size, min_age);
    // Directories should be ignored, even if they meet age criteria (size is not directly applicable to directories in this tool)
    assert!(bunnies.is_empty());

    Ok(())
}
