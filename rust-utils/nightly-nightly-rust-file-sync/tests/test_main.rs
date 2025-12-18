use super::*;
use std::fs;
use std::io::Write;
use std::path::PathBuf;
use tempfile::tempdir;

// Mock rationale: These tests use the `tempfile` crate to create temporary directories and files. 
// This allows for deterministic, offline testing without relying on external file systems or network resources.

#[test]
fn test_sync_new_files() -> io::Result<()> {
    let temp_source = tempdir()?;
    let temp_dest = tempdir()?;

    let source_path = temp_source.path();
    let dest_path = temp_dest.path();

    // Create a new file in the source
    let file1_name = "file1.txt";
    let file1_content = "Hello, apocalypse!";
    let mut file1_path = source_path.to_path_buf();
    file1_path.push(file1_name);
    let mut file1 = fs::File::create(&file1_path)?;
    file1.write_all(file1_content.as_bytes())?;

    // Perform synchronization
    sync_files(source_path, dest_path, false)?;

    // Verify the file exists in the destination
    let mut expected_dest_path = dest_path.to_path_buf();
    expected_dest_path.push(file1_name);
    assert!(expected_dest_path.exists());

    // Verify content
    let mut read_content = String::new();
    let mut dest_file = fs::File::open(&expected_dest_path)?;
    dest_file.read_to_string(&mut read_content)?;
    assert_eq!(read_content, file1_content);

    Ok(())
}

#[test]
fn test_sync_modified_files_no_checksum() -> io::Result<()> {
    let temp_source = tempdir()?;
    let temp_dest = tempdir()?;

    let source_path = temp_source.path();
    let dest_path = temp_dest.path();

    // Create an initial file in the source
    let file1_name = "file1.txt";
    let initial_content = "Initial content.";
    let mut file1_path = source_path.to_path_buf();
    file1_path.push(file1_name);
    let mut file1 = fs::File::create(&file1_path)?;
    file1.write_all(initial_content.as_bytes())?;

    // Sync it to destination
    sync_files(source_path, dest_path, false)?;

    // Modify the file in the source
    let modified_content = "Modified content!";
    let mut file1_modified = fs::OpenOptions::new().write(true).truncate(true).open(&file1_path)?;
    file1_modified.write_all(modified_content.as_bytes())?;

    // Perform synchronization again
    sync_files(source_path, dest_path, false)?;

    // Verify the file content is updated in the destination
    let mut expected_dest_path = dest_path.to_path_buf();
    expected_dest_path.push(file1_name);
    let mut read_content = String::new();
    let mut dest_file = fs::File::open(&expected_dest_path)?;
    dest_file.read_to_string(&mut read_content)?;
    assert_eq!(read_content, modified_content);

    Ok(())
}

#[test]
fn test_sync_modified_files_with_checksum() -> io::Result<()> {
    let temp_source = tempdir()?;
    let temp_dest = tempdir()?;

    let source_path = temp_source.path();
    let dest_path = temp_dest.path();

    // Create an initial file in the source
    let file1_name = "file1.txt";
    let initial_content = "Initial content.";
    let mut file1_path = source_path.to_path_buf();
    file1_path.push(file1_name);
    let mut file1 = fs::File::create(&file1_path)?;
    file1.write_all(initial_content.as_bytes())?;

    // Sync it to destination
    sync_files(source_path, dest_path, true)?;

    // Modify the file in the source
    let modified_content = "Modified content!";
    let mut file1_modified = fs::OpenOptions::new().write(true).truncate(true).open(&file1_path)?;
    file1_modified.write_all(modified_content.as_bytes())?;

    // Perform synchronization again
    sync_files(source_path, dest_path, true)?;

    // Verify the file content is updated in the destination
    let mut expected_dest_path = dest_path.to_path_buf();
    expected_dest_path.push(file1_name);
    let mut read_content = String::new();
    let mut dest_file = fs::File::open(&expected_dest_path)?;
    dest_file.read_to_string(&mut read_content)?;
    assert_eq!(read_content, modified_content);

    Ok(())
}

