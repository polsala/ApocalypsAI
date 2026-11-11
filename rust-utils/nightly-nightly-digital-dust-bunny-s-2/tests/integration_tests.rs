use assert_cmd::prelude::*;
use predicates::prelude::*;
use std::process::Command;
use tempfile::tempdir;
use std::fs::{self, File};
use std::io::Write;
use std::thread::sleep;
use std::time::Duration;

// Mock rationale: For these integration tests, we create actual temporary files and directories
// using `tempfile`. This allows us to test the utility's file system interactions directly
// in a controlled environment, ensuring it behaves as expected without complex mocking
// frameworks. The `tempfile` crate handles cleanup automatically.

#[test]
fn finds_old_files_with_specific_age() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let old_file_path = dir.path().join("old_bunny.txt");
    let new_file_path = dir.path().join("new_bunny.txt");

    // Create a file that will be considered 'old' for age_days=1
    File::create(&old_file_path)?.write_all(b"old content")?;
    // Ensure the file is closed so its modification time is finalized
    drop(File::create(&old_file_path)?);
    // Sleep to ensure a measurable time difference for the 'age_days' calculation
    sleep(Duration::from_secs(2));

    // Create a file that will be considered 'new'
    File::create(&new_file_path)?.write_all(b"new content")?;

    let mut cmd = Command::cargo_bin("nightly-digital-dust-bunny-sweeper")?;
    cmd.arg("--path").arg(dir.path())
       .arg("--age-days").arg("1"); // Files older than 1 day are dust bunnies

    cmd.assert()
        .success()
        .stdout(predicates::str::contains(old_file_path.to_string_lossy().as_ref()))
        .stdout(predicates::str::contains("1 digital dust bunnies"))
        .stdout(predicates::str::not(predicates::str::contains(new_file_path.to_string_lossy().as_ref())));

    Ok(())
}

#[test]
fn cuddles_files_to_archive() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let archive_dir = dir.path().join("archive");
    let old_file_path = dir.path().join("old_bunny_to_cuddle.txt");

    File::create(&old_file_path)?.write_all(b"cuddle me")?;
    drop(File::create(&old_file_path)?);
    sleep(Duration::from_secs(2));

    let mut cmd = Command::cargo_bin("nightly-digital-dust-bunny-sweeper")?;
    cmd.arg("--path").arg(dir.path())
       .arg("--age-days").arg("1")
       .arg("--cuddle-to").arg(&archive_dir);

    cmd.assert()
        .success()
        .stdout(predicates::str::contains("Cuddling all dust bunnies"))
        .stdout(predicates::str::contains(format!("\'{}\' -> \'{}\'", old_file_path.display(), archive_dir.join("old_bunny_to_cuddle.txt").display())));

    assert!(!old_file_path.exists());
    assert!(archive_dir.join("old_bunny_to_cuddle.txt").exists());

    Ok(())
}

#[test]
fn releases_files_with_confirmation() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let old_file_path = dir.path().join("old_bunny_to_release.txt");

    File::create(&old_file_path)?.write_all(b"release me")?;
    drop(File::create(&old_file_path)?);
    sleep(Duration::from_secs(2));

    let mut cmd = Command::cargo_bin("nightly-digital-dust-bunny-sweeper")?;
    cmd.arg("--path").arg(dir.path())
       .arg("--age-days").arg("1")
       .arg("--release-all")
       .arg("--confirm-release");

    cmd.assert()
        .success()
        .stdout(predicates::str::contains("Releasing all dust bunnies"))
        .stdout(predicates::str::contains(format!("Released \'{}\'", old_file_path.display())));

    assert!(!old_file_path.exists());

    Ok(())
}

#[test]
fn release_all_without_confirm_fails() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let old_file_path = dir.path().join("old_bunny_to_fail_release.txt");

    File::create(&old_file_path)?.write_all(b"fail release")?;
    drop(File::create(&old_file_path)?);
    sleep(Duration::from_secs(2));

    let mut cmd = Command::cargo_bin("nightly-digital-dust-bunny-sweeper")?;
    cmd.arg("--path").arg(dir.path())
       .arg("--age-days").arg("1")
       .arg("--release-all");

    cmd.assert()
        .failure()
        .stderr(predicates::str::contains("Error: --release-all requires --confirm-release for safety."));

    assert!(old_file_path.exists()); // File should not be deleted

    Ok(())
}

#[test]
fn no_dust_bunnies_found() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let new_file_path = dir.path().join("new_file.txt");
    File::create(&new_file_path)?.write_all(b"new content")?;

    let mut cmd = Command::cargo_bin("nightly-digital-dust-bunny-sweeper")?;
    cmd.arg("--path").arg(dir.path())
       .arg("--age-days").arg("0"); // No files are 0 days old, so none should be found

    cmd.assert()
        .success()
        .stdout(predicates::str::contains("No digital dust bunnies found! Your digital space is sparkling clean."));

    Ok(())
}
