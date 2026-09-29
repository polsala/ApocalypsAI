use tempfile::{tempdir, NamedTempFile};
use std::io::Write;
use std::fs;
use std::process::Command; // To run the compiled binary

// Mock rationale: We create temporary files and directories to simulate a file system
// without touching the actual user's file system or relying on external services.
// This makes tests deterministic and isolated.

#[test]
fn test_dry_run_finds_dust() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create some dust files
    let mut file1 = NamedTempFile::new_in(path)?;
    file1.write_all(b"small file")?; // 10 bytes
    let mut file2 = NamedTempFile::new_in(path)?;
    file2.write_all(b"tiny")?; // 4 bytes

    // Create a large file that shouldn't be dust
    let mut large_file = NamedTempFile::new_in(path)?;
    large_file.write_all(&vec![0; 2000])?; // 2KB

    // Create a subdirectory with dust
    let subdir = path.join("subdir");
    fs::create_dir(&subdir)?;
    let mut file3 = NamedTempFile::new_in(&subdir)?;
    file3.write_all(b"sub dust")?; // 8 bytes

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-cosmic-dust-collector"))
        .arg("--path")
        .arg(path)
        .arg("--max-size")
        .arg("1KB")
        .arg("--dry-run")
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Cosmic Dust Report"));
    assert!(stdout.contains("Total cosmic dust files found: 3"));
    assert!(stdout.contains("Dry run complete. No files were deleted."));
    assert!(stdout.contains(&file1.path().display().to_string()));
    assert!(stdout.contains(&file2.path().display().to_string()));
    assert!(stdout.contains(&file3.path().display().to_string()));
    assert!(!stdout.contains(&large_file.path().display().to_string())); // Large file should not be reported

    Ok(())
}

#[test]
fn test_delete_dust_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let mut file1 = NamedTempFile::new_in(path)?;
    file1.write_all(b"small file to delete")?;
    let file1_path = file1.path().to_path_buf();

    let mut file2 = NamedTempFile::new_in(path)?;
    file2.write_all(b"another small file")?;
    let file2_path = file2.path().to_path_buf();

    // Ensure files exist before deletion attempt
    assert!(file1_path.exists());
    assert!(file2_path.exists());

    // Simulate user input "yes" for confirmation
    let input = b"yes\n";

    let mut cmd = Command::new(env!("CARGO_BIN_EXE_nightly-cosmic-dust-collector"));
    cmd.arg("--path")
        .arg(path)
        .arg("--max-size")
        .arg("1KB")
        .arg("--delete")
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .stderr(std::process::Stdio::piped());

    let mut child = cmd.spawn()?;
    let mut stdin = child.stdin.take().expect("Failed to open stdin");
    stdin.write_all(input)?;
    drop(stdin); // Close stdin to signal EOF

    let output = child.wait_with_output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Successfully deleted 2 files"));
    assert!(!file1_path.exists()); // File should be deleted
    assert!(!file2_path.exists()); // File should be deleted

    Ok(())
}

#[test]
fn test_delete_cancelled() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let mut file1 = NamedTempFile::new_in(path)?;
    file1.write_all(b"small file to keep")?;
    let file1_path = file1.path().to_path_buf();

    assert!(file1_path.exists());

    // Simulate user input "no" for confirmation
    let input = b"no\n";

    let mut cmd = Command::new(env!("CARGO_BIN_EXE_nightly-cosmic-dust-collector"));
    cmd.arg("--path")
        .arg(path)
        .arg("--max-size")
        .arg("1KB")
        .arg("--delete")
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .stderr(std::process::Stdio::piped());

    let mut child = cmd.spawn()?;
    let mut stdin = child.stdin.take().expect("Failed to open stdin");
    stdin.write_all(input)?;
    drop(stdin); // Close stdin to signal EOF

    let output = child.wait_with_output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Deletion cancelled. Cosmic dust remains."));
    assert!(file1_path.exists()); // File should NOT be deleted

    Ok(())
}

#[test]
fn test_no_dust_found() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a large file
    let mut large_file = NamedTempFile::new_in(path)?;
    large_file.write_all(&vec![0; 5000])?; // 5KB

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-cosmic-dust-collector"))
        .arg("--path")
        .arg(path)
        .arg("--max-size")
        .arg("1KB")
        .arg("--dry-run")
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("No cosmic dust found in"));
    assert!(!stdout.contains("Cosmic Dust Report"));

    Ok(())
}

#[test]
fn test_invalid_max_size() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let output = Command::new(env!("CARGO_BIN_EXE_nightly-cosmic-dust-collector"))
        .arg("--path")
        .arg(path)
        .arg("--max-size")
        .arg("invalid_size")
        .arg("--dry-run")
        .output()?;

    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", String::from_utf8_lossy(&output.stdout));
    println!("STDERR:\n{}", stderr);

    assert!(!output.status.success()); // Should fail
    assert!(stderr.contains("Invalid max_size format"));

    Ok(())
}
