use std::process::Command;
use tempfile::tempdir;
use std::fs;
use std::path::Path;

// Mock rationale: `tempfile` crate is used to create isolated, temporary file system
// structures for deterministic and offline testing of file system interactions
// without relying on the actual user's file system state.

#[test]
fn test_cli_finds_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    fs::create_dir_all(path.join("subdir"))?;
    fs::write(path.join("report_q1.txt"), "content")?;
    fs::write(path.join("subdir/config.toml"), "content")?;
    fs::write(path.join("another_file.log"), "content")?;

    let output = Command::new(env!("CARGO_BIN_EXE_echo-locator"))
        .arg("report")
        .arg(path)
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains(&format!("{}", path.join("report_q1.txt").display())));
    assert!(!stdout.contains(&format!("{}", path.join("subdir/config.toml").display())));
    assert!(!stdout.contains(&format!("{}", path.join("another_file.log").display())));

    dir.close()?;
    Ok(())
}

#[test]
fn test_cli_finds_directories() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    fs::create_dir_all(path.join("my_reports"))?;
    fs::create_dir_all(path.join("other_stuff"))?;
    fs::write(path.join("my_reports/data.txt"), "content")?;

    let output = Command::new(env!("CARGO_BIN_EXE_echo-locator"))
        .arg("reports")
        .arg(path)
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains(&format!("{}", path.join("my_reports").display())));
    assert!(!stdout.contains(&format!("{}", path.join("other_stuff").display())));

    dir.close()?;
    Ok(())
}

#[test]
fn test_cli_no_match() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    fs::write(path.join("file.txt"), "content")?;

    let output = Command::new(env!("CARGO_BIN_EXE_echo-locator"))
        .arg("nonexistent")
        .arg(path)
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.is_empty());

    dir.close()?;
    Ok(())
}

#[test]
fn test_cli_default_path() -> Result<(), Box<dyn std::error::Error>> {
    let original_dir = std::env::current_dir()?;
    let temp_test_dir = tempdir()?;
    let temp_test_path = temp_test_dir.path();

    std::env::set_current_dir(temp_test_path)?;

    fs::write(temp_test_path.join("default_file.txt"), "content")?;

    let output = Command::new(env!("CARGO_BIN_EXE_echo-locator"))
        .arg("default")
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains(&format!("{}", temp_test_path.join("default_file.txt").display())));

    std::env::set_current_dir(original_dir)?;
    temp_test_dir.close()?;
    Ok(())
}
