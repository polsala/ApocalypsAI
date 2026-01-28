use std::fs::{self, File};
use std::io::Write;
use std::process::Command;
use tempfile::tempdir; // # Mock rationale: Using tempfile to create isolated, deterministic, and offline test environments for file system operations.

#[test]
fn test_no_duplicates() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    File::create(path.join("file1.txt"))?.write_all(b"content1")?;
    File::create(path.join("file2.txt"))?.write_all(b"content2")?;

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-echo-purger"))
        .arg(path)
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("No data echoes detected. Your digital wasteland is pristine!"));
    assert!(!stdout.contains("Found")); // Ensure no duplicates reported

    dir.close()?;
    Ok(())
}

#[test]
fn test_duplicates_found_dry_run() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    File::create(path.join("file_a.txt"))?.write_all(b"common_content")?;
    File::create(path.join("file_b.txt"))?.write_all(b"common_content")?;
    File::create(path.join("file_c.txt"))?.write_all(b"unique_content")?;

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-echo-purger"))
        .arg(path)
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Found 1 data echoes for hash"));
    assert!(stdout.contains(format!("Original (kept): {}", path.join("file_a.txt").display()).as_str()) ||
            stdout.contains(format!("Original (kept): {}", path.join("file_b.txt").display()).as_str()));
    assert!(stdout.contains(format!("Duplicate: {}", path.join("file_a.txt").display()).as_str()) ||
            stdout.contains(format!("Duplicate: {}", path.join("file_b.txt").display()).as_str()));
    assert!(stdout.contains("Dry run mode: No files will be deleted."));
    assert!(!stdout.contains("PURGED"));

    // Verify files still exist
    assert!(path.join("file_a.txt").exists());
    assert!(path.join("file_b.txt").exists());
    assert!(path.join("file_c.txt").exists());

    dir.close()?;
    Ok(())
}

#[test]
fn test_duplicates_deleted() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    File::create(path.join("original.txt"))?.write_all(b"content_to_delete")?;
    File::create(path.join("duplicate1.txt"))?.write_all(b"content_to_delete")?;
    File::create(path.join("duplicate2.txt"))?.write_all(b"content_to_delete")?;
    File::create(path.join("unique.txt"))?.write_all(b"unique_stuff")?;

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-echo-purger"))
        .arg("--delete")
        .arg(path)
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Found 2 data echoes for hash"));
    assert!(stdout.contains("PURGED:"));
    assert!(stdout.contains("Echoes purged! Your digital realm is a bit lighter."));

    // Verify one original and unique file exist, duplicates are gone
    let mut existing_files = Vec::new();
    if path.join("original.txt").exists() { existing_files.push("original.txt"); }
    if path.join("duplicate1.txt").exists() { existing_files.push("duplicate1.txt"); }
    if path.join("duplicate2.txt").exists() { existing_files.push("duplicate2.txt"); }
    if path.join("unique.txt").exists() { existing_files.push("unique.txt"); }

    assert_eq!(existing_files.len(), 2, "Expected 2 files to remain (1 original, 1 unique)");
    assert!(existing_files.contains(&"unique.txt"));
    assert!(existing_files.contains(&"original.txt") || existing_files.contains(&"duplicate1.txt") || existing_files.contains(&"duplicate2.txt")); // One of the duplicates might be kept as original, depending on walkdir order.

    // More robust check: count files with the specific content
    let mut remaining_content_files = 0;
    for entry in fs::read_dir(path)? {
        let entry = entry?;
        if entry.file_type()?.is_file() {
            let content = fs::read_to_string(entry.path())?;
            if content == "content_to_delete" {
                remaining_content_files += 1;
            }
        }
    }
    assert_eq!(remaining_content_files, 1, "Expected only one file with 'content_to_delete' to remain.");
    assert!(path.join("unique.txt").exists());


    dir.close()?;
    Ok(())
}

#[test]
fn test_multiple_paths() -> Result<(), Box<dyn std::error::Error>> {
    let dir1 = tempdir()?;
    let path1 = dir1.path();
    let dir2 = tempdir()?;
    let path2 = dir2.path();

    File::create(path1.join("file_x.txt"))?.write_all(b"shared_content")?;
    File::create(path2.join("file_y.txt"))?.write_all(b"shared_content")?;
    File::create(path1.join("file_z.txt"))?.write_all(b"unique_content")?;

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-echo-purger"))
        .arg(path1)
        .arg(path2)
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Found 1 data echoes for hash"));
    assert!(stdout.contains(format!("Original (kept): {}", path1.join("file_x.txt").display()).as_str()) ||
            stdout.contains(format!("Original (kept): {}", path2.join("file_y.txt").display()).as_str()));
    assert!(stdout.contains(format!("Duplicate: {}", path1.join("file_x.txt").display()).as_str()) ||
            stdout.contains(format!("Duplicate: {}", path2.join("file_y.txt").display()).as_str()));
    assert!(stdout.contains("Dry run mode: No files will be deleted."));

    dir1.close()?;
    dir2.close()?;
    Ok(())
}

#[test]
fn test_verbose_output() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    File::create(path.join("verbose_file.txt"))?.write_all(b"verbose_content")?;

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-echo-purger"))
        .arg("-v")
        .arg(path)
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Scanning for data echoes in:"));
    assert!(stdout.contains(format!("Scanning file: {}", path.join("verbose_file.txt").display()).as_str()));
    assert!(stdout.contains("Dry run mode: No files will be deleted."));

    dir.close()?;
    Ok(())
}
