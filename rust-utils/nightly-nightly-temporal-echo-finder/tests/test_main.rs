use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use tempfile::tempdir;

// Mock rationale: For testing file system utilities, creating actual temporary files
// and directories is the most direct and deterministic way to simulate real-world
// scenarios. It's offline as it doesn't rely on external network or services.
// The `tempfile` crate ensures these temporary resources are cleaned up automatically.

#[test]
fn test_hash_file_unique_content() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("unique.txt");
    let mut file = File::create(&file_path).unwrap();
    file.write_all(b"This is unique content.").unwrap();

    let hash = super::hash_file(&file_path).unwrap();
    // Expected SHA256 hash for "This is unique content."
    let expected_hash = hex::decode("1d871d1872f28148b52125f168d184131572d4277726e63297a7019672052445").unwrap();
    assert_eq!(hash, expected_hash);
}

#[test]
fn test_hash_file_empty_content() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("empty.txt");
    File::create(&file_path).unwrap(); // Create an empty file

    let hash = super::hash_file(&file_path).unwrap();
    // Expected SHA256 hash for an empty string
    let expected_hash = hex::decode("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855").unwrap();
    assert_eq!(hash, expected_hash);
}

#[test]
fn test_find_temporal_echoes_no_duplicates() {
    let dir = tempdir().unwrap();
    let path1 = dir.path().join("file1.txt");
    let path2 = dir.path().join("file2.txt");

    File::create(&path1).unwrap().write_all(b"content A").unwrap();
    File::create(&path2).unwrap().write_all(b"content B").unwrap();

    let echoes = super::find_temporal_echoes(&[dir.path().to_path_buf()]);
    assert!(echoes.is_empty());
}

#[test]
fn test_find_temporal_echoes_with_duplicates() {
    let dir = tempdir().unwrap();
    let path1 = dir.path().join("file_a.txt");
    let path2 = dir.path().join("file_b.txt");
    let path3 = dir.path().join("file_c.txt");

    File::create(&path1).unwrap().write_all(b"duplicate content").unwrap();
    File::create(&path2).unwrap().write_all(b"duplicate content").unwrap();
    File::create(&path3).unwrap().write_all(b"unique content").unwrap();

    let echoes = super::find_temporal_echoes(&[dir.path().to_path_buf()]);
    assert_eq!(echoes.len(), 1); // Expect one group of duplicates

    let mut found_paths: Vec<PathBuf> = echoes.values().next().unwrap().clone();
    found_paths.sort(); // Sort for deterministic comparison

    let mut expected_paths = vec![path1, path2];
    expected_paths.sort();

    assert_eq!(found_paths, expected_paths);
}

#[test]
fn test_find_temporal_echoes_multiple_directories() {
    let dir1 = tempdir().unwrap();
    let dir2 = tempdir().unwrap();

    let path1_in_dir1 = dir1.path().join("doc1.txt");
    let path2_in_dir1 = dir1.path().join("doc2_copy.txt");
    let path3_in_dir2 = dir2.path().join("doc2.txt");
    let path4_in_dir2 = dir2.path().join("unique.txt");

    File::create(&path1_in_dir1).unwrap().write_all(b"content X").unwrap();
    File::create(&path2_in_dir1).unwrap().write_all(b"content Y").unwrap();
    File::create(&path3_in_dir2).unwrap().write_all(b"content Y").unwrap(); // Duplicate of path2_in_dir1
    File::create(&path4_in_dir2).unwrap().write_all(b"content Z").unwrap();

    let echoes = super::find_temporal_echoes(&[dir1.path().to_path_buf(), dir2.path().to_path_buf()]);
    assert_eq!(echoes.len(), 1); // Expect one group of duplicates

    let mut found_paths: Vec<PathBuf> = echoes.values().next().unwrap().clone();
    found_paths.sort();

    let mut expected_paths = vec![path2_in_dir1, path3_in_dir2];
    expected_paths.sort();

    assert_eq!(found_paths, expected_paths);
}

#[test]
fn test_find_temporal_echoes_subdirectories() {
    let dir = tempdir().unwrap();
    let subdir = dir.path().join("subdir");
    fs::create_dir(&subdir).unwrap();

    let path1 = dir.path().join("root_file.txt");
    let path2 = subdir.join("sub_file.txt");

    File::create(&path1).unwrap().write_all(b"recursive content").unwrap();
    File::create(&path2).unwrap().write_all(b"recursive content").unwrap();

    let echoes = super::find_temporal_echoes(&[dir.path().to_path_buf()]);
    assert_eq!(echoes.len(), 1);

    let mut found_paths: Vec<PathBuf> = echoes.values().next().unwrap().clone();
    found_paths.sort();

    let mut expected_paths = vec![path1, path2];
    expected_paths.sort();

    assert_eq!(found_paths, expected_paths);
}
