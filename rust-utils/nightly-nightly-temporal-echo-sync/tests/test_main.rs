use super::*;
use tempfile::{tempdir, NamedTempFile};
use std::io::Write;

// Mock rationale: We use `tempfile` to create isolated, temporary file system structures
// for each test. This ensures tests are deterministic, run offline, and don't interfere
// with the actual file system or other tests. File content is controlled directly, and
// the core logic functions are called directly, bypassing actual CLI argument parsing
// and stdout capture for simpler, more robust testing.

#[test]
fn test_calculate_file_hash() -> io::Result<()> {
    let mut temp_file = NamedTempFile::new()?;
    temp_file.write_all(b"hello world")?;
    let path = temp_file.path();

    let hash = calculate_file_hash(path)?;
    // SHA256 hash for "hello world"
    assert_eq!(hash, "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824");
    Ok(())
}

#[test]
fn test_create_snapshot_no_files() -> io::Result<()> {
    let dir = tempdir()?;
    let snapshot = create_snapshot_internal(dir.path())?;
    assert!(snapshot.files.is_empty());
    Ok(())
}

#[test]
fn test_create_snapshot_with_files() -> io::Result<()> {
    let dir = tempdir()?;
    let file1_path = dir.path().join("file1.txt");
    fs::write(&file1_path, b"content1")?;
    let file2_path = dir.path().join("subdir").join("file2.txt");
    fs::create_dir(dir.path().join("subdir"))?;
    fs::write(&file2_path, b"content2")?;

    let snapshot = create_snapshot_internal(dir.path())?;
    assert_eq!(snapshot.files.len(), 2);

    let relative_file1 = PathBuf::from("file1.txt");
    let relative_file2 = PathBuf::from("subdir/file2.txt");

    assert!(snapshot.files.contains_key(&relative_file1));
    assert!(snapshot.files.contains_key(&relative_file2));

    let hash1 = calculate_file_hash(&file1_path)?;
    assert_eq!(snapshot.files[&relative_file1].hash, hash1);
    assert_eq!(snapshot.files[&relative_file1].size, 8);

    let hash2 = calculate_file_hash(&file2_path)?;
    assert_eq!(snapshot.files[&relative_file2].hash, hash2);
    assert_eq!(snapshot.files[&relative_file2].size, 8);

    Ok(())
}

#[test]
fn test_compare_snapshot_no_changes() -> io::Result<()> {
    let dir = tempdir()?;
    let file1_path = dir.path().join("file1.txt");
    fs::write(&file1_path, b"content1")?;

    let old_snapshot = create_snapshot_internal(dir.path())?;
    let new_snapshot = create_snapshot_internal(dir.path())?; // Re-snapshot the same state

    let changes = compare_snapshot_internal(&old_snapshot, &new_snapshot);
    assert!(changes.is_empty());
    Ok(())
}

#[test]
fn test_compare_snapshot_new_file() -> io::Result<()> {
    let dir = tempdir()?;
    let file1_path = dir.path().join("file1.txt");
    fs::write(&file1_path, b"content1")?;

    let old_snapshot = create_snapshot_internal(dir.path())?;

    let file2_path = dir.path().join("file2.txt");
    fs::write(&file2_path, b"content2")?; // Add a new file

    let new_snapshot = create_snapshot_internal(dir.path())?;

    let changes = compare_snapshot_internal(&old_snapshot, &new_snapshot);
    assert_eq!(changes.len(), 1);
    assert_eq!(changes[0].change_type, ChangeType::New);
    assert_eq!(changes[0].path, PathBuf::from("file2.txt"));
    Ok(())
}

#[test]
fn test_compare_snapshot_modified_file() -> io::Result<()> {
    let dir = tempdir()?;
    let file1_path = dir.path().join("file1.txt");
    fs::write(&file1_path, b"content1")?;

    let old_snapshot = create_snapshot_internal(dir.path())?;

    fs::write(&file1_path, b"modified_content1")?; // Modify existing file

    let new_snapshot = create_snapshot_internal(dir.path())?;

    let changes = compare_snapshot_internal(&old_snapshot, &new_snapshot);
    assert_eq!(changes.len(), 1);
    assert_eq!(changes[0].change_type, ChangeType::Modified);
    assert_eq!(changes[0].path, PathBuf::from("file1.txt"));
    Ok(())
}

#[test]
fn test_compare_snapshot_deleted_file() -> io::Result<()> {
    let dir = tempdir()?;
    let file1_path = dir.path().join("file1.txt");
    fs::write(&file1_path, b"content1")?;
    let file2_path = dir.path().join("file2.txt");
    fs::write(&file2_path, b"content2")?;

    let old_snapshot = create_snapshot_internal(dir.path())?;

    fs::remove_file(&file2_path)?; // Delete a file

    let new_snapshot = create_snapshot_internal(dir.path())?;

    let changes = compare_snapshot_internal(&old_snapshot, &new_snapshot);
    assert_eq!(changes.len(), 1);
    assert_eq!(changes[0].change_type, ChangeType::Deleted);
    assert_eq!(changes[0].path, PathBuf::from("file2.txt"));
    Ok(())
}

#[test]
fn test_compare_snapshot_mixed_changes() -> io::Result<()> {
    let dir = tempdir()?;
    let file1_path = dir.path().join("file1.txt");
    fs::write(&file1_path, b"content1")?;
    let file2_path = dir.path().join("file2.txt");
    fs::write(&file2_path, b"content2")?;

    let old_snapshot = create_snapshot_internal(dir.path())?;

    fs::write(&file1_path, b"modified_content1")?; // Modify file1
    fs::remove_file(&file2_path)?; // Delete file2
    let file3_path = dir.path().join("file3.txt");
    fs::write(&file3_path, b"content3")?; // Add file3

    let new_snapshot = create_snapshot_internal(dir.path())?;

    let changes = compare_snapshot_internal(&old_snapshot, &new_snapshot);
    assert_eq!(changes.len(), 3);

    let mut change_types = changes.iter().map(|c| &c.change_type).collect::<Vec<_>>();
    change_types.sort_by_key(|&ct| match ct {
        ChangeType::New => 0,
        ChangeType::Modified => 1,
        ChangeType::Deleted => 2,
    });

    assert_eq!(change_types[0], &ChangeType::New);
    assert_eq!(change_types[1], &ChangeType::Modified);
    assert_eq!(change_types[2], &ChangeType::Deleted);

    let mut changed_paths = changes.iter().map(|c| c.path.clone()).collect::<Vec<_>>();
    changed_paths.sort(); // Sort paths for deterministic comparison

    assert_eq!(changed_paths[0], PathBuf::from("file1.txt"));
    assert_eq!(changed_paths[1], PathBuf::from("file2.txt"));
    assert_eq!(changed_paths[2], PathBuf::from("file3.txt"));

    Ok(())
}
