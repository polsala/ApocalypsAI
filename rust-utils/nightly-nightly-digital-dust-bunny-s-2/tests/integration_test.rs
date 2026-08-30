use assert_cmd::Command;
use tempfile::{tempdir, NamedTempFile};
use std::fs::{self, File};
use std::io::Write;
use std::time::{SystemTime, UNIX_EPOCH};
use filetime::{set_file_times, FileTime};
use chrono::{Utc, Duration};

// Mock rationale: Tests create temporary files and directories with controlled timestamps
// to simulate various file system states, avoiding actual file system modifications
// outside the test environment and ensuring deterministic results.

#[test]
fn test_no_dust_bunnies_found() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    // Create a recent file
    let mut file = File::create(path.join("recent_file.txt")).unwrap();
    writeln!(file, "Hello, world!").unwrap();

    let mut cmd = Command::cargo_bin("dust-bunny-sweeper").unwrap();
    let output = cmd
        .arg("--path")
        .arg(path)
        .arg("--age")
        .arg("1d") // Look for files older than 1 day
        .assert();

    output.success().stdout(
        predicates::str::contains("No digital dust bunnies found! Your digital realm is sparkling clean. \u{2728}")
    );

    temp_dir.close().unwrap();
}

#[test]
fn test_finds_old_file() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    // Create an old file
    let old_file_path = path.join("old_log.txt");
    let mut file = File::create(&old_file_path).unwrap();
    writeln!(file, "Old log entry.").unwrap();

    // Set its modification and access times to be very old
    let old_time = Utc::now() - Duration::days(365);
    let old_file_time = FileTime::from_system_time(SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(old_time.timestamp() as u64));
    set_file_times(&old_file_path, old_file_time, old_file_time).unwrap();

    let mut cmd = Command::cargo_bin("dust-bunny-sweeper").unwrap();
    let output = cmd
        .arg("--path")
        .arg(path)
        .arg("--age")
        .arg("30d") // Look for files older than 30 days
        .arg("--dry-run")
        .assert();

    output.success().stdout(
        predicates::str::contains("Found 1 digital dust bunnies:")
            .and(predicates::str::contains("old_log.txt"))
            .and(predicates::str::contains("[Petrified Pixie Dust]")) // Small file
    );

    temp_dir.close().unwrap();
}

#[test]
fn test_finds_old_large_file() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    // Create an old, large file (simulated)
    let large_file_path = path.join("old_backup.zip");
    let mut file = File::create(&large_file_path).unwrap();
    // Write 150MB of dummy data
    let dummy_data = vec![0; 1024 * 1024 * 150]; 
    file.write_all(&dummy_data).unwrap();

    // Set its modification and access times to be very old
    let old_time = Utc::now() - Duration::days(365);
    let old_file_time = FileTime::from_system_time(SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(old_time.timestamp() as u64));
    set_file_times(&large_file_path, old_file_time, old_file_time).unwrap();

    let mut cmd = Command::cargo_bin("dust-bunny-sweeper").unwrap();
    let output = cmd
        .arg("--path")
        .arg(path)
        .arg("--age")
        .arg("6m") // Look for files older than 6 months
        .arg("--dry-run")
        .assert();

    output.success().stdout(
        predicates::str::contains("Found 1 digital dust bunnies:")
            .and(predicates::str::contains("old_backup.zip"))
            .and(predicates::str::contains("[Slumbering Data Golem]")) // Large file
    );

    temp_dir.close().unwrap();
}

#[test]
fn test_finds_empty_old_directory() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    // Create an old, empty directory
    let old_dir_path = path.join("empty_old_folder");
    fs::create_dir(&old_dir_path).unwrap();

    // Set its modification time to be very old
    let old_time = Utc::now() - Duration::days(180);
    let old_file_time = FileTime::from_system_time(SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(old_time.timestamp() as u64));
    set_file_times(&old_dir_path, old_file_time, old_file_time).unwrap();

    let mut cmd = Command::cargo_bin("dust-bunny-sweeper").unwrap();
    let output = cmd
        .arg("--path")
        .arg(path)
        .arg("--age")
        .arg("3m") // Look for files/dirs older than 3 months
        .arg("--dry-run")
        .assert();

    output.success().stdout(
        predicates::str::contains("Found 1 digital dust bunnies:")
            .and(predicates::str::contains("empty_old_folder"))
            .and(predicates::str::contains("[Vacant Memory Cavern]"))
    );

    temp_dir.close().unwrap();
}

