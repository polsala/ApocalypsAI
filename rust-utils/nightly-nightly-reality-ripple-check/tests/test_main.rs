use super::find_ripples;
use tempfile::{tempdir, TempDir};
use std::collections::HashSet;
use std::io::Write;
use std::fs;
use std::path::PathBuf;

// Helper to create a temporary directory with files
fn setup_test_dir(files: &[(&str, &str)]) -> Result<TempDir, Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    for (path, content) in files {
        let file_path = dir.path().join(path);
        if let Some(parent) = file_path.parent() {
            fs::create_dir_all(parent)?;
        }
        let mut file = fs::File::create(&file_path)?;
        file.write_all(content.as_bytes())?;
    }
    Ok(dir)
}

#[test]
fn test_no_ripples_identical_dirs() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Using tempfile to create isolated, deterministic file system states for testing.
    // This avoids reliance on actual user files or network, ensuring offline and repeatable tests.
    let dir1 = setup_test_dir(
        &[
            ("file1.txt", "content A"),
            ("subdir/file2.txt", "content B"),
        ],
    )?;
    let dir2 = setup_test_dir(
        &[
            ("file1.txt", "content A"),
            ("subdir/file2.txt", "content B"),
        ],
    )?;

    let base_dirs = vec![dir1.path().to_path_buf(), dir2.path().to_path_buf()];
    let result = find_ripples(&base_dirs)?;

    // Expect no content differences or missing files
    assert_eq!(result.len(), 2); // Two files in total
    for (_relative_path, dir_hashes) in result {
        assert_eq!(dir_hashes.len(), 2); // Present in both dirs
        let unique_hashes: HashSet<&String> = dir_hashes.values().collect();
        assert_eq!(unique_hashes.len(), 1); // Only one unique hash (identical content)
    }

    Ok(())
}

#[test]
fn test_ripple_different_content() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Using tempfile to create isolated, deterministic file system states for testing.
    // This avoids reliance on actual user files or network, ensuring offline and repeatable tests.
    let dir1 = setup_test_dir(
        &[
            ("file1.txt", "content A"),
            ("subdir/file2.txt", "content B"),
        ],
    )?;
    let dir2 = setup_test_dir(
        &[
            ("file1.txt", "content A - modified"), // Different content
            ("subdir/file2.txt", "content B"),
        ],
    )?;

    let base_dirs = vec![dir1.path().to_path_buf(), dir2.path().to_path_buf()];
    let result = find_ripples(&base_dirs)?;

    let file1_relative_path = PathBuf::from("file1.txt");
    let file2_relative_path = PathBuf::from("subdir/file2.txt");

    assert!(result.contains_key(&file1_relative_path));
    assert!(result.contains_key(&file2_relative_path));

    // Check file1.txt for content ripple
    let file1_hashes = result.get(&file1_relative_path).unwrap();
    assert_eq!(file1_hashes.len(), 2); // Present in both
    let unique_file1_hashes: HashSet<&String> = file1_hashes.values().collect();
    assert_eq!(unique_file1_hashes.len(), 2); // Expect two different hashes

    // Check file2.txt for no ripple
    let file2_hashes = result.get(&file2_relative_path).unwrap();
    assert_eq!(file2_hashes.len(), 2); // Present in both
    let unique_file2_hashes: HashSet<&String> = file2_hashes.values().collect();
    assert_eq!(unique_file2_hashes.len(), 1); // Expect one unique hash

    Ok(())
}

#[test]
fn test_ripple_missing_file() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Using tempfile to create isolated, deterministic file system states for testing.
    // This avoids reliance on actual user files or network, ensuring offline and repeatable tests.
    let dir1 = setup_test_dir(
        &[
            ("file1.txt", "content A"),
            ("subdir/file2.txt", "content B"),
        ],
    )?;
    let dir2 = setup_test_dir(
        &[
            ("subdir/file2.txt", "content B"), // file1.txt is missing here
        ],
    )?;

    let base_dirs = vec![dir1.path().to_path_buf(), dir2.path().to_path_buf()];
    let result = find_ripples(&base_dirs)?;

    let file1_relative_path = PathBuf::from("file1.txt");
    let file2_relative_path = PathBuf::from("subdir/file2.txt");

    assert!(result.contains_key(&file1_relative_path));
    assert!(result.contains_key(&file2_relative_path));

    // Check file1.txt for missing ripple
    let file1_hashes = result.get(&file1_relative_path).unwrap();
    assert_eq!(file1_hashes.len(), 1); // Only present in one directory

    // Check file2.txt for no ripple
    let file2_hashes = result.get(&file2_relative_path).unwrap();
    assert_eq!(file2_hashes.len(), 2); // Present in both
    let unique_file2_hashes: HashSet<&String> = file2_hashes.values().collect();
    assert_eq!(unique_file2_hashes.len(), 1);

    Ok(())
}

#[test]
fn test_empty_directories() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Using tempfile to create isolated, deterministic file system states for testing.
    // This avoids reliance on actual user files or network, ensuring offline and repeatable tests.
    let dir1 = tempdir()?;
    let dir2 = tempdir()?;

    let base_dirs = vec![dir1.path().to_path_buf(), dir2.path().to_path_buf()];
    let result = find_ripples(&base_dirs)?;

    assert!(result.is_empty()); // No files, no ripples

    Ok(())
}

#[test]
fn test_non_existent_directory_error() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Testing error handling for non-existent directories.
    let dir1 = tempdir()?;
    let non_existent_dir = PathBuf::from("non_existent_path_12345");

    let base_dirs = vec![dir1.path().to_path_buf(), non_existent_dir];
    let result = find_ripples(&base_dirs);

    assert!(result.is_err());
    assert!(result.unwrap_err().to_string().contains("Directory not found"));

    Ok(())
}

#[test]
fn test_multiple_ripples() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Using tempfile to create isolated, deterministic file system states for testing.
    // This avoids reliance on actual user files or network, ensuring offline and repeatable tests.
    let dir1 = setup_test_dir(
        &[
            ("file_a.txt", "content A"),
            ("file_b.txt", "content B"),
            ("file_c.txt", "content C"),
        ],
    )?;
    let dir2 = setup_test_dir(
        &[
            ("file_a.txt", "content A_modified"), // Content ripple
            ("file_c.txt", "content C"),
            ("file_d.txt", "content D"), // Missing in dir1
        ],
    )?;

    let base_dirs = vec![dir1.path().to_path_buf(), dir2.path().to_path_buf()];
    let result = find_ripples(&base_dirs)?;

    // file_a.txt should have content ripple
    let file_a_hashes = result.get(&PathBuf::from("file_a.txt")).unwrap();
    assert_eq!(file_a_hashes.len(), 2);
    assert_eq!(file_a_hashes.values().collect::<HashSet<_>>().len(), 2);

    // file_b.txt should be missing in dir2
    let file_b_hashes = result.get(&PathBuf::from("file_b.txt")).unwrap();
    assert_eq!(file_b_hashes.len(), 1);

    // file_c.txt should have no ripple
    let file_c_hashes = result.get(&PathBuf::from("file_c.txt")).unwrap();
    assert_eq!(file_c_hashes.len(), 2);
    assert_eq!(file_c_hashes.values().collect::<HashSet<_>>().len(), 1);

    // file_d.txt should be missing in dir1
    let file_d_hashes = result.get(&PathBuf::from("file_d.txt")).unwrap();
    assert_eq!(file_d_hashes.len(), 1);

    Ok(())
}
