// tests/integration_tests.rs
use std::{
    fs,
    io::{self, Write},
    path::{Path, PathBuf},
    process::Command,
    time::Duration,
};
use tempfile::tempdir;

// Helper to get the path to the compiled binary
fn get_binary_path() -> PathBuf {
    assert!(env!("CARGO_BIN_EXE_nightly-digital-tremor-scan").len() > 0);
    PathBuf::from(env!("CARGO_BIN_EXE_nightly-digital-tremor-scan"))
}

// Helper to run the CLI command
fn run_command(args: &[&str]) -> String {
    let output = Command::new(get_binary_path())
        .args(args)
        .output()
        .expect("Failed to execute command");

    if !output.status.success() {
        eprintln!("Command failed: {:?}", args);
        eprintln!("Stdout: {}", String::from_utf8_lossy(&output.stdout));
        eprintln!("Stderr: {}", String::from_utf8_lossy(&output.stderr));
        panic!("Command failed with status: {}", output.status);
    }
    String::from_utf8_lossy(&output.stdout).into_owned()
}

#[test]
fn test_snapshot_and_no_tremors() -> io::Result<()> {
    // Mock rationale: Using tempdir and creating files programmatically ensures a clean, isolated, and deterministic test environment.
    let dir = tempdir()?;
    let path = dir.path();
    let snapshot_file = path.join("snapshot.json");

    // Create some files
    fs::write(path.join("file1.txt"), "hello")?;
    fs::create_dir(path.join("subdir"))?;
    fs::write(path.join("subdir/file2.txt"), "world")?;

    // 1. Create snapshot
    let output = run_command(&[
        "snapshot",
        "--path",
        path.to_str().unwrap(),
        "--output",
        snapshot_file.to_str().unwrap(),
    ]);
    assert!(output.contains("Snapshot saved to"));
    assert!(snapshot_file.exists());

    // 2. Detect tremors (should be none)
    let output = run_command(&[
        "detect",
        "--path",
        path.to_str().unwrap(),
        "--snapshot",
        snapshot_file.to_str().unwrap(),
    ]);
    assert!(output.contains("No tremors detected. The digital landscape is calm."));

    Ok(())
}

#[test]
fn test_new_file_tremor() -> io::Result<()> {
    // Mock rationale: Using tempdir and creating files programmatically ensures a clean, isolated, and deterministic test environment.
    let dir = tempdir()?;
    let path = dir.path();
    let snapshot_file = path.join("snapshot.json");

    fs::write(path.join("file1.txt"), "initial")?;

    // Create initial snapshot
    run_command(&[
        "snapshot",
        "--path",
        path.to_str().unwrap(),
        "--output",
        snapshot_file.to_str().unwrap(),
    ]);

    // Add a new file
    fs::write(path.join("new_file.txt"), "content")?;

    // Detect tremors
    let output = run_command(&[
        "detect",
        "--path",
        path.to_str().unwrap(),
        "--snapshot",
        snapshot_file.to_str().unwrap(),
    ]);
    assert!(output.contains("--- DIGITAL TREMORS DETECTED! ---"));
    assert!(output.contains("[NEW]    'new_file.txt'"));

    Ok(())
}

#[test]
fn test_missing_file_tremor() -> io::Result<()> {
    // Mock rationale: Using tempdir and creating files programmatically ensures a clean, isolated, and deterministic test environment.
    let dir = tempdir()?;
    let path = dir.path();
    let snapshot_file = path.join("snapshot.json");
    let file_to_delete = path.join("to_delete.txt");

    fs::write(path.join("file1.txt"), "initial")?;
    fs::write(&file_to_delete, "delete me")?;

    // Create initial snapshot
    run_command(&[
        "snapshot",
        "--path",
        path.to_str().unwrap(),
        "--output",
        snapshot_file.to_str().unwrap(),
    ]);

    // Delete a file
    fs::remove_file(&file_to_delete)?;

    // Detect tremors
    let output = run_command(&[
        "detect",
        "--path",
        path.to_str().unwrap(),
        "--snapshot",
        snapshot_file.to_str().unwrap(),
    ]);
    assert!(output.contains("--- DIGITAL TREMORS DETECTED! ---"));
    assert!(output.contains("[MISSING] 'to_delete.txt'"));

    Ok(())
}

