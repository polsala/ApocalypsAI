use super::{sweep_directory, FileCategory};
use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use tempfile::tempdir;
use filetime::{set_file_times, FileTime};
use chrono::{Utc, Duration};

// Mock rationale: Tests create temporary files and directories with specific modification/access times
// to simulate different 'age' categories without relying on actual file system state or external dependencies.
// The `tempfile` crate is used for isolated test environments, and `filetime` for setting timestamps.

#[test]
fn test_sweep_empty_directory() {
    let dir = tempdir().unwrap();
    let path = dir.path().to_path_buf();
    let results = sweep_directory(&path, false);
    assert!(results.is_empty());
}

#[test]
fn test_sweep_fresh_file() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("fresh_file.txt");
    File::create(&file_path).unwrap().write_all(b"hello").unwrap();

    // Set access time to now
    let now = Utc::now();
    let file_time = FileTime::from_system_time(now.into());
    set_file_times(&file_path, file_time, file_time).unwrap();

    let results = sweep_directory(&dir.path().to_path_buf(), false);
    assert_eq!(results.len(), 1);
    assert!(results.contains_key(&FileCategory::Fresh));
    assert_eq!(results[&FileCategory::Fresh].len(), 1);
    assert_eq!(results[&FileCategory::Fresh][0].path, file_path);
}

#[test]
fn test_sweep_fossilized_file() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("fossilized_file.txt");
    File::create(&file_path).unwrap().write_all(b"old data").unwrap();

    // Set access time to 2 years ago
    let two_years_ago = Utc::now() - Duration::days(365 * 2);
    let file_time = FileTime::from_system_time(two_years_ago.into());
    set_file_times(&file_path, file_time, file_time).unwrap();

    let results = sweep_directory(&dir.path().to_path_buf(), false);
    assert_eq!(results.len(), 1);
    assert!(results.contains_key(&FileCategory::Fossilized));
    assert_eq!(results[&FileCategory::Fossilized].len(), 1);
    assert_eq!(results[&FileCategory::Fossilized][0].path, file_path);
}

#[test]
fn test_sweep_mixed_files() {
    let dir = tempdir().unwrap();
    let path = dir.path().to_path_buf();

    // Fresh file
    let fresh_file = path.join("fresh.txt");
    File::create(&fresh_file).unwrap().write_all(b"fresh").unwrap();
    let now = Utc::now();
    set_file_times(&fresh_file, FileTime::from_system_time(now.into()), FileTime::from_system_time(now.into())).unwrap();

    // Stale file (60 days ago)
    let stale_file = path.join("stale.txt");
    File::create(&stale_file).unwrap().write_all(b"stale").unwrap();
    let sixty_days_ago = now - Duration::days(60);
    set_file_times(&stale_file, FileTime::from_system_time(sixty_days_ago.into()), FileTime::from_system_time(sixty_days_ago.into())).unwrap();

    // Ancient file (200 days ago)
    let ancient_file = path.join("ancient.txt");
    File::create(&ancient_file).unwrap().write_all(b"ancient").unwrap();
    let two_hundred_days_ago = now - Duration::days(200);
    set_file_times(&ancient_file, FileTime::from_system_time(two_hundred_days_ago.into()), FileTime::from_system_time(two_hundred_days_ago.into())).unwrap();

    // Fossilized file (2 years ago)
    let fossilized_file = path.join("fossilized.txt");
    File::create(&fossilized_file).unwrap().write_all(b"fossilized").unwrap();
    let two_years_ago = now - Duration::days(365 * 2);
    set_file_times(&fossilized_file, FileTime::from_system_time(two_years_ago.into()), FileTime::from_system_time(two_years_ago.into())).unwrap();

    let results = sweep_directory(&path, false);

    assert_eq!(results.len(), 4);
    assert_eq!(results[&FileCategory::Fresh].len(), 1);
    assert_eq!(results[&FileCategory::Stale].len(), 1);
    assert_eq!(results[&FileCategory::Ancient].len(), 1);
    assert_eq!(results[&FileCategory::Fossilized].len(), 1);

    assert!(results[&FileCategory::Fresh].iter().any(|f| f.path == fresh_file));
    assert!(results[&FileCategory::Stale].iter().any(|f| f.path == stale_file));
    assert!(results[&FileCategory::Ancient].iter().any(|f| f.path == ancient_file));
    assert!(results[&FileCategory::Fossilized].iter().any(|f| f.path == fossilized_file));
}

#[test]
fn test_sweep_non_existent_path() {
    let non_existent_path = PathBuf::from("/tmp/non_existent_dir_12345");
    let results = sweep_directory(&non_existent_path, false);
    assert!(results.is_empty());
}

#[test]
fn test_file_category_from_duration() {
    assert_eq!(FileCategory::from_duration(Duration::days(0)), FileCategory::Fresh);
    assert_eq!(FileCategory::from_duration(Duration::days(29)), FileCategory::Fresh);
    assert_eq!(FileCategory::from_duration(Duration::days(30)), FileCategory::Stale);
    assert_eq!(FileCategory::from_duration(Duration::days(89)), FileCategory::Stale);
    assert_eq!(FileCategory::from_duration(Duration::days(90)), FileCategory::Ancient);
    assert_eq!(FileCategory::from_duration(Duration::days(364)), FileCategory::Ancient);
    assert_eq!(FileCategory::from_duration(Duration::days(365)), FileCategory::Fossilized);
    assert_eq!(FileCategory::from_duration(Duration::days(730)), FileCategory::Fossilized);
}
