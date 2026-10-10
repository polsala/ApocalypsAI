use assert_cmd::Command;
use predicates::prelude::*;
use std::{fs, path::Path, time::{SystemTime, Duration}};
use tempfile::tempdir;

#[test]
fn test_scavenge_basic_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a recent file (should not be reported by default age/size)
    fs::write(path.join("recent_data.txt"), "recent data")?;

    // Create an old, large file (will be caught by max_age_days=0 and min_size_bytes=10)
    let old_large_file = path.join("ancient_archive.zip");
    fs::write(&old_large_file, vec![0; 2 * 1024 * 1024])?; // 2MB

    // Create a small, old log file (will be caught by max_age_days=0 and ephemeral type)
    let small_old_log = path.join("debug.log");
    fs::write(&small_old_log, "small log content")?;

    // Create a file that is only 'significant' (large) if max_age_days is high
    let large_but_recent = path.join("current_backup.bak");
    fs::write(&large_but_recent, vec![0; 3 * 1024 * 1024])?; // 3MB

    // Mock rationale: For deterministic testing of file age, we set `max_age_days` to 0.
    // This ensures any file created during the test run (which is effectively 'now') is considered
    // 'older than 0 days ago', allowing us to test the age-based classification reliably without
    // manipulating system time or relying on external time-setting utilities.
    Command::cargo_bin("nightly-resource-scavenger")?
        .arg("-p")
        .arg(path.to_str().unwrap())
        .arg("-r") // recursive
        .arg("--max-age-days")
        .arg("0") // Any file is considered old
        .arg("--min-size-bytes")
        .arg("10") // Any file larger than 10 bytes
        .assert()
        .success()
        .stdout(predicate::str::contains("--- Scavenger Report ---"))
        .stdout(predicate::str::contains(format!("[Forgotten Relic & Significant] {}", old_large_file.display())))
        .stdout(predicate::str::contains(format!("[Forgotten Relic (Ephemeral Scrap)] {}", small_old_log.display())))
        .stdout(predicate::str::contains(format!("[Forgotten Relic & Significant (Ephemeral Scrap)] {}", large_but_recent.display())))
        .stdout(predicate::str::not(predicate::str::contains(format!("{}", path.join("recent_data.txt").display()))))
        .stdout(predicate::str::contains("Consider these findings for reclamation or respectful disposal."));

    dir.close()?;
    Ok(())
}

#[test]
fn test_scavenge_no_files_match() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a recent, small file that should not match default criteria
    fs::write(path.join("current_project.rs"), "fn main() {}\n")?;

    // Mock rationale: Using default `max_age_days` (30) and `min_size_bytes` (1MB) ensures
    // this newly created small file is not reported, verifying the 'no files found' scenario.
    Command::cargo_bin("nightly-resource-scavenger")?
        .arg("-p")
        .arg(path.to_str().unwrap())
        .arg("-r")
        .assert()
        .success()
        .stdout(predicate::str::contains("No forgotten relics or dusty archives found. Your digital wasteland is surprisingly tidy!"));

    dir.close()?;
    Ok(())
}

#[test]
fn test_scavenge_non_recursive() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();
    let subdir = path.join("subdir");
    fs::create_dir(&subdir)?;

    let top_level_file = path.join("top_level_data.bin");
    fs::write(&top_level_file, vec![0; 2 * 1024 * 1024])?; // 2MB

    let sub_level_file = subdir.join("sub_level_data.bin");
    fs::write(&sub_level_file, vec![0; 2 * 1024 * 1024])?; // 2MB

    // Mock rationale: `max_age_days=0` and `min_size_bytes=10` ensure all created files would match
    // if scanned. This allows us to specifically test the `recursive` flag's effect.
    Command::cargo_bin("nightly-resource-scavenger")?
        .arg("-p")
        .arg(path.to_str().unwrap())
        .arg("--max-age-days")
        .arg("0")
        .arg("--min-size-bytes")
        .arg("10")
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("[Forgotten Relic & Significant] {}", top_level_file.display())))
        .stdout(predicate::str::not(predicate::str::contains(format!("{}", sub_level_file.display()))));

    dir.close()?;
    Ok(())
}

#[test]
fn test_scavenge_non_existent_path() -> Result<(), Box<dyn std::error::Error>> {
    let non_existent_path = Path::new("/this/path/does/not/exist/definitely");

    // Mock rationale: Testing with a non-existent path directly verifies the error handling
    // and graceful exit without needing to mock file system operations.
    Command::cargo_bin("nightly-resource-scavenger")?
        .arg("-p")
        .arg(non_existent_path.to_str().unwrap())
        .assert()
        .success() // The tool prints a warning and exits successfully, not an error
        .stderr(predicate::str::contains(format!("Warning: Directory '{}' does not exist or is not a directory. Skipping.", non_existent_path.display())))
        .stdout(predicate::str::contains("No forgotten relics or dusty archives found."));

    Ok(())
}