#[test]
#[cfg(unix)] // Permissions are Unix-specific
fn test_permission_change_tremor() -> io::Result<()> {
    // Mock rationale: Using tempdir and creating files programmatically ensures a clean, isolated, and deterministic test environment.
    let dir = tempdir()?;
    let path = dir.path();
    let snapshot_file = path.join("snapshot.json");
    let target_file = path.join("perms.txt");

    fs::write(&target_file, "content")?;
    // Set initial permissions (e.g., 644)
    use std::os::unix::fs::PermissionsExt;
    fs::set_permissions(&target_file, fs::Permissions::from_mode(0o644))?;

    // Create initial snapshot
    run_command(&[
        "snapshot",
        "--path",
        path.to_str().unwrap(),
        "--output",
        snapshot_file.to_str().unwrap(),
    ]);

    // Change permissions (e.g., to 755)
    fs::set_permissions(&target_file, fs::Permissions::from_mode(0o755))?;

    // Detect tremors
    let output = run_command(&[
        "detect",
        "--path",
        path.to_str().unwrap(),
        "--snapshot",
        snapshot_file.to_str().unwrap(),
    ]);
    assert!(output.contains("--- DIGITAL TREMORS DETECTED! ---"));
    assert!(output.contains("Field 'permissions' changed from '644' to '755'"));

    Ok(())
}

#[test]
fn test_size_change_tremor() -> io::Result<()> {
    // Mock rationale: Using tempdir and creating files programmatically ensures a clean, isolated, and deterministic test environment.
    let dir = tempdir()?;
    let path = dir.path();
    let snapshot_file = path.join("snapshot.json");
    let target_file = path.join("size.txt");

    fs::write(&target_file, "small")?;

    // Create initial snapshot
    run_command(&[
        "snapshot",
        "--path",
        path.to_str().unwrap(),
        "--output",
        snapshot_file.to_str().unwrap(),
    ]);

    // Change file content (and thus size)
    fs::write(&target_file, "much larger content now")?;

    // Detect tremors
    let output = run_command(&[
        "detect",
        "--path",
        path.to_str().unwrap(),
        "--snapshot",
        snapshot_file.to_str().unwrap(),
    ]);
    assert!(output.contains("--- DIGITAL TREMORS DETECTED! ---"));
    assert!(output.contains("Field 'size' changed from '5' to '23'")); // "small" is 5 bytes, "much larger content now" is 23 bytes

    Ok(())
}

#[test]
fn test_modified_time_change_tremor() -> io::Result<()> {
    // Mock rationale: Using tempdir and creating files programmatically ensures a clean, isolated, and deterministic test environment.
    let dir = tempdir()?;
    let path = dir.path();
    let snapshot_file = path.join("snapshot.json");
    let target_file = path.join("mtime.txt");

    fs::write(&target_file, "content")?;

    // Create initial snapshot
    run_command(&[
        "snapshot",
        "--path",
        path.to_str().unwrap(),
        "--output",
        snapshot_file.to_str().unwrap(),
    ]);

    // Wait a bit, then touch the file to update mtime
    std::thread::sleep(Duration::from_millis(100)); // Ensure mtime changes
    filetime::set_file_mtime(&target_file, filetime::FileTime::now())?;

    // Detect tremors
    let output = run_command(&[
        "detect",
        "--path",
        path.to_str().unwrap(),
        "--snapshot",
        snapshot_file.to_str().unwrap(),
    ]);
    assert!(output.contains("--- DIGITAL TREMORS DETECTED! ---"));
    assert!(output.contains("Field 'modified_time' changed from")); // The exact time string will vary
    assert!(!output.contains("to ''")); // Ensure it shows both old and new

    Ok(())
}
