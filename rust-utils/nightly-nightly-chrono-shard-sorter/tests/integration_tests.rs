use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};
use std::io::Write;
use tempfile::tempdir;
use nightly_chrono_shard_sorter::sort_chrono_shards;

// Mock rationale: File system operations are mocked by using temporary directories and files created and controlled by the test environment.
// Timestamps are explicitly set using the `filetime` crate for deterministic behavior across different test runs and environments.

#[test]
fn test_sort_and_move_files() -> Result<(), Box<dyn std::error::Error>> {
    let source_dir = tempdir()?;
    let dest_dir = tempdir()?;

    // Define specific modification times for deterministic sorting
    let file1_mod_time = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(1672531200); // Jan 1, 2023 00:00:00 UTC
    let file2_mod_time = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(1674259200); // Jan 21, 2023 00:00:00 UTC
    let file3_mod_time = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(1680220800); // Mar 31, 2023 00:00:00 UTC

    // Create files and set their modification times
    let file1_path = source_dir.path().join("file1.txt");
    fs::File::create(&file1_path)?.write_all(b"content1")?;
    filetime::set_file_mtime(&file1_path, filetime::FileTime::from_system_time(file1_mod_time))?;

    let file2_path = source_dir.path().join("file2.log");
    fs::File::create(&file2_path)?.write_all(b"content2")?;
    filetime::set_file_mtime(&file2_path, filetime::FileTime::from_system_time(file2_mod_time))?;

    let file3_path = source_dir.path().join("report.pdf");
    fs::File::create(&file3_path)?.write_all(b"content3")?;
    filetime::set_file_mtime(&file3_path, filetime::FileTime::from_system_time(file3_mod_time))?;

    // Run the sorter in move mode
    sort_chrono_shards(source_dir.path(), dest_dir.path(), false)?;

    // Assertions for move mode: original files should no longer exist in source
    assert!(!source_dir.path().join("file1.txt").exists());
    assert!(!source_dir.path().join("file2.log").exists());
    assert!(!source_dir.path().join("report.pdf").exists());

    // Assertions for destination: files should be in the correct temporal directories
    assert!(dest_dir.path().join("2023/01/01/file1.txt").exists());
    assert!(dest_dir.path().join("2023/01/21/file2.log").exists());
    assert!(dest_dir.path().join("2023/03/31/report.pdf").exists());

    Ok(())
}

#[test]
fn test_sort_and_copy_files() -> Result<(), Box<dyn std::error::Error>> {
    let source_dir = tempdir()?;
    let dest_dir = tempdir()?;

    let file1_mod_time = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(1672531200); // Jan 1, 2023 00:00:00 UTC
    let file1_path = source_dir.path().join("file1.txt");
    fs::File::create(&file1_path)?.write_all(b"content1")?;
    filetime::set_file_mtime(&file1_path, filetime::FileTime::from_system_time(file1_mod_time))?;

    // Run the sorter in copy mode
    sort_chrono_shards(source_dir.path(), dest_dir.path(), true)?;

    // Assertions for copy mode: original file should still exist in source
    assert!(source_dir.path().join("file1.txt").exists()); 
    assert!(dest_dir.path().join("2023/01/01/file1.txt").exists());

    Ok(())
}

#[test]
fn test_empty_source_directory() -> Result<(), Box<dyn std::error::Error>> {
    let source_dir = tempdir()?;
    let dest_dir = tempdir()?;

    sort_chrono_shards(source_dir.path(), dest_dir.path(), false)?;

    // Destination should be created but remain empty as source was empty
    assert!(dest_dir.path().exists());
    assert!(fs::read_dir(dest_dir.path())?.next().is_none());

    Ok(())
}

#[test]
fn test_file_conflict_resolution() -> Result<(), Box<dyn std::error::Error>> {
    let source_dir = tempdir()?;
    let dest_dir = tempdir()?;

    let common_filename = "duplicate.txt";

    // File 1: Modified Jan 1, 2023
    let file1_mod_time = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(1672531200); 
    let file1_path = source_dir.path().join(common_filename);
    fs::File::create(&file1_path)?.write_all(b"content of file 1")?;
    filetime::set_file_mtime(&file1_path, filetime::FileTime::from_system_time(file1_mod_time))?;

    // Run sorter for file 1 (moves it to dest/2023/01/01/duplicate.txt)
    sort_chrono_shards(source_dir.path(), dest_dir.path(), false)?;

    let expected_path_file1 = dest_dir.path().join("2023/01/01/duplicate.txt");
    assert!(expected_path_file1.exists());
    assert_eq!(fs::read_to_string(&expected_path_file1)?, "content of file 1");

    // File 2: Same name, different content, same modification date (Jan 1, 2023)
    // This will trigger the conflict resolution logic because the target path already exists.
    let file2_mod_time = SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(1672531200); 
    let file2_path = source_dir.path().join(common_filename);
    fs::File::create(&file2_path)?.write_all(b"content of file 2")?;
    filetime::set_file_mtime(&file2_path, filetime::FileTime::from_system_time(file2_mod_time))?;

    // Run sorter for file 2 (should be renamed due to conflict)
    sort_chrono_shards(source_dir.path(), dest_dir.path(), false)?;

    // Assert file 2 is moved and renamed with a timestamp suffix
    let expected_renamed_path_file2 = dest_dir.path().join(format!("2023/01/01/duplicate_{}.txt", file2_mod_time.duration_since(UNIX_EPOCH)?.as_secs()));
    assert!(expected_renamed_path_file2.exists());
    assert_eq!(fs::read_to_string(&expected_renamed_path_file2)?, "content of file 2");

    // Ensure the original file1 (now at expected_path_file1) is still there and not overwritten
    assert!(expected_path_file1.exists());
    assert_eq!(fs::read_to_string(&expected_path_file1)?, "content of file 1");

    Ok(())
}
