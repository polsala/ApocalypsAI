use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::{tempdir, TempDir};
use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;

// Mock rationale: These tests create temporary directories and files on the local filesystem
// to simulate different states for comparison. This is a controlled, isolated environment
// and does not interact with any external services or network, ensuring determinism and
// offline execution.

fn setup_test_dirs() -> Result<(TempDir, TempDir), Box<dyn std::error::Error>> {
    let baseline_dir = tempdir()?;
    let current_dir = tempdir()?;
    Ok((baseline_dir, current_dir))
}

fn create_file(dir: &PathBuf, filename: &str, content: &str) -> Result<(), Box<dyn std::error::Error>> {
    let filepath = dir.join(filename);
    let mut file = File::create(&filepath)?;
    file.write_all(content.as_bytes())?;
    Ok(())
}

#[test]
fn test_no_drift() -> Result<(), Box<dyn std::error::Error>> {
    let (baseline_dir, current_dir) = setup_test_dirs()?;

    create_file(&baseline_dir.path().to_path_buf(), "file1.txt", "content A")?;
    create_file(&baseline_dir.path().to_path_buf(), "file2.txt", "content B")?;
    create_file(&current_dir.path().to_path_buf(), "file1.txt", "content A")?;
    create_file(&current_dir.path().to_path_buf(), "file2.txt", "content B")?;

    Command::cargo_bin("nightly-chrono-drift-detector")?
        .arg("--baseline")
        .arg(baseline_dir.path())
        .arg("--current")
        .arg(current_dir.path())
        .assert()
        .success()
        .stdout(predicate::str::contains("No significant chrono-drift detected. Reality remains stable... for now."));

    Ok(())
}

#[test]
fn test_new_file() -> Result<(), Box<dyn std::error::Error>> {
    let (baseline_dir, current_dir) = setup_test_dirs()?;

    create_file(&baseline_dir.path().to_path_buf(), "file1.txt", "content A")?;
    create_file(&current_dir.path().to_path_buf(), "file1.txt", "content A")?;
    create_file(&current_dir.path().to_path_buf(), "new_file.txt", "new content")?;

    Command::cargo_bin("nightly-chrono-drift-detector")?
        .arg("--baseline")
        .arg(baseline_dir.path())
        .arg("--current")
        .arg(current_dir.path())
        .assert()
        .success()
        .stdout(predicate::str::contains("Emergent Chrono-Entities (New Files):"))
        .stdout(predicate::str::contains("  - new_file.txt"));

    Ok(())
}

#[test]
fn test_deleted_file() -> Result<(), Box<dyn std::error::Error>> {
    let (baseline_dir, current_dir) = setup_test_dirs()?;

    create_file(&baseline_dir.path().to_path_buf(), "file1.txt", "content A")?;
    create_file(&baseline_dir.path().to_path_buf(), "deleted_file.txt", "old content")?;
    create_file(&current_dir.path().to_path_buf(), "file1.txt", "content A")?;

    Command::cargo_bin("nightly-chrono-drift-detector")?
        .arg("--baseline")
        .arg(baseline_dir.path())
        .arg("--current")
        .arg(current_dir.path())
        .assert()
        .success()
        .stdout(predicate::str::contains("Vanished Temporal Echoes (Deleted Files):"))
        .stdout(predicate::str::contains("  - deleted_file.txt"));

    Ok(())
}

#[test]
fn test_modified_file() -> Result<(), Box<dyn std::error::Error>> {
    let (baseline_dir, current_dir) = setup_test_dirs()?;

    create_file(&baseline_dir.path().to_path_buf(), "file1.txt", "content A")?;
    create_file(&current_dir.path().to_path_buf(), "file1.txt", "modified content A")?;

    Command::cargo_bin("nightly-chrono-drift-detector")?
        .arg("--baseline")
        .arg(baseline_dir.path())
        .arg("--current")
        .arg(current_dir.path())
        .assert()
        .success()
        .stdout(predicate::str::contains("Distorted Chrono-Signatures (Modified Files):"))
        .stdout(predicate::str::contains("  - file1.txt"));

    Ok(())
}