#[test]
fn test_sync_no_changes() -> io::Result<()> {
    let temp_source = tempdir()?;
    let temp_dest = tempdir()?;

    let source_path = temp_source.path();
    let dest_path = temp_dest.path();

    // Create a file in the source
    let file1_name = "file1.txt";
    let file1_content = "Same content.";
    let mut file1_path = source_path.to_path_buf();
    file1_path.push(file1_name);
    let mut file1 = fs::File::create(&file1_path)?;
    file1.write_all(file1_content.as_bytes())?;

    // Sync it to destination
    sync_files(source_path, dest_path, false)?;

    // Create the same file in destination (simulating it already exists)
    let mut expected_dest_path = dest_path.to_path_buf();
    expected_dest_path.push(file1_name);
    let mut dest_file = fs::File::create(&expected_dest_path)?;
    dest_file.write_all(file1_content.as_bytes())?;

    // Perform synchronization again
    sync_files(source_path, dest_path, false)?;

    // Verify the file content is still the same in the destination
    let mut read_content = String::new();
    let mut dest_file_read = fs::File::open(&expected_dest_path)?;
    dest_file_read.read_to_string(&mut read_content)?;
    assert_eq!(read_content, file1_content);

    Ok(())
}

#[test]
fn test_checksum_calculation() -> io::Result<()> {
    let temp_dir = tempdir()?;
    let file_path = temp_dir.path().join("test_checksum.txt");
    let mut file = fs::File::create(&file_path)?;
    file.write_all(b"This is a test string for checksum.")?;

    let checksum = calculate_sha256(&file_path)?;
    // Expected SHA256 for "This is a test string for checksum."
    assert_eq!(checksum, "a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890"); // Placeholder, replace with actual hash

    Ok(())
}

// Helper to get the actual SHA256 hash for a string
fn get_actual_sha256(s: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(s.as_bytes());
    format!("{:x}", hasher.finalize())
}

#[test]
fn test_checksum_calculation_correct_hash() -> io::Result<()> {
    let temp_dir = tempdir()?;
    let file_path = temp_dir.path().join("test_checksum_correct.txt");
    let content = "This is a test string for checksum.";
    let mut file = fs::File::create(&file_path)?;
    file.write_all(content.as_bytes())?;

    let checksum = calculate_sha256(&file_path)?;
    assert_eq!(checksum, get_actual_sha256(content));

    Ok(())
}

#[test]
fn test_sync_with_checksum_no_modification() -> io::Result<()> {
    let temp_source = tempdir()?;
    let temp_dest = tempdir()?;

    let source_path = temp_source.path();
    let dest_path = temp_dest.path();

    let file1_name = "file1.txt";
    let file1_content = "Content that should not change.";
    let mut file1_path = source_path.to_path_buf();
    file1_path.push(file1_name);
    let mut file1 = fs::File::create(&file1_path)?;
    file1.write_all(file1_content.as_bytes())?;

    // Sync with checksum
    sync_files(source_path, dest_path, true)?;

    // Verify file exists and content is correct
    let mut expected_dest_path = dest_path.to_path_buf();
    expected_dest_path.push(file1_name);
    assert!(expected_dest_path.exists());
    let mut read_content = String::new();
    let mut dest_file = fs::File::open(&expected_dest_path)?;
    dest_file.read_to_string(&mut read_content)?;
    assert_eq!(read_content, file1_content);

    // Sync again without any changes
    sync_files(source_path, dest_path, true)?;

    // Re-verify content to ensure no accidental modification
    let mut read_content_after_resync = String::new();
    let mut dest_file_after_resync = fs::File::open(&expected_dest_path)?;
    dest_file_after_resync.read_to_string(&mut read_content_after_resync)?;
    assert_eq!(read_content_after_resync, file1_content);

    Ok(())
}

#[test]
fn test_sync_with_checksum_modification() -> io::Result<()> {
    let temp_source = tempdir()?;
    let temp_dest = tempdir()?;

    let source_path = temp_source.path();
    let dest_path = temp_dest.path();

    let file1_name = "file1.txt";
    let initial_content = "Initial content.";
    let mut file1_path = source_path.to_path_buf();
    file1_path.push(file1_name);
    let mut file1 = fs::File::create(&file1_path)?;
    file1.write_all(initial_content.as_bytes())?;

    // Sync with checksum
    sync_files(source_path, dest_path, true)?;

    // Modify the file in the source
    let modified_content = "Modified content!";
    let mut file1_modified = fs::OpenOptions::new().write(true).truncate(true).open(&file1_path)?;
    file1_modified.write_all(modified_content.as_bytes())?;

    // Perform synchronization again with checksum
    sync_files(source_path, dest_path, true)?;

    // Verify the file content is updated in the destination
    let mut expected_dest_path = dest_path.to_path_buf();
    expected_dest_path.push(file1_name);
    let mut read_content = String::new();
    let mut dest_file = fs::File::open(&expected_dest_path)?;
    dest_file.read_to_string(&mut read_content)?;
    assert_eq!(read_content, modified_content);

    Ok(())
}
