use super::*;
use tempfile::tempdir;
use std::io::Write;

// Mock rationale: We need to simulate a file system with specific files and content
// to test the duplicate detection logic. Creating temporary directories and files
// allows for deterministic, isolated, and offline testing without affecting the
// actual file system or requiring external resources.

#[test]
fn test_no_duplicates() {
    let dir = tempdir().expect("Failed to create temp dir");
    let path = dir.path();

    let file1_path = path.join("file1.txt");
    let mut file1 = fs::File::create(&file1_path).expect("Failed to create file1");
    file1.write_all(b"content A").expect("Failed to write to file1");

    let file2_path = path.join("file2.txt");
    let mut file2 = fs::File::create(&file2_path).expect("Failed to create file2");
    file2.write_all(b"content B").expect("Failed to write to file2");

    let duplicates = find_duplicates(path);
    let duplicate_groups: Vec<&Vec<PathBuf>> = duplicates.values().filter(|v| v.len() > 1).collect();

    assert!(duplicate_groups.is_empty(), "Expected no duplicates, but found some.");
    dir.close().expect("Failed to close temp dir");
}

#[test]
fn test_with_duplicates() {
    let dir = tempdir().expect("Failed to create temp dir");
    let path = dir.path();

    let file1_path = path.join("file1.txt");
    let mut file1 = fs::File::create(&file1_path).expect("Failed to create file1");
    file1.write_all(b"duplicate content").expect("Failed to write to file1");

    let file2_path = path.join("file2.txt");
    let mut file2 = fs::File::create(&file2_path).expect("Failed to create file2");
    file2.write_all(b"duplicate content").expect("Failed to write to file2");

    let file3_path = path.join("file3.txt");
    let mut file3 = fs::File::create(&file3_path).expect("Failed to create file3");
    file3.write_all(b"unique content").expect("Failed to write to file3");

    let duplicates = find_duplicates(path);
    let duplicate_groups: Vec<&Vec<PathBuf>> = duplicates.values().filter(|v| v.len() > 1).collect();

    assert_eq!(duplicate_groups.len(), 1, "Expected exactly one group of duplicates.");
    let group = duplicate_groups[0];
    assert_eq!(group.len(), 2, "Expected two files in the duplicate group.");
    assert!(group.contains(&file1_path), "Duplicate group should contain file1");
    assert!(group.contains(&file2_path), "Duplicate group should contain file2");
    assert!(!group.contains(&file3_path), "Duplicate group should not contain file3");

    dir.close().expect("Failed to close temp dir");
}

#[test]
fn test_empty_directory() {
    let dir = tempdir().expect("Failed to create temp dir");
    let path = dir.path();

    let duplicates = find_duplicates(path);
    let duplicate_groups: Vec<&Vec<PathBuf>> = duplicates.values().filter(|v| v.len() > 1).collect();

    assert!(duplicate_groups.is_empty(), "Expected no duplicates in an empty directory.");
    dir.close().expect("Failed to close temp dir");
}

#[test]
fn test_subdirectories() {
    let dir = tempdir().expect("Failed to create temp dir");
    let path = dir.path();

    let subdir_path = path.join("subdir");
    fs::create_dir(&subdir_path).expect("Failed to create subdir");

    let file1_path = path.join("file1.txt");
    let mut file1 = fs::File::create(&file1_path).expect("Failed to create file1");
    file1.write_all(b"shared content").expect("Failed to write to file1");

    let file2_path = subdir_path.join("file2.txt");
    let mut file2 = fs::File::create(&file2_path).expect("Failed to create file2");
    file2.write_all(b"shared content").expect("Failed to write to file2");

    let duplicates = find_duplicates(path);
    let duplicate_groups: Vec<&Vec<PathBuf>> = duplicates.values().filter(|v| v.len() > 1).collect();

    assert_eq!(duplicate_groups.len(), 1, "Expected one group of duplicates across subdirectories.");
    let group = duplicate_groups[0];
    assert!(group.contains(&file1_path), "Duplicate group should contain file1");
    assert!(group.contains(&file2_path), "Duplicate group should contain file2");

    dir.close().expect("Failed to close temp dir");
}

#[test]
fn test_different_sizes_not_duplicates() {
    let dir = tempdir().expect("Failed to create temp dir");
    let path = dir.path();

    let file1_path = path.join("file1.txt");
    let mut file1 = fs::File::create(&file1_path).expect("Failed to create file1");
    file1.write_all(b"content A").expect("Failed to write to file1");

    let file2_path = path.join("file2.txt");
    let mut file2 = fs::File::create(&file2_path).expect("Failed to create file2");
    file2.write_all(b"content AA").expect("Failed to write to file2"); // Different content, different size

    let duplicates = find_duplicates(path);
    let duplicate_groups: Vec<&Vec<PathBuf>> = duplicates.values().filter(|v| v.len() > 1).collect();

    assert!(duplicate_groups.is_empty(), "Expected no duplicates for files with different content/sizes.");
    dir.close().expect("Failed to close temp dir");
}
