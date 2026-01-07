use super::*;
use std::fs;
use std::io::Write;
use std::path::Path;
use tempfile::tempdir;

// Mock rationale: Using tempfile crate to create isolated temporary directories for testing.
// This avoids relying on external file system state and ensures deterministic, offline tests.

#[test]
fn test_sync_new_files() {
    let tmp_src = tempdir().unwrap();
    let tmp_dest = tempdir().unwrap();

    let src_dir = tmp_src.path();
    let dest_dir = tmp_dest.path();

    // Create a file in the source directory
    let file1_path = src_dir.join("file1.txt");
    let mut file1 = fs::File::create(&file1_path).unwrap();
    file1.write_all(b"content1").unwrap();

    let file2_path = src_dir.join("file2.txt");
    let mut file2 = fs::File::create(&file2_path).unwrap();
    file2.write_all(b"content2").unwrap();

    // Perform synchronization
    sync_files(src_dir, dest_dir, false, false, false).unwrap();

    // Assert files exist in destination
    assert!(dest_dir.join("file1.txt").exists());
    assert!(dest_dir.join("file2.txt").exists());

    // Assert content is the same
    let mut dest_file1 = fs::File::open(dest_dir.join("file1.txt")).unwrap();
    let mut content = Vec::new();
    dest_file1.read_to_end(&mut content).unwrap();
    assert_eq!(content, b"content1");
}

#[test]
fn test_sync_overwrite_existing() {
    let tmp_src = tempdir().unwrap();
    let tmp_dest = tempdir().unwrap();

    let src_dir = tmp_src.path();
    let dest_dir = tmp_dest.path();

    // Create a file in the source directory
    let file1_path = src_dir.join("file1.txt");
    let mut file1 = fs::File::create(&file1_path).unwrap();
    file1.write_all(b"new content").unwrap();

    // Create an existing file in the destination directory with different content
    let dest_file1_path = dest_dir.join("file1.txt");
    let mut dest_file1 = fs::File::create(&dest_file1_path).unwrap();
    dest_file1.write_all(b"old content").unwrap();

    // Perform synchronization with overwrite enabled
    sync_files(src_dir, dest_dir, false, true, false).unwrap();

    // Assert content is overwritten
    let mut dest_file1_after = fs::File::open(&dest_file1_path).unwrap();
    let mut content = Vec::new();
    dest_file1_after.read_to_end(&mut content).unwrap();
    assert_eq!(content, b"new content");
}

#[test]
fn test_sync_skip_existing_no_overwrite() {
    let tmp_src = tempdir().unwrap();
    let tmp_dest = tempdir().unwrap();

    let src_dir = tmp_src.path();
    let dest_dir = tmp_dest.path();

    // Create a file in the source directory
    let file1_path = src_dir.join("file1.txt");
    let mut file1 = fs::File::create(&file1_path).unwrap();
    file1.write_all(b"new content").unwrap();

    // Create an existing file in the destination directory with the same content
    let dest_file1_path = dest_dir.join("file1.txt");
    let mut dest_file1 = fs::File::create(&dest_file1_path).unwrap();
    dest_file1.write_all(b"new content").unwrap();

    // Perform synchronization without overwrite
    sync_files(src_dir, dest_dir, false, false, false).unwrap();

    // Assert content is not changed (should still be "new content")
    let mut dest_file1_after = fs::File::open(&dest_file1_path).unwrap();
    let mut content = Vec::new();
    dest_file1_after.read_to_end(&mut content).unwrap();
    assert_eq!(content, b"new content");
}

#[test]
fn test_sync_dry_run() {
    let tmp_src = tempdir().unwrap();
    let tmp_dest = tempdir().unwrap();

    let src_dir = tmp_src.path();
    let dest_dir = tmp_dest.path();

    // Create a file in the source directory
    let file1_path = src_dir.join("file1.txt");
    let mut file1 = fs::File::create(&file1_path).unwrap();
    file1.write_all(b"content for dry run").unwrap();

    // Perform synchronization in dry run mode
    sync_files(src_dir, dest_dir, false, false, true).unwrap();

    // Assert no files were actually created in the destination
    assert!(!dest_dir.join("file1.txt").exists());
}

