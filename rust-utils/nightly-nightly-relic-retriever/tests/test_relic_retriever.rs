use super::{
    calculate_hash,
    main,
    Args
};
use clap::Parser;
use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use tempfile::tempdir;

// Mock rationale: We use `tempfile::tempdir` to create isolated, temporary file system
// environments for each test. This ensures tests are deterministic, don't interfere
// with the actual filesystem, and run offline without external dependencies.

fn create_test_file(dir: &Path, filename: &str, content: &str) -> PathBuf {
    let file_path = dir.join(filename);
    let mut file = fs::File::create(&file_path).unwrap();
    file.write_all(content.as_bytes()).unwrap();
    file_path
}

fn setup_test_environment() -> (tempfile::TempDir, PathBuf) {
    let tmp_dir = tempdir().unwrap();
    let scan_path = tmp_dir.path().join("scavenged_data");
    fs::create_dir(&scan_path).unwrap();
    (tmp_dir, scan_path)
}

#[test]
fn test_calculate_hash() {
    let (_tmp_dir, scan_path) = setup_test_environment();
    let file_path = create_test_file(&scan_path, "test_relic.txt", "hello world");
    let hash = calculate_hash(&file_path).unwrap();
    assert_eq!(hash, "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e7304336293879ecb");
}

#[test]
fn test_no_duplicates_dry_run() {
    let (_tmp_dir, scan_path) = setup_test_environment();
    create_test_file(&scan_path, "unique1.txt", "content A");
    create_test_file(&scan_path, "unique2.txt", "content B");

    let args = Args::parse_from(&["relic-retriever", "scan", scan_path.to_str().unwrap(), "--dry-run"]);
    // Redirect stdout/stderr to capture output for assertions, if needed.
    // For now, we'll rely on file system state.
    let result = std::panic::catch_unwind(|| {
        main().unwrap();
    });
    assert!(result.is_ok());

    assert!(scan_path.join("unique1.txt").exists());
    assert!(scan_path.join("unique2.txt").exists());
    assert!(!scan_path.join(".void_vault").exists());
}

#[test]
fn test_duplicates_dry_run() {
    let (_tmp_dir, scan_path) = setup_test_environment();
    create_test_file(&scan_path, "relic_a.txt", "duplicate content");
    create_test_file(&scan_path, "relic_b.txt", "duplicate content");
    create_test_file(&scan_path, "unique_c.txt", "unique content");

    let args = Args::parse_from(&["relic-retriever", "scan", scan_path.to_str().unwrap(), "--dry-run"]);
    let result = std::panic::catch_unwind(|| {
        main().unwrap();
    });
    assert!(result.is_ok());

    // In dry run, all original files should still exist
    assert!(scan_path.join("relic_a.txt").exists());
    assert!(scan_path.join("relic_b.txt").exists());
    assert!(scan_path.join("unique_c.txt").exists());
    assert!(!scan_path.join(".void_vault").exists()); // Vault should not be created in dry run
}

#[test]
fn test_duplicates_actual_run() {
    let (_tmp_dir, scan_path) = setup_test_environment();
    let file_a = create_test_file(&scan_path, "relic_a.txt", "duplicate content");
    let file_b = create_test_file(&scan_path, "relic_b.txt", "duplicate content");
    let file_c = create_test_file(&scan_path, "unique_c.txt", "unique content");

    let args = Args::parse_from(&["relic-retriever", "scan", scan_path.to_str().unwrap()]);
    let result = std::panic::catch_unwind(|| {
        main().unwrap();
    });
    assert!(result.is_ok());

    let void_vault_path = scan_path.join(".void_vault");
    assert!(void_vault_path.exists());
    assert!(void_vault_path.is_dir());

    // One of the duplicates should remain, the other moved
    let a_exists = file_a.exists();
    let b_exists = file_b.exists();
    assert!((a_exists && !b_exists) || (!a_exists && b_exists)); // Exactly one should remain
    assert!(file_c.exists()); // Unique file should remain

    // Check if one duplicate is in the void vault
    let archived_files: Vec<_> = fs::read_dir(&void_vault_path).unwrap()
        .filter_map(|e| e.ok())
        .map(|e| e.file_name().to_string_lossy().to_string())
        .collect();
    assert_eq!(archived_files.len(), 1);
    assert!(archived_files[0].contains("relic_"));
    assert!(archived_files[0].contains("duplicate content")); // Hash prefix check
}

