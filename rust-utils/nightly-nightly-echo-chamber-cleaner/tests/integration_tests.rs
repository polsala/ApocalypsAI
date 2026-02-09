use std::fs;
use std::io::{self, Write};
use std::path::{Path, PathBuf};
use tempfile::tempdir;

// Mock rationale: We need to test file system operations. Creating temporary directories and files
// is a standard and deterministic way to mock the file system for integration tests without
// touching the actual user's file system. This ensures tests are isolated and repeatable.

// Import the main functions to test
use echo_chamber_cleaner::{find_duplicates, harmonize_duplicates, Action};

// Helper to create a file with specific content
fn create_file(dir: &Path, name: &str, content: &str) -> io::Result<PathBuf> {
    let path = dir.join(name);
    let mut file = fs::File::create(&path)?;
    file.write_all(content.as_bytes())?;
    Ok(path)
}

#[test]
fn test_find_duplicates_no_duplicates() -> io::Result<()> {
    let dir = tempdir()?;
    let root = dir.path();

    create_file(root, "file1.txt", "content A")?;
    create_file(root, "file2.txt", "content B")?;
    create_file(root, "file3.txt", "content C")?;

    let duplicates = find_duplicates(root, false)?;
    assert!(duplicates.is_empty());

    Ok(())
}

#[test]
fn test_find_duplicates_with_duplicates() -> io::Result<()> {
    let dir = tempdir()?;
    let root = dir.path();

    create_file(root, "file1.txt", "content A")?;
    create_file(root, "file2.txt", "content B")?;
    create_file(root, "file3.txt", "content A")?;
    create_file(root, "file4.txt", "content C")?;
    create_file(root, "file5.txt", "content B")?;

    let duplicates = find_duplicates(root, false)?;
    assert_eq!(duplicates.len(), 2); // Two groups of duplicates (A and B)

    let mut found_a = false;
    let mut found_b = false;

    for (_, paths) in duplicates {
        if paths.len() == 2 {
            let p1 = paths[0].file_name().unwrap().to_str().unwrap();
            let p2 = paths[1].file_name().unwrap().to_str().unwrap();
            if (p1 == "file1.txt" && p2 == "file3.txt") || (p1 == "file3.txt" && p2 == "file1.txt") {
                found_a = true;
            } else if (p1 == "file2.txt" && p2 == "file5.txt") || (p1 == "file5.txt" && p2 == "file2.txt") {
                found_b = true;
            }
        }
    }
    assert!(found_a);
    assert!(found_b);

    Ok(())
}

#[test]
fn test_harmonize_duplicates_delete() -> io::Result<()> {
    let dir = tempdir()?;
    let root = dir.path();

    let path1 = create_file(root, "original.txt", "content A")?;
    let path2 = create_file(root, "duplicate1.txt", "content A")?;
    let path3 = create_file(root, "duplicate2.txt", "content A")?;
    create_file(root, "unique.txt", "content B")?;

    let duplicates = find_duplicates(root, false)?;
    assert_eq!(duplicates.len(), 1);

    harmonize_duplicates(duplicates, Action::Delete, false, false)?;

    // Check if original.txt and unique.txt still exist
    assert!(path1.exists());
    assert!(root.join("unique.txt").exists());

    // Check if duplicates are deleted
    assert!(!path2.exists());
    assert!(!path3.exists());

    // Only 2 files should remain
    let remaining_files: Vec<_> = fs::read_dir(root)?.filter_map(|e| e.ok()).filter(|e| e.file_type().unwrap().is_file()).collect();
    assert_eq!(remaining_files.len(), 2);

    Ok(())
}

#[test]
fn test_harmonize_duplicates_link() -> io::Result<()> {
    let dir = tempdir()?;
    let root = dir.path();

    let path1 = create_file(root, "original.txt", "content A")?;
    let path2 = create_file(root, "duplicate1.txt", "content A")?;
    let path3 = create_file(root, "duplicate2.txt", "content A")?;
    create_file(root, "unique.txt", "content B")?;

    let duplicates = find_duplicates(root, false)?;
    assert_eq!(duplicates.len(), 1);

    harmonize_duplicates(duplicates, Action::Link, false, false)?;

    // Check if original.txt and unique.txt still exist
    assert!(path1.exists());
    assert!(root.join("unique.txt").exists());

    // Check if duplicates are replaced by hard links
    assert!(path2.exists());
    assert!(path3.exists());

    // Verify they are hard links to the original
    let metadata1 = fs::metadata(&path1)?;
    let metadata2 = fs::metadata(&path2)?;
    let metadata3 = fs::metadata(&path3)?;

    // Inode numbers should be the same for hard-linked files
    assert_eq!(metadata1.ino(), metadata2.ino());
    assert_eq!(metadata1.ino(), metadata3.ino());

    // All 4 files should still exist, but 2 are links
    let remaining_files: Vec<_> = fs::read_dir(root)?.filter_map(|e| e.ok()).filter(|e| e.file_type().unwrap().is_file()).collect();
    assert_eq!(remaining_files.len(), 4);

    Ok(())
}

#[test]
fn test_harmonize_duplicates_dry_run() -> io::Result<()> {
    let dir = tempdir()?;
    let root = dir.path();

    let path1 = create_file(root, "original.txt", "content A")?;
    let path2 = create_file(root, "duplicate1.txt", "content A")?;
    create_file(root, "unique.txt", "content B")?;

    let duplicates = find_duplicates(root, false)?;
    assert_eq!(duplicates.len(), 1);

    harmonize_duplicates(duplicates, Action::Delete, true, false)?;

    // In dry run, no files should be deleted or linked
    assert!(path1.exists());
    assert!(path2.exists());
    assert!(root.join("unique.txt").exists());

    let remaining_files: Vec<_> = fs::read_dir(root)?.filter_map(|e| e.ok()).filter(|e| e.file_type().unwrap().is_file()).collect();
    assert_eq!(remaining_files.len(), 3);

    Ok(())
}

#[test]
fn test_find_duplicates_nested_directories() -> io::Result<()> {
    let dir = tempdir()?;
    let root = dir.path();

    let sub_dir = root.join("sub");
    fs::create_dir(&sub_dir)?;

    create_file(root, "file1.txt", "content A")?;
    create_file(&sub_dir, "file2.txt", "content B")?;
    create_file(&sub_dir, "file3.txt", "content A")?;

    let duplicates = find_duplicates(root, false)?;
    assert_eq!(duplicates.len(), 1);

    let paths = duplicates.into_iter().next().unwrap().1;
    assert_eq!(paths.len(), 2);
    assert!(paths.iter().any(|p| p.file_name().unwrap() == "file1.txt"));
    assert!(paths.iter().any(|p| p.file_name().unwrap() == "file3.txt"));

    Ok(())
}
