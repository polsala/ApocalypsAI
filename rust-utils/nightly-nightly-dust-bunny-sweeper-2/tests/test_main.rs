#![cfg(test)]

use super::*;
use tempfile::{tempdir, NamedTempFile};
use std::io::Write;

// Mock rationale: `tempfile` is used to create isolated, temporary filesystem structures
// for testing file operations without affecting the actual system or requiring external
// resources. This ensures tests are deterministic and offline.

#[test]
fn test_is_file_old_enough() -> Result<(), String> {
    let temp_dir = tempdir().map_err(|e| format!("Tempdir error: {}", e))?;
    let file_path = temp_dir.path().join("test_file.txt");

    // Create a file and set its modification time
    let mut file = fs::File::create(&file_path).map_err(|e| format!("File create error: {}", e))?;
    file.write_all(b"hello").map_err(|e| format!("File write error: {}", e))?;

    // Test case 1: File is old enough
    let old_threshold = Utc::now() - Duration::days(10);
    // Set file modified time to be older than 10 days ago
    let ten_days_ago = Utc::now() - Duration::days(11);
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(ten_days_ago.into()))
        .map_err(|e| format!("Set mtime error: {}", e))?;
    assert!(is_file_old_enough(&file_path, old_threshold)?);

    // Test case 2: File is NOT old enough
    let new_threshold = Utc::now() - Duration::days(1);
    // Set file modified time to be newer than 1 day ago
    let now_minus_hours = Utc::now() - Duration::hours(1);
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(now_minus_hours.into()))
        .map_err(|e| format!("Set mtime error: {}", e))?;
    assert!(!is_file_old_enough(&file_path, new_threshold)?);

    Ok(())
}

#[test]
fn test_find_dust_bunnies_logic() -> Result<(), String> {
    let temp_dir = tempdir().map_err(|e| format!("Tempdir error: {}", e))?;
    let scan_path = temp_dir.path();

    // Create an old file
    let old_file_path = scan_path.join("old_bunny.txt");
    let mut old_file = fs::File::create(&old_file_path).map_err(|e| format!("File create error: {}", e))?;
    old_file.write_all(b"old").map_err(|e| format!("File write error: {}", e))?;
    let two_days_ago = Utc::now() - Duration::days(2);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(two_days_ago.into()))
        .map_err(|e| format!("Set mtime error: {}", e))?;

    // Create a new file
    let new_file_path = scan_path.join("new_file.txt");
    let mut new_file = fs::File::create(&new_file_path).map_err(|e| format!("File create error: {}", e))?;
    new_file.write_all(b"new").map_err(|e| format!("File write error: {}", e))?;
    let one_hour_ago = Utc::now() - Duration::hours(1);
    filetime::set_file_mtime(&new_file_path, filetime::FileTime::from_system_time(one_hour_ago.into()))
        .map_err(|e| format!("Set mtime error: {}", e))?;

    // Create a subdirectory with an old file
    let sub_dir = scan_path.join("subdir");
    fs::create_dir(&sub_dir).map_err(|e| format!("Subdir create error: {}", e))?;
    let old_sub_file_path = sub_dir.join("old_sub_bunny.log");
    let mut old_sub_file = fs::File::create(&old_sub_file_path).map_err(|e| format!("File create error: {}", e))?;
    old_sub_file.write_all(b"old sub").map_err(|e| format!("File write error: {}", e))?;
    filetime::set_file_mtime(&old_sub_file_path, filetime::FileTime::from_system_time(two_days_ago.into()))
        .map_err(|e| format!("Set mtime error: {}", e))?;

    let age_threshold = Utc::now() - Duration::days(1);
    let mut dust_bunnies: Vec<PathBuf> = Vec::new();

    for entry in WalkDir::new(scan_path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            if is_file_old_enough(path, age_threshold)? {
                dust_bunnies.push(path.to_path_buf());
            }
        }
    }

    assert_eq!(dust_bunnies.len(), 2);
    assert!(dust_bunnies.contains(&old_file_path));
    assert!(dust_bunnies.contains(&old_sub_file_path));
    assert!(!dust_bunnies.contains(&new_file_path));

    Ok(())
}

#[test]
fn test_compost_file() -> Result<(), String> {
    let temp_dir = tempdir().map_err(|e| format!("Tempdir error: {}", e))?;
    let compost_dir = temp_dir.path().join("compost_bin");

    let file_to_compost = NamedTempFile::new_in(temp_dir.path())
        .map_err(|e| format!("NamedTempFile error: {}", e))?;
    let original_path = file_to_compost.path().to_path_buf();
    let file_name = original_path.file_name().unwrap();
    let destination_path = compost_dir.join(file_name);

    // Ensure the file exists before composting
    assert!(original_path.exists());
    assert!(!compost_dir.exists());
    assert!(!destination_path.exists());

    compost_file(&original_path, &compost_dir)?;

    // Check if the original file is gone and the new one exists
    assert!(!original_path.exists());
    assert!(compost_dir.exists());
    assert!(destination_path.exists());

    Ok(())
}

#[test]
fn test_compost_file_non_existent_source() -> Result<(), String> {
    let temp_dir = tempdir().map_err(|e| format!("Tempdir error: {}", e))?;
    let compost_dir = temp_dir.path().join("compost_bin");
    let non_existent_file = temp_dir.path().join("non_existent.txt");

    let result = compost_file(&non_existent_file, &compost_dir);
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Failed to move"));

    Ok(())
}

#[test]
fn test_compost_file_invalid_destination() -> Result<(), String> {
    let temp_dir = tempdir().map_err(|e| format!("Tempdir error: {}", e))?;
    let file_to_compost = NamedTempFile::new_in(temp_dir.path())
        .map_err(|e| format!("NamedTempFile error: {}", e))?;
    let original_path = file_to_compost.path().to_path_buf();

    // Use a path that cannot be created as a directory (e.g., a file path)
    let invalid_compost_dir = temp_dir.path().join("invalid_dir_name.txt");
    fs::File::create(&invalid_compost_dir).map_err(|e| format!("File create error: {}", e))?;

    let result = compost_file(&original_path, &invalid_compost_dir);
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Failed to create compost directory"));

    Ok(())
}
