use assert_cmd::Command;
use predicates::prelude::*;
use std::fs;
use std::io::Write;
use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};
use tempfile::tempdir;

// Mock rationale: These tests create temporary files and directories on the local filesystem
// to simulate real-world scenarios. This allows for deterministic and offline testing of
// file system operations without relying on external services or actual user files.
// The `filetime` crate is used to precisely control file modification/access times for age-based tests.

#[cfg(target_family = "unix")]
fn set_file_times(path: &PathBuf, modified: SystemTime, accessed: SystemTime) {
    use filetime::{set_file_times, FileTime};
    set_file_times(path, FileTime::from_system_time(accessed), FileTime::from_system_time(modified))
        .expect("Failed to set file times");
}

#[cfg(target_family = "windows")]
fn set_file_times(path: &PathBuf, modified: SystemTime, accessed: SystemTime) {
    // Windows requires `filetime` crate for setting both access and modification times.
    // For simplicity in this test, we'll just use `set_file_mtime` and `set_file_atime`
    // if available, or rely on `std::fs::File::set_times` which might not be as precise.
    // The `filetime` crate is the robust solution.
    use filetime::{set_file_times, FileTime};
    set_file_times(path, FileTime::from_system_time(accessed), FileTime::from_system_time(modified))
        .expect("Failed to set file times");
}

#[cfg(not(any(target_family = "unix", target_family = "windows")))]
fn set_file_times(_path: &PathBuf, _modified: SystemTime, _accessed: SystemTime) {
    // Fallback for other OS, might not be precise or work at all.
    // For robust cross-platform testing, `filetime` crate is recommended.
    eprintln!("Warning: set_file_times not implemented for this OS family. Age tests might be less reliable.");
}

#[test]
fn test_dry_run_no_args_no_output() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path().to_path_buf();

    fs::write(path.join("file1.txt"), "content").unwrap();

    Command::cargo_bin("chrono-scrub").unwrap()
        .arg("--path").arg(&path)
        .assert()
        .success()
        .stdout(predicate::str::contains("No temporal detritus found"));
}

#[test]
fn test_dry_run_age_detection() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path().to_path_buf();

    let old_file_path = path.join("old_log.txt");
    fs::write(&old_file_path, "old log content").unwrap();
    // Set modified/accessed time to 100 days ago
    let old_time = SystemTime::now() - std::time::Duration::from_secs(100 * 24 * 60 * 60);
    set_file_times(&old_file_path, old_time, old_time);

    let recent_file_path = path.join("recent_data.txt");
    fs::write(&recent_file_path, "recent content").unwrap();
    // Default time is recent, no need to set explicitly

    Command::cargo_bin("chrono-scrub").unwrap()
        .arg("--path").arg(&path)
        .arg("--age").arg("90") // Look for files older than 90 days
        .assert()
        .success()
        .stdout(predicate::str::contains("old_log.txt"))
        .stdout(predicate::str::contains("Total files identified for scrubbing: 1"))
        .stdout(predicate::str::contains("This was a DRY RUN"));

    assert!(old_file_path.exists()); // Should not be deleted in dry run
}

#[test]
fn test_dry_run_duplicate_detection() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path().to_path_buf();

    let content = "duplicate content";
    fs::write(path.join("dup1.txt"), content).unwrap();
    fs::write(path.join("subdir").tap_mut(|p| { fs::create_dir_all(p).unwrap(); }).join("dup2.txt"), content).unwrap();
    fs::write(path.join("unique.txt"), "unique content").unwrap();

    Command::cargo_bin("chrono-scrub").unwrap()
        .arg("--path").arg(&path)
        .arg("--duplicates")
        .assert()
        .success()
        .stdout(predicate::str::contains("dup1.txt"))
        .stdout(predicate::str::contains("dup2.txt"))
        .stdout(predicate::str::contains("Total files identified for scrubbing: 1")) // One duplicate identified for deletion
        .stdout(predicate::str::contains("This was a DRY RUN"));

    assert!(path.join("dup1.txt").exists());
    assert!(path.join("subdir/dup2.txt").exists());
}

#[test]
fn test_delete_age_detection() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path().to_path_buf();

    let old_file_path = path.join("old_data.bin");
    fs::write(&old_file_path, "binary data").unwrap();
    let old_time = SystemTime::now() - std::time::Duration::from_secs(100 * 24 * 60 * 60);
    set_file_times(&old_file_path, old_time, old_time);

    let recent_file_path = path.join("recent_config.json");
    fs::write(&recent_file_path, "{}").unwrap();

    Command::cargo_bin("chrono-scrub").unwrap()
        .arg("--path").arg(&path)
        .arg("--age").arg("90")
        .arg("--delete")
        .write_stdin("yes\n") // Simulate user confirmation
        .assert()
        .success()
        .stdout(predicate::str::contains("old_data.bin"))
        .stdout(predicate::str::contains("Chrono-Scrub complete. 1 files purged"));

    assert!(!old_file_path.exists()); // Should be deleted
    assert!(recent_file_path.exists()); // Should remain
}

