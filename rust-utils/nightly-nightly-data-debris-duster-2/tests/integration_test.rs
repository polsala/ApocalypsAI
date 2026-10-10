use std::collections::HashMap;
use std::fs;
use std::io;
use std::path::PathBuf;
use tempfile::tempdir;
use nightly_data_debris_duster::{calculate_hash, find_duplicate_files}; // Import from the library

// Mock rationale: We create temporary files and directories to simulate a file system
// without touching actual user data or relying on external resources.
// This ensures deterministic and and isolated testing.

#[test]
fn test_finds_duplicates() -> io::Result<()> {
    let dir = tempdir()?;
    let path = dir.path().to_path_buf();

    // Create files
    fs::write(path.join("file1.txt"), "content A")?;
    fs::write(path.join("file2.txt"), "content B")?;
    fs::write(path.join("file3.txt"), "content A")?; // Duplicate of file1
    fs::write(path.join("file4.txt"), "content C")?;
    fs::write(path.join("file5.txt"), "content B")?; // Duplicate of file2

    // Create a subdirectory and a duplicate there
    fs::create_dir(path.join("subdir"))?;
    fs::write(path.join("subdir/file6.txt"), "content A")?; // Duplicate of file1, file3

    let duplicates = find_duplicate_files(&path)?;

    // Assertions
    assert_eq!(duplicates.len(), 2, "Should find two groups of duplicates");

    let hash_a = calculate_hash(&path.join("file1.txt"))?;
    let hash_b = calculate_hash(&path.join("file2.txt"))?;

    assert!(duplicates.contains_key(&hash_a));
    assert!(duplicates.contains_key(&hash_b));

    let mut group_a_paths = duplicates.get(&hash_a).unwrap().clone();
    group_a_paths.sort();
    let mut group_b_paths = duplicates.get(&hash_b).unwrap().clone();
    group_b_paths.sort();

    let expected_group_a_paths = vec![
        path.join("file1.txt"),
        path.join("file3.txt"),
        path.join("subdir/file6.txt"),
    ];
    let expected_group_b_paths = vec![
        path.join("file2.txt"),
        path.join("file5.txt"),
    ];

    assert_eq!(group_a_paths, expected_group_a_paths, "Group A (content A) paths mismatch");
    assert_eq!(group_b_paths, expected_group_b_paths, "Group B (content B) paths mismatch");

    Ok(())
}

#[test]
fn test_no_duplicates() -> io::Result<()> {
    let dir = tempdir()?;
    let path = dir.path().to_path_buf();

    fs::write(path.join("unique1.txt"), "content X")?;
    fs::write(path.join("unique2.txt"), "content Y")?;
    fs::write(path.join("unique3.txt"), "content Z")?;

    let duplicates = find_duplicate_files(&path)?;

    assert!(duplicates.is_empty(), "Should find no duplicate groups");

    Ok(())
}

#[test]
fn test_empty_files_are_duplicates() -> io::Result<()> {
    let dir = tempdir()?;
    let path = dir.path().to_path_buf();

    fs::write(path.join("empty1.txt"), "")?;
    fs::write(path.join("empty2.txt"), "")?;
    fs::write(path.join("non_empty.txt"), "some content")?;

    let duplicates = find_duplicate_files(&path)?;

    assert_eq!(duplicates.len(), 1, "Should find one group of empty file duplicates");

    let empty_hash = calculate_hash(&path.join("empty1.txt"))?;
    assert!(duplicates.contains_key(&empty_hash));

    let mut empty_group_paths = duplicates.get(&empty_hash).unwrap().clone();
    empty_group_paths.sort();

    let expected_paths = vec![
        path.join("empty1.txt"),
        path.join("empty2.txt"),
    ];

    assert_eq!(empty_group_paths, expected_paths, "Empty files group not correct");

    Ok(())
}

#[test]
fn test_non_existent_path() {
    let non_existent_path = PathBuf::from("/this/path/does/not/exist_12345");
    let result = find_duplicate_files(&non_existent_path);
    assert!(result.is_err());
    assert_eq!(result.unwrap_err().kind(), io::ErrorKind::NotFound);
}

#[test]
fn test_path_is_file_not_dir() -> io::Result<()> {
    let dir = tempdir()?;
    let file_path = dir.path().join("single_file.txt");
    fs::write(&file_path, "some content")?;

    let result = find_duplicate_files(&file_path);
    assert!(result.is_err());
    assert_eq!(result.unwrap_err().kind(), io::ErrorKind::InvalidInput);
    Ok(())
}
