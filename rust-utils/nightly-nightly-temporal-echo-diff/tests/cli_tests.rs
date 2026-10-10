use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;
use std::fs;
use std::path::PathBuf;

// Mock rationale: These tests use `tempfile::tempdir()` to create isolated, temporary directories
// for storing test files and their echoes. This ensures that tests are deterministic, do not
// interfere with the actual user's home directory or existing echoes, and clean up after themselves.
// File system operations are performed on these temporary paths, effectively mocking the real
// file system interactions for the purpose of testing the CLI logic.

#[test]
fn test_create_and_diff_no_changes() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let file_path = temp_dir.path().join("test_file.txt");
    fs::write(&file_path, "line 1\nline 2\n")?;

    // Set HOME env var to temp_dir for echo storage
    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());

    // Create echo
    cmd.arg("create").arg(&file_path).assert().success()
        .stdout(predicates::str::contains(format!("Echo created for: {}", file_path.display())));

    // Diff with no changes
    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());
    cmd.arg("diff").arg(&file_path).assert().success()
        .stdout(predicates::str::contains("No changes detected"));

    Ok(())
}

#[test]
fn test_create_and_diff_with_changes() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let file_path = temp_dir.path().join("test_file.txt");
    fs::write(&file_path, "line 1\nline 2\nline 3\n")?;

    // Set HOME env var to temp_dir for echo storage
    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());

    // Create echo
    cmd.arg("create").arg(&file_path).assert().success();

    // Modify file
    fs::write(&file_path, "line 1\nNEW line 2\nline 4\n")?;

    // Diff with changes
    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());
    cmd.arg("diff").arg(&file_path).assert().success()
        .stdout(predicates::str::contains("- line 2"))
        .stdout(predicates::str::contains("+ NEW line 2"))
        .stdout(predicates::str::contains("- line 3"))
        .stdout(predicates::str::contains("+ line 4"));

    Ok(())
}

#[test]
fn test_diff_non_existent_echo() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let file_path = temp_dir.path().join("non_existent_echo.txt");
    fs::write(&file_path, "some content")?;

    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());
    cmd.arg("diff").arg(&file_path).assert().success()
        .stdout(predicates::str::contains("No echo found for:"));

    Ok(())
}

#[test]
fn test_list_echoes() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let file1_path = temp_dir.path().join("file1.txt");
    let file2_path = temp_dir.path().join("file2.txt");
    fs::write(&file1_path, "content1")?;
    fs::write(&file2_path, "content2")?;

    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());
    cmd.arg("create").arg(&file1_path).assert().success();

    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());
    cmd.arg("create").arg(&file2_path).assert().success();

    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());
    cmd.arg("list").assert().success()
        .stdout(predicates::str::contains(".echo").count(2)); // Expect two echo files listed

    Ok(())
}

#[test]
fn test_clean_specific_echo() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let file_path = temp_dir.path().join("to_clean.txt");
    fs::write(&file_path, "content")?;

    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());
    cmd.arg("create").arg(&file_path).assert().success();

    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());
    cmd.arg("clean").arg(&file_path).assert().success()
        .stdout(predicates::str::contains(format!("Echo removed for: {}", file_path.display())));

    // Verify it's gone by trying to diff (should say no echo found)
    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());
    cmd.arg("diff").arg(&file_path).assert().success()
        .stdout(predicates::str::contains("No echo found for:"));

    Ok(())
}

#[test]
fn test_clean_all_echoes() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let file1_path = temp_dir.path().join("file1.txt");
    let file2_path = temp_dir.path().join("file2.txt");
    fs::write(&file1_path, "content1")?;
    fs::write(&file2_path, "content2")?;

    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());
    cmd.arg("create").arg(&file1_path).assert().success();

    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());
    cmd.arg("create").arg(&file2_path).assert().success();

    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());
    cmd.arg("clean-all").assert().success()
        .stdout(predicates::str::contains("All temporal echoes removed."));

    // Verify echo directory is gone
    let echo_root = temp_dir.path().join(".temporal_echoes");
    assert!(!echo_root.exists());

    Ok(())
}

#[test]
fn test_create_non_existent_file() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let file_path = temp_dir.path().join("non_existent.txt");

    let mut cmd = Command::cargo_bin("nightly-temporal-echo-diff")?;
    cmd.env("HOME", temp_dir.path());
    cmd.arg("create").arg(&file_path).assert().failure()
        .stderr(predicates::str::contains("File not found"));

    Ok(())
}
