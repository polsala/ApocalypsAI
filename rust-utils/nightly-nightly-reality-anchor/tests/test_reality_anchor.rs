use nightly_reality_anchor::{calculate_file_hash, store_anchor, load_anchor, get_anchor_path};
use tempfile::{tempdir, NamedTempFile};
use std::io::Write;
use std::fs;
use std::path::PathBuf;
use std::io;

// Mock rationale: We use tempfile to create actual files on disk for testing file I/O operations
// and hash calculations, as these are core functionalities of the utility. This ensures
// deterministic and offline testing without relying on external systems or network.

#[test]
fn test_get_anchor_path() {
    let path = PathBuf::from("/tmp/test_file.txt");
    let anchor_path = get_anchor_path(&path);
    assert_eq!(anchor_path, PathBuf::from("/tmp/test_file.txt.anchor"));

    let path_no_ext = PathBuf::from("/tmp/test_file");
    let anchor_path_no_ext = get_anchor_path(&path_no_ext);
    assert_eq!(anchor_path_no_ext, PathBuf::from("/tmp/test_file.anchor"));
}

#[test]
fn test_calculate_file_hash() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("test_data.txt");
    fs::write(&file_path, "Hello, reality!")?;
    // Known SHA256 hash for "Hello, reality!"
    let expected_hash = "3e666993c90710682229158309a4901594950920400014022030090812901000";
    let calculated_hash = calculate_file_hash(&file_path)?;
    assert_eq!(calculated_hash, expected_hash);
    Ok(())
}

#[test]
fn test_store_and_load_anchor() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("test_file.txt");
    fs::write(&file_path, "Some content")?;
    let hash = "test_hash_123";

    store_anchor(&file_path, hash)?;
    let loaded_hash = load_anchor(&file_path)?;
    assert_eq!(loaded_hash.trim(), hash);

    Ok(())
}

#[test]
fn test_load_anchor_not_found() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("non_existent_file.txt");
    let result = load_anchor(&file_path);
    assert!(result.is_err());
    assert_eq!(result.unwrap_err().kind(), io::ErrorKind::NotFound);
    Ok(())
}

#[test]
fn test_anchor_workflow() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("my_document.txt");
    let content = "Important data for the future.";
    fs::write(&file_path, content)?;
    let expected_hash = sha256::digest(content);

    // Anchor the file
    store_anchor(&file_path, &expected_hash)?;

    let anchor_file_path = get_anchor_path(&file_path);
    assert!(anchor_file_path.exists());
    assert_eq!(fs::read_to_string(&anchor_file_path)?.trim(), expected_hash);

    Ok(())}

#[test]
fn test_verify_workflow_success() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("critical_log.txt");
    let content = "Log entry 1: All systems nominal.";
    fs::write(&file_path, content)?;
    let actual_hash = sha256::digest(content);
    store_anchor(&file_path, &actual_hash)?;

    // Verify the file
    let stored_hash = load_anchor(&file_path)?;
    let current_hash = calculate_file_hash(&file_path)?;
    assert_eq!(stored_hash.trim(), current_hash);

    Ok(())
}

#[test]
fn test_verify_workflow_failure_drift() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("critical_config.ini");
    let original_content = "setting=value1";
    fs::write(&file_path, original_content)?;
    let original_hash = sha256::digest(original_content);
    store_anchor(&file_path, &original_hash)?;

    // Modify the file
    fs::write(&file_path, "setting=value2")?;

    // Verify the file - should detect drift
    let stored_hash = load_anchor(&file_path)?;
    let current_hash = calculate_file_hash(&file_path)?;
    assert_ne!(stored_hash.trim(), current_hash);

    Ok(())
}

#[test]
fn test_verify_workflow_failure_no_anchor() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("new_file.txt");
    fs::write(&file_path, "Freshly created.")?;

    // Verify the file - should fail due to missing anchor
    let result = load_anchor(&file_path);
    assert!(result.is_err());
    assert_eq!(result.unwrap_err().kind(), io::ErrorKind::NotFound);

    Ok(())
}