#[test]
fn test_verbose_output() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    // Create an old file
    let old_file_path = path.join("verbose_test.txt");
    let mut file = File::create(&old_file_path).unwrap();
    writeln!(file, "Verbose log entry.").unwrap();

    let old_time = Utc::now() - Duration::days(100);
    let old_file_time = FileTime::from_system_time(SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(old_time.timestamp() as u64));
    set_file_times(&old_file_path, old_file_time, old_file_time).unwrap();

    let mut cmd = Command::cargo_bin("dust-bunny-sweeper").unwrap();
    let output = cmd
        .arg("--path")
        .arg(path)
        .arg("--age")
        .arg("1m") // Look for files older than 1 month
        .arg("--verbose")
        .arg("--dry-run")
        .assert();

    output.success().stdout(
        predicates::str::contains("Found 1 digital dust bunnies:")
            .and(predicates::str::contains("verbose_test.txt"))
            .and(predicates::str::contains("Last Accessed:"))
            .and(predicates::str::contains("Last Modified:"))
    );

    temp_dir.close().unwrap();
}

#[test]
fn test_invalid_path() {
    let mut cmd = Command::cargo_bin("dust-bunny-sweeper").unwrap();
    let output = cmd
        .arg("--path")
        .arg("/non/existent/path/12345")
        .assert();

    output.failure().stderr(
        predicates::str::contains("Error: Path '/non/existent/path/12345' does not exist.")
    );
}

#[test]
fn test_invalid_age_format() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    let mut cmd = Command::cargo_bin("dust-bunny-sweeper").unwrap();
    let output = cmd
        .arg("--path")
        .arg(path)
        .arg("--age")
        .arg("invalid_age_string")
        .assert();

    output.failure().stderr(
        predicates::str::contains("Error: Invalid age format. Please use formats like '30d', '1y', '2w'.")
    );

    temp_dir.close().unwrap();
}

#[test]
fn test_cleanup_suggestions_not_in_dry_run() {
    let temp_dir = tempdir().unwrap();
    let path = temp_dir.path();

    let old_file_path = path.join("suggest_test.txt");
    let mut file = File::create(&old_file_path).unwrap();
    writeln!(file, "Suggest me!").unwrap();

    let old_time = Utc::now() - Duration::days(100);
    let old_file_time = FileTime::from_system_time(SystemTime::UNIX_EPOCH + std::time::Duration::from_secs(old_time.timestamp() as u64));
    set_file_times(&old_file_path, old_file_time, old_file_time).unwrap();

    // Test with dry-run
    let mut cmd_dry_run = Command::cargo_bin("dust-bunny-sweeper").unwrap();
    let output_dry_run = cmd_dry_run
        .arg("--path")
        .arg(path)
        .arg("--age")
        .arg("1m")
        .arg("--dry-run")
        .assert();

    output_dry_run.success().stdout(
        predicates::str::contains("Found 1 digital dust bunnies:")
            .and(predicates::str::contains("suggest_test.txt"))
            .and(predicates::str::contains("Dry run mode: no files will be deleted or modified."))
            .and(predicates::str::contains("Run without `--dry-run` to get cleanup suggestions."))
            .and(predicates::str::not(predicates::str::contains("Suggestion: `rm")))
    );

    // Test without dry-run
    let mut cmd_no_dry_run = Command::cargo_bin("dust-bunny-sweeper").unwrap();
    let output_no_dry_run = cmd_no_dry_run
        .arg("--path")
        .arg(path)
        .arg("--age")
        .arg("1m")
        .assert();

    output_no_dry_run.success().stdout(
        predicates::str::contains("Found 1 digital dust bunnies:")
            .and(predicates::str::contains("suggest_test.txt"))
            .and(predicates::str::contains("Suggestion: `rm"))
            .and(predicates::str::contains("Consider sweeping these away to free up some digital space!"))
            .and(predicates::str::not(predicates::str::contains("Dry run mode:")))
    );

    temp_dir.close().unwrap();
}