#[test]
fn test_mixed_changes() -> Result<(), Box<dyn std::error::Error>> {
    let (baseline_dir, current_dir) = setup_test_dirs()?;

    // Baseline
    create_file(&baseline_dir.path().to_path_buf(), "common.txt", "original")?;
    create_file(&baseline_dir.path().to_path_buf(), "deleted.txt", "will be gone")?;
    create_file(&baseline_dir.path().to_path_buf(), "modified.txt", "old content")?;
    fs::create_dir(baseline_dir.path().join("subdir"))?;
    create_file(&baseline_dir.path().join("subdir"), "nested_deleted.txt", "nested old")?;
    create_file(&baseline_dir.path().join("subdir"), "nested_modified.txt", "nested old")?;

    // Current
    create_file(&current_dir.path().to_path_buf(), "common.txt", "original")?;
    create_file(&current_dir.path().to_path_buf(), "new.txt", "brand new")?;
    create_file(&current_dir.path().to_path_buf(), "modified.txt", "new content")?;
    fs::create_dir(current_dir.path().join("subdir"))?;
    create_file(&current_dir.path().join("subdir"), "nested_new.txt", "nested new")?;
    create_file(&current_dir.path().join("subdir"), "nested_modified.txt", "nested new content")?;

    Command::cargo_bin("nightly-chrono-drift-detector")?
        .arg("--baseline")
        .arg(baseline_dir.path())
        .arg("--current")
        .arg(current_dir.path())
        .assert()
        .success()
        .stdout(predicate::str::contains("Emergent Chrono-Entities (New Files):"))
        .stdout(predicate::str::contains("  - new.txt"))
        .stdout(predicate::str::contains("  - subdir/nested_new.txt"))
        .stdout(predicate::str::contains("Vanished Temporal Echoes (Deleted Files):"))
        .stdout(predicate::str::contains("  - deleted.txt"))
        .stdout(predicate::str::contains("  - subdir/nested_deleted.txt"))
        .stdout(predicate::str::contains("Distorted Chrono-Signatures (Modified Files):"))
        .stdout(predicate::str::contains("  - modified.txt"))
        .stdout(predicate::str::contains("  - subdir/nested_modified.txt"));

    Ok(())
}

#[test]
fn test_empty_directories() -> Result<(), Box<dyn std::error::Error>> {
    let (baseline_dir, current_dir) = setup_test_dirs()?;

    Command::cargo_bin("nightly-chrono-drift-detector")?
        .arg("--baseline")
        .arg(baseline_dir.path())
        .arg("--current")
        .arg(current_dir.path())
        .assert()
        .success()
        .stdout(predicate::str::contains("No significant chrono-drift detected. Reality remains stable... for now."));

    Ok(())
}

#[test]
fn test_baseline_empty_current_has_files() -> Result<(), Box<dyn std::error::Error>> {
    let (baseline_dir, current_dir) = setup_test_dirs()?;
    create_file(&current_dir.path().to_path_buf(), "new_file.txt", "content")?;

    Command::cargo_bin("nightly-chrono-drift-detector")?
        .arg("--baseline")
        .arg(baseline_dir.path())
        .arg("--current")
        .arg(current_dir.path())
        .assert()
        .success()
        .stdout(predicate::str::contains("Emergent Chrono-Entities (New Files):"))
        .stdout(predicate::str::contains("  - new_file.txt"));

    Ok(())
}

#[test]
fn test_current_empty_baseline_has_files() -> Result<(), Box<dyn std::error::Error>> {
    let (baseline_dir, current_dir) = setup_test_dirs()?;
    create_file(&baseline_dir.path().to_path_buf(), "deleted_file.txt", "content")?;

    Command::cargo_bin("nightly-chrono-drift-detector")?
        .arg("--baseline")
        .arg(baseline_dir.path())
        .arg("--current")
        .arg(current_dir.path())
        .assert()
        .success()
        .stdout(predicate::str::contains("Vanished Temporal Echoes (Deleted Files):"))
        .stdout(predicate::str::contains("  - deleted_file.txt"));

    Ok(())
}
