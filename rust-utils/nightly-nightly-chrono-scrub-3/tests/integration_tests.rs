use std::process::Command;
use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use tempfile::tempdir;
use filetime::{set_file_mtime, FileTime};
use chrono::{Utc, Duration};

// Mock rationale: Tests create temporary directories and files within a controlled environment
// to simulate file system interactions without affecting the actual system. File modification
// times are explicitly set for deterministic age-based filtering.

fn get_cargo_bin_path() -> PathBuf {
    let mut path = Command::new("cargo")
        .arg("locate-project")
        .arg("--workspace")
        .arg("--message-format=plain")
        .output()
        .expect("Failed to locate cargo project")
        .stdout;
    path.pop(); // Remove trailing newline
    let project_root = PathBuf::from(String::from_utf8(path).unwrap().trim());
    project_root.join("target").join(env!("PROFILE")).join("chrono-scrub")
}

#[test]
fn test_dry_run_identifies_old_files() {
    let temp_dir = tempdir().expect("Failed to create temp dir");
    let temp_path = temp_dir.path();

    // Create a file older than 1 day
    let old_file_path = temp_path.join("old_log.txt");
    File::create(&old_file_path).expect("Failed to create old_log.txt").write_all(b"old content").unwrap();
    let one_day_ago = Utc::now() - Duration::days(1) - Duration::hours(1); // Ensure it's definitely older
    set_file_mtime(&old_file_path, FileTime::from_system_time(one_day_ago.into())).expect("Failed to set mtime");

    // Create a file newer than 1 day
    let new_file_path = temp_path.join("new_log.txt");
    File::create(&new_file_path).expect("Failed to create new_log.txt").write_all(b"new content").unwrap();
    let now = Utc::now();
    set_file_mtime(&new_file_path, FileTime::from_system_time(now.into())).expect("Failed to set mtime");

    let output = Command::new(get_cargo_bin_path())
        .arg(temp_path)
        .arg("--duration")
        .arg("1d")
        .arg("--dry-run")
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("stdout: {}\nstderr: {}", stdout, stderr);

    assert!(output.status.success());
    assert!(stdout.contains(&format!("Found 1 files fading into the void:")));
    assert!(stdout.contains(&format!("  - {}", old_file_path.display())));
    assert!(!stdout.contains(&format!("  - {}", new_file_path.display())));
    assert!(stdout.contains("(Dry run complete. No files were actually scrubbed.)"));

    assert!(old_file_path.exists()); // Should still exist in dry run
    assert!(new_file_path.exists());
}

#[test]
fn test_scrub_deletes_old_files_force() {
    let temp_dir = tempdir().expect("Failed to create temp dir");
    let temp_path = temp_dir.path();

    let old_file_path = temp_path.join("old_data.bin");
    File::create(&old_file_path).expect("Failed to create old_data.bin").write_all(b"old content").unwrap();
    let two_days_ago = Utc::now() - Duration::days(2);
    set_file_mtime(&old_file_path, FileTime::from_system_time(two_days_ago.into())).expect("Failed to set mtime");

    let new_file_path = temp_path.join("new_data.bin");
    File::create(&new_file_path).expect("Failed to create new_data.bin").write_all(b"new content").unwrap();
    let now = Utc::now();
    set_file_mtime(&new_file_path, FileTime::from_system_time(now.into())).expect("Failed to set mtime");

    let output = Command::new(get_cargo_bin_path())
        .arg(temp_path)
        .arg("--duration")
        .arg("1d")
        .arg("--force")
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("stdout: {}\nstderr: {}", stdout, stderr);

    assert!(output.status.success());
    assert!(stdout.contains(&format!("Found 1 files fading into the void:")));
    assert!(stdout.contains(&format!("Reclaiming temporal bandwidth: '{}' scrubbed.", old_file_path.display())));
    assert!(stdout.contains("The digital dust has settled. 1 files scrubbed."));

    assert!(!old_file_path.exists()); // Should be deleted
    assert!(new_file_path.exists()); // Should still exist
}

#[test]
fn test_exclude_pattern() {
    let temp_dir = tempdir().expect("Failed to create temp dir");
    let temp_path = temp_dir.path();

    let old_log_path = temp_path.join("old.log");
    File::create(&old_log_path).expect("Failed to create old.log").write_all(b"log content").unwrap();
    let two_days_ago = Utc::now() - Duration::days(2);
    set_file_mtime(&old_log_path, FileTime::from_system_time(two_days_ago.into())).expect("Failed to set mtime");

    let old_txt_path = temp_path.join("old.txt");
    File::create(&old_txt_path).expect("Failed to create old.txt").write_all(b"txt content").unwrap();
    set_file_mtime(&old_txt_path, FileTime::from_system_time(two_days_ago.into())).expect("Failed to set mtime");

    let output = Command::new(get_cargo_bin_path())
        .arg(temp_path)
        .arg("--duration")
        .arg("1d")
        .arg("--dry-run")
        .arg("--exclude")
        .arg("*.log")
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("stdout: {}\nstderr: {}", stdout, stderr);

    assert!(output.status.success());
    assert!(stdout.contains(&format!("Found 1 files fading into the void:")));
    assert!(stdout.contains(&format!("  - {}", old_txt_path.display())));
    assert!(!stdout.contains(&format!("  - {}", old_log_path.display()))); // Excluded
}

#[test]
fn test_no_old_files() {
    let temp_dir = tempdir().expect("Failed to create temp dir");
    let temp_path = temp_dir.path();

    let file_path = temp_path.join("recent.txt");
    File::create(&file_path).expect("Failed to create recent.txt").write_all(b"recent content").unwrap();
    let now = Utc::now();
    set_file_mtime(&file_path, FileTime::from_system_time(now.into())).expect("Failed to set mtime");

    let output = Command::new(get_cargo_bin_path())
        .arg(temp_path)
        .arg("--duration")
        .arg("1d")
        .arg("--dry-run")
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("stdout: {}\nstderr: {}", stdout, stderr);

    assert!(output.status.success());
    assert!(stdout.contains("No files found succumbing to digital entropy within the specified duration."));
    assert!(!stdout.contains("Found"));
}

#[test]
fn test_invalid_path_error() {
    let output = Command::new(get_cargo_bin_path())
        .arg("non_existent_dir_12345")
        .arg("--dry-run")
        .output()
        .expect("Failed to execute command");

    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(!output.status.success());
    assert!(stderr.contains("Error: Path 'non_existent_dir_12345' does not exist."));
}