#[test]
fn test_delete_duplicate_detection() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path().to_path_buf();

    let content = "another duplicate";
    let dup1_path = path.join("dup_a.log");
    let dup2_path = path.join("archive").tap_mut(|p| { fs::create_dir_all(p).unwrap(); }).join("dup_b.log");
    let unique_path = path.join("unique.log");

    fs::write(&dup1_path, content).unwrap();
    fs::write(&dup2_path, content).unwrap();
    fs::write(&unique_path, "unique content").unwrap();

    Command::cargo_bin("chrono-scrub").unwrap()
        .arg("--path").arg(&path)
        .arg("--duplicates")
        .arg("--delete")
        .write_stdin("yes\n")
        .assert()
        .success()
        .stdout(predicate::str::contains("dup_b.log")) // The second instance is marked for deletion
        .stdout(predicate::str::contains("Chrono-Scrub complete. 1 files purged"));

    assert!(dup1_path.exists()); // First instance should remain
    assert!(!dup2_path.exists()); // Second instance should be deleted
    assert!(unique_path.exists()); // Unique file should remain
}

#[test]
fn test_delete_confirmation_no() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path().to_path_buf();

    let old_file_path = path.join("temp_file.tmp");
    fs::write(&old_file_path, "temp content").unwrap();
    let old_time = SystemTime::now() - std::time::Duration::from_secs(100 * 24 * 60 * 60);
    set_file_times(&old_file_path, old_time, old_time);

    Command::cargo_bin("chrono-scrub").unwrap()
        .arg("--path").arg(&path)
        .arg("--age").arg("90")
        .arg("--delete")
        .write_stdin("no\n") // Simulate user declining confirmation
        .assert()
        .success()
        .stdout(predicate::str::contains("Chrono-Scrub aborted. Files remain untouched."));

    assert!(old_file_path.exists()); // Should not be deleted
}

#[test]
fn test_min_size_filter() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path().to_path_buf();

    let small_file_path = path.join("small.txt");
    fs::write(&small_file_path, "a").unwrap(); // 1 byte
    let large_file_path = path.join("large.txt");
    fs::write(&large_file_path, "this is larger").unwrap(); // > 1 byte

    let old_time = SystemTime::now() - std::time::Duration::from_secs(100 * 24 * 60 * 60);
    set_file_times(&small_file_path, old_time, old_time);
    set_file_times(&large_file_path, old_time, old_time);

    Command::cargo_bin("chrono-scrub").unwrap()
        .arg("--path").arg(&path)
        .arg("--age").arg("90")
        .arg("--min-size").arg("5") // Only consider files >= 5 bytes
        .assert()
        .success()
        .stdout(predicate::str::contains("large.txt"))
        .stdout(predicate::str::contains("Total files identified for scrubbing: 1"))
        .stdout(predicate::str::contains("This was a DRY RUN"))
        .stdout(predicate::str::not(predicate::str::contains("small.txt")));
}

#[test]
fn test_non_existent_path() {
    let non_existent_path = PathBuf::from("/this/path/does/not/exist_12345");

    Command::cargo_bin("chrono-scrub").unwrap()
        .arg("--path").arg(&non_existent_path)
        .assert()
        .success() // The program should exit gracefully, not with an error code
        .stderr(predicate::str::contains("Error: Provided path is not a directory"));
}

#[test]
fn test_verbose_output() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path().to_path_buf();

    let small_file_path = path.join("tiny.txt");
    fs::write(&small_file_path, "a").unwrap(); // 1 byte
    let old_time = SystemTime::now() - std::time::Duration::from_secs(100 * 24 * 60 * 60);
    set_file_times(&small_file_path, old_time, old_time);

    Command::cargo_bin("chrono-scrub").unwrap()
        .arg("--path").arg(&path)
        .arg("--age").arg("90")
        .arg("--min-size").arg("5") // This will skip tiny.txt
        .arg("--verbose")
        .assert()
        .success()
        .stdout(predicate::str::contains("Skipping small file: ").and(predicate::str::contains("tiny.txt")))
        .stdout(predicate::str::contains("No temporal detritus found"));
}
