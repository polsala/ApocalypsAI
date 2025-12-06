use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;
use std::{fs, path::PathBuf, time::SystemTime};
use filetime::{set_file_mtime, FileTime};
use chrono::{Utc, Duration};

// Mock rationale: We create a temporary directory and files with specific modification times
// to simulate a file system state. This ensures tests are deterministic and do not
// depend on the actual system's file structure or current time.

#[test]
fn test_finds_old_files() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let temp_path = temp_dir.path();

    // Create a file that is old enough to be a relic (e.g., 100 days old)
    let old_file_path = temp_path.join("old_relic.txt");
    fs::write(&old_file_path, "This is an old relic.")?;
    let old_time = Utc::now() - Duration::days(100);
    set_file_mtime(&old_file_path, FileTime::from_system_time(old_time.to_system_time()))?;

    // Create a file that is not old enough (e.g., 50 days old)
    let new_file_path = temp_path.join("new_data.txt");
    fs::write(&new_file_path, "This is new data.")?;
    let new_time = Utc::now() - Duration::days(50);
    set_file_mtime(&new_file_path, FileTime::from_system_time(new_time.to_system_time()))?;

    // Create a file that is very new (e.g., 1 day old)
    let very_new_file_path = temp_path.join("current_log.txt");
    fs::write(&very_new_file_path, "Current log.")?;
    let very_new_time = Utc::now() - Duration::days(1);
    set_file_mtime(&very_new_file_path, FileTime::from_system_time(very_new_time.to_system_time()))?;

    // Create a subdirectory with an old file
    let sub_dir = temp_path.join("archive");
    fs::create_dir(&sub_dir)?;
    let old_sub_file_path = sub_dir.join("ancient_scroll.doc");
    fs::write(&old_sub_file_path, "An ancient scroll.")?;
    set_file_mtime(&old_sub_file_path, FileTime::from_system_time(old_time.to_system_time()))?;


    // Run the command with a threshold of 90 days
    let mut cmd = Command::cargo_bin("nightly-relic-rustler")?;
    cmd.arg("-p").arg(temp_path.to_str().unwrap())
       .arg("-a").arg("90");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains(format!("  {} (Modified: {})", old_file_path.display(), old_time.format("%Y-%m-%d"))))
        .stdout(predicate::str::contains(format!("  {} (Modified: {})", old_sub_file_path.display(), old_time.format("%Y-%m-%d"))))
        .stdout(predicate::str::contains("Found 2 digital relics."))
        .stdout(predicate::str::does_not_contain(new_file_path.display().to_string()))
        .stdout(predicate::str::does_not_contain(very_new_file_path.display().to_string()));

    Ok(())
}

#[test]
fn test_no_relics_found() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let temp_path = temp_dir.path();

    // Create a file that is not old enough (e.g., 50 days old)
    let new_file_path = temp_path.join("new_data.txt");
    fs::write(&new_file_path, "This is new data.")?;
    let new_time = Utc::now() - Duration::days(50);
    set_file_mtime(&new_file_path, FileTime::from_system_time(new_time.to_system_time()))?;

    // Run the command with a threshold of 90 days
    let mut cmd = Command::cargo_bin("nightly-relic-rustler")?;
    cmd.arg("-p").arg(temp_path.to_str().unwrap())
       .arg("-a").arg("90");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Found 0 digital relics."))
        .stdout(predicate::str::does_not_contain(new_file_path.display().to_string()));

    Ok(())
}

#[test]
fn test_all_files_are_relics() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let temp_path = temp_dir.path();

    // Create a file that is old enough to be a relic (e.g., 100 days old)
    let old_file_path_1 = temp_path.join("old_relic_1.txt");
    fs::write(&old_file_path_1, "This is an old relic 1.")?;
    let old_time = Utc::now() - Duration::days(100);
    set_file_mtime(&old_file_path_1, FileTime::from_system_time(old_time.to_system_time()))?;

    let old_file_path_2 = temp_path.join("old_relic_2.txt");
    fs::write(&old_file_path_2, "This is an old relic 2.")?;
    set_file_mtime(&old_file_path_2, FileTime::from_system_time(old_time.to_system_time()))?;

    // Run the command with a threshold of 90 days
    let mut cmd = Command::cargo_bin("nightly-relic-rustler")?;
    cmd.arg("-p").arg(temp_path.to_str().unwrap())
       .arg("-a").arg("90");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains(format!("  {} (Modified: {})", old_file_path_1.display(), old_time.format("%Y-%m-%d"))))
        .stdout(predicate::str::contains(format!("  {} (Modified: {})", old_file_path_2.display(), old_time.format("%Y-%m-%d"))))
        .stdout(predicate::str::contains("Found 2 digital relics."));

    Ok(())
}