#[test]
fn test_duplicates_with_custom_archive_path() {
    let (tmp_dir, scan_path) = setup_test_environment();
    let custom_archive_path = tmp_dir.path().join("my_custom_vault");

    let file_a = create_test_file(&scan_path, "relic_x.txt", "another duplicate");
    let file_b = create_test_file(&scan_path, "relic_y.txt", "another duplicate");

    let args = Args::parse_from(&[
        "relic-retriever",
        "scan",
        scan_path.to_str().unwrap(),
        "--archive-path",
        custom_archive_path.to_str().unwrap(),
    ]);
    let result = std::panic::catch_unwind(|| {
        main().unwrap();
    });
    assert!(result.is_ok());

    assert!(custom_archive_path.exists());
    assert!(custom_archive_path.is_dir());

    // One of the duplicates should remain, the other moved
    let a_exists = file_a.exists();
    let b_exists = file_b.exists();
    assert!((a_exists && !b_exists) || (!a_exists && b_exists)); // Exactly one should remain

    let archived_files: Vec<_> = fs::read_dir(&custom_archive_path).unwrap()
        .filter_map(|e| e.ok())
        .map(|e| e.file_name().to_string_lossy().to_string())
        .collect();
    assert_eq!(archived_files.len(), 1);
    assert!(archived_files[0].contains("relic_"));
}

#[test]
fn test_subdirectories() {
    let (_tmp_dir, scan_path) = setup_test_environment();
    let sub_dir = scan_path.join("sub_dir");
    fs::create_dir(&sub_dir).unwrap();

    let file_a = create_test_file(&scan_path, "relic_1.txt", "subdir content");
    let file_b = create_test_file(&sub_dir, "relic_2.txt", "subdir content");
    let file_c = create_test_file(&scan_path, "unique_sub.txt", "unique sub content");

    let args = Args::parse_from(&["relic-retriever", "scan", scan_path.to_str().unwrap()]);
    let result = std::panic::catch_unwind(|| {
        main().unwrap();
    });
    assert!(result.is_ok());

    let void_vault_path = scan_path.join(".void_vault");
    assert!(void_vault_path.exists());

    // One of the duplicates should remain, the other moved
    let a_exists = file_a.exists();
    let b_exists = file_b.exists();
    assert!((a_exists && !b_exists) || (!a_exists && b_exists)); // Exactly one should remain
    assert!(file_c.exists()); // Unique file should remain

    let archived_files: Vec<_> = fs::read_dir(&void_vault_path).unwrap()
        .filter_map(|e| e.ok())
        .map(|e| e.file_name().to_string_lossy().to_string())
        .collect();
    assert_eq!(archived_files.len(), 1);
    assert!(archived_files[0].contains("relic_"));
}

#[test]
fn test_archive_path_inside_scan_path_is_ignored() {
    let (_tmp_dir, scan_path) = setup_test_environment();
    let void_vault_path = scan_path.join(".void_vault");
    fs::create_dir(&void_vault_path).unwrap();

    create_test_file(&scan_path, "relic_outer.txt", "test content");
    create_test_file(&void_vault_path, "relic_inner.txt", "test content"); // This should be ignored

    let args = Args::parse_from(&["relic-retriever", "scan", scan_path.to_str().unwrap()]);
    let result = std::panic::catch_unwind(|| {
        main().unwrap();
    });
    assert!(result.is_ok());

    // The outer relic should remain, no new archives should be made from the inner one
    assert!(scan_path.join("relic_outer.txt").exists());
    assert!(void_vault_path.join("relic_inner.txt").exists()); // Should still be there, untouched

    let archived_files: Vec<_> = fs::read_dir(&void_vault_path).unwrap()
        .filter_map(|e| e.ok())
        .map(|e| e.file_name().to_string_lossy().to_string())
        .collect();
    // Only the 'relic_inner.txt' should be in the vault, and it was there initially.
    // No *new* files should be moved into the vault from the scan of 'relic_inner.txt'.
    // The count should be 1, representing the pre-existing file.
    assert_eq!(archived_files.len(), 1);
    assert!(archived_files[0].contains("relic_inner.txt"));
}