#[test]
fn test_sync_checksum_verification_match() {
    let tmp_src = tempdir().unwrap();
    let tmp_dest = tempdir().unwrap();

    let src_dir = tmp_src.path();
    let dest_dir = tmp_dest.path();

    // Create a file in the source directory
    let file1_path = src_dir.join("file1.txt");
    let mut file1 = fs::File::create(&file1_path).unwrap();
    file1.write_all(b"content for checksum").unwrap();

    // Create the same file in the destination directory
    let dest_file1_path = dest_dir.join("file1.txt");
    let mut dest_file1 = fs::File::create(&dest_file1_path).unwrap();
    dest_file1.write_all(b"content for checksum").unwrap();

    // Perform synchronization with checksum enabled
    sync_files(src_dir, dest_dir, true, false, false).unwrap();

    // Assert file content is unchanged (no copy needed)
    let mut dest_file1_after = fs::File::open(&dest_file1_path).unwrap();
    let mut content = Vec::new();
    dest_file1_after.read_to_end(&mut content).unwrap();
    assert_eq!(content, b"content for checksum");
}

#[test]
fn test_sync_checksum_verification_mismatch() {
    let tmp_src = tempdir().unwrap();
    let tmp_dest = tempdir().unwrap();

    let src_dir = tmp_src.path();
    let dest_dir = tmp_dest.path();

    // Create a file in the source directory
    let file1_path = src_dir.join("file1.txt");
    let mut file1 = fs::File::create(&file1_path).unwrap();
    file1.write_all(b"new content for checksum").unwrap();

    // Create the same file in the destination directory with different content
    let dest_file1_path = dest_dir.join("file1.txt");
    let mut dest_file1 = fs::File::create(&dest_file1_path).unwrap();
    dest_file1.write_all(b"old content for checksum").unwrap();

    // Perform synchronization with checksum enabled
    sync_files(src_dir, dest_dir, true, false, false).unwrap();

    // Assert file content is updated due to checksum mismatch
    let mut dest_file1_after = fs::File::open(&dest_file1_path).unwrap();
    let mut content = Vec::new();
    dest_file1_after.read_to_end(&mut content).unwrap();
    assert_eq!(content, b"new content for checksum");
}

#[test]
fn test_sync_recursive_directories() {
    let tmp_src = tempdir().unwrap();
    let tmp_dest = tempdir().unwrap();

    let src_dir = tmp_src.path();
    let dest_dir = tmp_dest.path();

    // Create a subdirectory and a file within it
    let sub_dir_path = src_dir.join("subdir");
    fs::create_dir(&sub_dir_path).unwrap();
    let sub_file_path = sub_dir_path.join("subfile.txt");
    let mut sub_file = fs::File::create(&sub_file_path).unwrap();
    sub_file.write_all(b"content in subdir").unwrap();

    // Perform synchronization
    sync_files(src_dir, dest_dir, false, false, false).unwrap();

    // Assert subdirectory and file exist in destination
    let dest_sub_dir = dest_dir.join("subdir");
    assert!(dest_sub_dir.exists());
    assert!(dest_sub_dir.join("subfile.txt").exists());

    // Assert content is the same
    let mut dest_sub_file = fs::File::open(dest_sub_dir.join("subfile.txt")).unwrap();
    let mut content = Vec::new();
    dest_sub_file.read_to_end(&mut content).unwrap();
    assert_eq!(content, b"content in subdir");
}

#[test]
fn test_calculate_md5() {
    let tmp_dir = tempdir().unwrap();
    let file_path = tmp_dir.path().join("test_md5.txt");
    let mut file = fs::File::create(&file_path).unwrap();
    file.write_all(b"hello world").unwrap();

    let md5_hash = calculate_md5(&file_path).unwrap();
    // Expected MD5 for "hello world" is "5eb63bbbe01eeed093cb22bb8f5acdc3"
    assert_eq!(md5_hash, "5eb63bbbe01eeed093cb22bb8f5acdc3");
}

#[test]
fn test_sync_empty_source() {
    let tmp_src = tempdir().unwrap();
    let tmp_dest = tempdir().unwrap();

    let src_dir = tmp_src.path();
    let dest_dir = tmp_dest.path();

    // Perform synchronization with an empty source directory
    sync_files(src_dir, dest_dir, false, false, false).unwrap();

    // Assert destination directory is still empty
    let entries = fs::read_dir(dest_dir).unwrap().count();
    assert_eq!(entries, 0);
}

#[test]
fn test_sync_destination_not_exists() {
    let tmp_src = tempdir().unwrap();
    let non_existent_dest = PathBuf::from("non_existent_dest_dir_for_test");

    let src_dir = tmp_src.path();

    // Create a file in the source directory
    let file1_path = src_dir.join("file1.txt");
    let mut file1 = fs::File::create(&file1_path).unwrap();
    file1.write_all(b"content1").unwrap();

    // Perform synchronization when destination does not exist
    sync_files(src_dir, &non_existent_dest, false, false, false).unwrap();

    // Assert the destination directory and file were created
    assert!(non_existent_dest.exists());
    assert!(non_existent_dest.join("file1.txt").exists());

    // Clean up the created directory
    fs::remove_dir_all(&non_existent_dest).unwrap();
}
