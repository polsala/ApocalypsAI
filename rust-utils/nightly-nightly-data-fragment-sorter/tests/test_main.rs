use super::{categorize_file, calculate_hash, FragmentCategory};
use std::path::{Path, PathBuf};
use std::collections::HashMap;
use std::fs;
use std::io::Write;
use tempfile::tempdir;
use filetime::{FileTime, set_file_mtime};
use std::time::{SystemTime, Duration};

// Mock rationale: We use `tempfile` to create isolated, temporary file system structures
// for each test. This ensures tests are deterministic, don't interfere with each other,
// and clean up after themselves, without requiring actual network or external service calls.
// `filetime` is used to precisely control file modification times for 'recent' file tests.

#[test]
fn test_calculate_hash() {
    let temp_dir = tempdir().unwrap();
    let file_path = temp_dir.path().join("test_hash_file.txt");
    fs::write(&file_path, "hello world").unwrap();

    let hash = calculate_hash(&file_path).unwrap();
    assert_eq!(hash, "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"); // SHA256 of "hello world"
}

#[test]
fn test_categorize_empty_file() {
    let temp_dir = tempdir().unwrap();
    let file_path = temp_dir.path().join("empty.txt");
    fs::File::create(&file_path).unwrap(); // Creates an empty file

    let mut hashes = HashMap::new();
    let category = categorize_file(&file_path, 1024 * 1024, 7, &mut hashes);
    assert_eq!(category, FragmentCategory::Empty);
}

#[test]
fn test_categorize_large_file() {
    let temp_dir = tempdir().unwrap();
    let file_path = temp_dir.path().join("large.bin");
    let mut file = fs::File::create(&file_path).unwrap();
    file.write_all(&vec![0; 2 * 1024 * 1024]).unwrap(); // 2MB file

    let mut hashes = HashMap::new();
    let category = categorize_file(&file_path, 1024 * 1024, 7, &mut hashes); // min_large_size = 1MB
    assert_eq!(category, FragmentCategory::Large);
}

#[test]
fn test_categorize_recent_file() {
    let temp_dir = tempdir().unwrap();
    let file_path = temp_dir.path().join("recent.txt");
    fs::write(&file_path, "recent content").unwrap();

    // Set modification time to be just a few hours ago (well within 7 days)
    let now = SystemTime::now();
    let recent_time = now - Duration::from_secs(3 * 60 * 60); // 3 hours ago
    set_file_mtime(&file_path, FileTime::from_system_time(recent_time)).unwrap();

    let mut hashes = HashMap::new();
    let category = categorize_file(&file_path, 10, 7, &mut hashes); // min_large_size=10 (so it's not large)
    assert_eq!(category, FragmentCategory::Recent);
}

#[test]
fn test_categorize_old_file() {
    let temp_dir = tempdir().unwrap();
    let file_path = temp_dir.path().join("old.txt");
    fs::write(&file_path, "old content").unwrap();

    // Set modification time to be far in the past (e.g., 10 days ago)
    let now = SystemTime::now();
    let old_time = now - Duration::from_secs(10 * 24 * 60 * 60); // 10 days ago
    set_file_mtime(&file_path, FileTime::from_system_time(old_time)).unwrap();

    let mut hashes = HashMap::new();
    let category = categorize_file(&file_path, 10, 7, &mut hashes); // min_large_size=10, recent_days=7
    assert_eq!(category, FragmentCategory::Other); // Should not be recent
}

#[test]
fn test_categorize_duplicate_file() {
    let temp_dir = tempdir().unwrap();
    let file1_path = temp_dir.path().join("file1.txt");
    let file2_path = temp_dir.path().join("file2.txt");
    let content = "duplicate content";
    fs::write(&file1_path, content).unwrap();
    fs::write(&file2_path, content).unwrap();

    let mut hashes = HashMap::new();

    // First file should be 'Other' and its hash stored
    let category1 = categorize_file(&file1_path, 1024 * 1024, 7, &mut hashes);
    assert_eq!(category1, FragmentCategory::Other);
    assert_eq!(hashes.len(), 1);

    // Second file should be a duplicate
    let category2 = categorize_file(&file2_path, 1024 * 1024, 7, &mut hashes);
    match category2 {
        FragmentCategory::Duplicate(original_path) => {
            assert_eq!(PathBuf::from(original_path), file1_path);
        }
        _ => panic!("Expected Duplicate category, got {:?}", category2),
    }
    assert_eq!(hashes.len(), 1); // Still 1 unique hash
}

#[test]
fn test_categorize_other_file() {
    let temp_dir = tempdir().unwrap();
    let file_path = temp_dir.path().join("other.txt");
    fs::write(&file_path, "small old content").unwrap();

    // Make it old by setting modified time far in the past
    let past_time = SystemTime::UNIX_EPOCH; // Very old
    set_file_mtime(&file_path, FileTime::from_system_time(past_time)).unwrap();

    let mut hashes = HashMap::new();
    let category = categorize_file(&file_path, 1024 * 1024, 7, &mut hashes);
    assert_eq!(category, FragmentCategory::Other);
}

#[test]
fn test_categorize_error_file() {
    let non_existent_path = PathBuf::from("/non/existent/path/file.txt"); // Should cause metadata error

    let mut hashes = HashMap::new();
    let category = categorize_file(&non_existent_path, 10, 7, &mut hashes);
    assert!(matches!(category, FragmentCategory::Error(_)));
}
