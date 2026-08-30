use crate::{classify_path, TemporalStatus, DurationExt};
use std::fs::{self, File};
use std::io::Write;
use std::path::Path;
use std::time::{SystemTime, Duration};
use tempfile::tempdir; // For creating temporary directories

// Mock rationale: We use `tempfile` to create isolated, temporary file system structures
// with controlled modification times. This ensures tests are deterministic,
// run offline, and don't interfere with the actual file system.
// We manually set modification times for precise temporal classification testing.

#[test]
fn test_classify_fresh_sprout() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("fresh_file.txt");
    File::create(&file_path).unwrap().write_all(b"hello").unwrap();

    // Ensure the file is very recent
    let now = SystemTime::now();
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(now)).unwrap();

    assert_eq!(classify_path(&file_path), TemporalStatus::FreshSprout);
}

#[test]
fn test_classify_blooming_archive() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("blooming_file.txt");
    File::create(&file_path).unwrap().write_all(b"hello").unwrap();

    // Set modification time to 15 days ago
    let fifteen_days_ago = SystemTime::now() - Duration::from_days(15);
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(fifteen_days_ago)).unwrap();

    assert_eq!(classify_path(&file_path), TemporalStatus::BloomingArchive);
}

#[test]
fn test_classify_dusty_tome() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("dusty_file.txt");
    File::create(&file_path).unwrap().write_all(b"hello").unwrap();

    // Set modification time to 90 days ago
    let ninety_days_ago = SystemTime::now() - Duration::from_days(90);
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(ninety_days_ago)).unwrap();

    assert_eq!(classify_path(&file_path), TemporalStatus::DustyTome);
}

#[test]
fn test_classify_ancient_relic() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("relic_file.txt");
    File::create(&file_path).unwrap().write_all(b"hello").unwrap();

    // Set modification time to 200 days ago
    let two_hundred_days_ago = SystemTime::now() - Duration::from_days(200);
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(two_hundred_days_ago)).unwrap();

    assert_eq!(classify_path(&file_path), TemporalStatus::AncientRelic);
}

#[test]
fn test_classify_forgotten_echo() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("forgotten_file.txt");
    File::create(&file_path).unwrap().write_all(b"hello").unwrap();

    // Set modification time to 400 days ago
    let four_hundred_days_ago = SystemTime::now() - Duration::from_days(400);
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(four_hundred_days_ago)).unwrap();

    assert_eq!(classify_path(&file_path), TemporalStatus::ForgottenEcho);
}

#[test]
fn test_classify_non_existent_path() {
    let non_existent_path = Path::new("/this/path/does/not/exist/definitely");
    assert_eq!(classify_path(non_existent_path), TemporalStatus::Unknown);
}

#[test]
fn test_duration_from_days() {
    assert_eq!(Duration::from_days(1), Duration::from_secs(24 * 60 * 60));
    assert_eq!(Duration::from_days(7), Duration::from_secs(7 * 24 * 60 * 60));
    assert_eq!(Duration::from_days(30), Duration::from_secs(30 * 24 * 60 * 60));
}

// Additional test for directory classification
#[test]
fn test_classify_directory() {
    let dir = tempdir().unwrap();
    let sub_dir_path = dir.path().join("sub_dir");
    fs::create_dir(&sub_dir_path).unwrap();

    // Set modification time to 5 days ago
    let five_days_ago = SystemTime::now() - Duration::from_days(5);
    filetime::set_file_mtime(&sub_dir_path, filetime::FileTime::from_system_time(five_days_ago)).unwrap();

    assert_eq!(classify_path(&sub_dir_path), TemporalStatus::FreshSprout);
}

// Test for a file with a future modification time (should result in Unknown due to `duration_since` returning an error)
#[test]
fn test_classify_future_modified_time() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("future_file.txt");
    File::create(&file_path).unwrap().write_all(b"future").unwrap();

    // Set modification time to 1 day in the future
    let one_day_in_future = SystemTime::now() + Duration::from_days(1);
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(one_day_in_future)).unwrap();

    // `duration_since` returns an error if the other time is later, which we handle as Unknown
    assert_eq!(classify_path(&file_path), TemporalStatus::Unknown);
}
