use assert_cmd::prelude::*;
use predicates::prelude::*;
use std::process::Command;
use tempfile::tempdir;
use std::fs::{self, File};
use std::io::Write;
use std::time::{SystemTime, Duration};
use chrono::{Utc, Duration as ChronoDuration};
use filetime::{set_file_mtime, FileTime};

// Mock rationale: The tests use the `tempfile` crate to create isolated, temporary file system
// structures, allowing for deterministic and offline testing of file scanning and manipulation
// logic without affecting the actual user's filesystem or requiring network access.
// `assert_cmd` is used to run the compiled binary and assert its output and exit status.

#[test]
fn test_list_dust_bunnies() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create an old file (dust bunny)
    let old_file_path = path.join("old_report.txt");
    File::create(&old_file_path)?.write_all(b"old data")?;
    let one_year_ago = Utc::now() - ChronoDuration::days(366); // Older than default 365 days
    set_file_mtime(&old_file_path, FileTime::from_system_time(one_year_ago.into()))?;

    // Create a new file
    let new_file_path = path.join("new_log.txt");
    File::create(&new_file_path)?.write_all(b"new data")?;
    // Default mtime is now, so it's new enough

    Command::cargo_bin("nightly-dust-bunny-collector")?
        .arg("--path")
        .arg(path)
        .arg("--age")
        .arg("365") // Default age
        .arg("list")
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("[DUST BUNNY] {}", old_file_path.display())))
        .stdout(predicate::str::contains("Found 1 digital dust bunnies."))
        .stdout(predicate::str::does_not_contain(format!("[DUST BUNNY] {}", new_file_path.display())));

    Ok(())
}

#[test]
fn test_move_dust_bunnies() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();
    let dest_dir = tempdir()?;
    let dest_path = dest_dir.path();

    // Create an old file (dust bunny)
    let old_file_path = path.join("old_config.toml");
    File::create(&old_file_path)?.write_all(b"old config")?;
    let one_year_ago = Utc::now() - ChronoDuration::days(366);
    set_file_mtime(&old_file_path, FileTime::from_system_time(one_year_ago.into()))?;

    // Create a new file
    let new_file_path = path.join("current_project.rs");
    File::create(&new_file_path)?.write_all(b"current code")?;

    Command::cargo_bin("nightly-dust-bunny-collector")?
        .arg("--path")
        .arg(path)
        .arg("--age")
        .arg("365")
        .arg("move")
        .arg("--destination")
        .arg(dest_path)
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("[MOVED] {} -> {}", old_file_path.display(), dest_path.join("old_config.toml").display())))
        .stdout(predicate::str::contains("Found 1 digital dust bunnies."));

    // Verify the old file is moved and the new file is untouched
    assert!(!old_file_path.exists());
    assert!(dest_path.join("old_config.toml").exists());
    assert!(new_file_path.exists());

    Ok(())
}

#[test]
fn test_no_dust_bunnies_found() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create a new file
    let new_file_path = path.join("recent_doc.md");
    File::create(&new_file_path)?.write_all(b"recent content")?;

    Command::cargo_bin("nightly-dust-bunny-collector")?
        .arg("--path")
        .arg(path)
        .arg("--age")
        .arg("365")
        .arg("list")
        .assert()
        .success()
        .stdout(predicate::str::contains("Found 0 digital dust bunnies."))
        .stdout(predicate::str::does_not_contain("[DUST BUNNY]"));

    Ok(())
}

#[test]
fn test_nested_dust_bunnies() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();
    let nested_dir = path.join("nested");
    fs::create_dir(&nested_dir)?;

    // Create an old file in a nested directory
    let nested_old_file_path = nested_dir.join("nested_old.log");
    File::create(&nested_old_file_path)?.write_all(b"nested old data")?;
    let one_year_ago = Utc::now() - ChronoDuration::days(366);
    set_file_mtime(&nested_old_file_path, FileTime::from_system_time(one_year_ago.into()))?;

    Command::cargo_bin("nightly-dust-bunny-collector")?
        .arg("--path")
        .arg(path)
        .arg("--age")
        .arg("365")
        .arg("list")
        .assert()
        .success()
        .stdout(predicate::str::contains(format!("[DUST BUNNY] {}", nested_old_file_path.display())))
        .stdout(predicate::str::contains("Found 1 digital dust bunnies."));

    Ok(())
}
