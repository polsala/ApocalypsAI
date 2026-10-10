use super::*;
use std::io::Write;
use tempfile::tempdir;
use chrono::{TimeZone, Duration};

// Mock rationale: Tests create temporary files. The `find_relics` function accepts a `now` parameter,
// allowing tests to define a specific reference point in time for age calculations. This ensures
// deterministic results without relying on the actual current system time or external filesystem
// state beyond the temporary test directory. Files created during the test will have their
// modification time set to the actual system time at creation, and the `test_now` parameter
// is then adjusted to simulate different ages relative to these creation times.

#[test]
fn test_find_relics_no_relics() {
    let dir = tempdir().unwrap();
    let path = dir.path().to_path_buf();

    let min_age_days = 90;
    // `test_now` is set such that files created *now* (during test execution)
    // are not old enough to be considered relics.
    let test_now = Utc::now() + Duration::days(min_age_days - 1); // 89 days after file creation

    // Create a file that is NOT a relic
    let fresh_file_path = path.join("fresh_file.txt");
    std::fs::write(&fresh_file_path, "fresh content").unwrap();

    let relics = find_relics(&path, min_age_days, test_now);
    assert!(relics.is_empty(), "Expected no relics, but found {}: {:?}", relics.len(), relics.iter().map(|r| r.path.display()).collect::<Vec<_>>());

    dir.close().unwrap();
}

#[test]
fn test_find_relics_with_relics() {
    let dir = tempdir().unwrap();
    let path = dir.path().to_path_buf();

    let min_age_days = 90;
    // `test_now` is set such that files created *now* (during test execution)
    // are old enough to be considered relics.
    let test_now = Utc::now() + Duration::days(min_age_days + 1); // 91 days after file creation

    // Create a file that IS a relic
    let relic_file_path = path.join("old_relic.txt");
    std::fs::write(&relic_file_path, "old content").unwrap();

    let relics = find_relics(&path, min_age_days, test_now);
    assert_eq!(relics.len(), 1, "Expected 1 relic, found {}", relics.len());
    assert!(relics.iter().any(|r| r.path.ends_with("old_relic.txt")));
    assert!(relics.iter().all(|r| r.age_days >= min_age_days));

    dir.close().unwrap();
}

#[test]
fn test_find_relics_empty_dir() {
    let dir = tempdir().unwrap();
    let path = dir.path().to_path_buf();

    let test_now = Utc::now() + Duration::days(100);
    let min_age_days = 90;

    let relics = find_relics(&path, min_age_days, test_now);
    assert!(relics.is_empty(), "Expected no relics in empty directory.");

    dir.close().unwrap();
}

#[test]
fn test_find_relics_subdirectories() {
    let dir = tempdir().unwrap();
    let path = dir.path().to_path_buf();

    let sub_dir = path.join("sub");
    std::fs::create_dir(&sub_dir).unwrap();

    let min_age_days = 90;
    let test_now = Utc::now() + Duration::days(min_age_days + 1);

    // Create a relic in the subdirectory
    std::fs::write(sub_dir.join("sub_relic.txt"), "sub content").unwrap();
    // Create a relic in the root directory
    std::fs::write(path.join("root_relic.txt"), "root content").unwrap();

    let relics = find_relics(&path, min_age_days, test_now);
    assert_eq!(relics.len(), 2, "Expected 2 relics across directories, found {}", relics.len());
    assert!(relics.iter().any(|r| r.path.ends_with("sub_relic.txt")));
    assert!(relics.iter().any(|r| r.path.ends_with("root_relic.txt")));
    assert!(relics.iter().all(|r| r.age_days >= min_age_days));

    dir.close().unwrap();
}

#[test]
fn test_find_relics_mixed_files() {
    let dir = tempdir().unwrap();
    let path = dir.path().to_path_buf();

    let min_age_days = 90;
    let test_now = Utc::now() + Duration::days(min_age_days + 1); // Makes files created now 'relics'

    // Relic file
    std::fs::write(path.join("relic_file.txt"), "old data").unwrap();

    // Fresh file (will also be a relic with this `test_now` strategy, but tests the count)
    std::fs::write(path.join("fresh_file.txt"), "new data").unwrap();

    let relics = find_relics(&path, min_age_days, test_now);
    assert_eq!(relics.len(), 2, "Expected 2 relics, found {}", relics.len());
    assert!(relics.iter().any(|r| r.path.ends_with("relic_file.txt")));
    assert!(relics.iter().any(|r| r.path.ends_with("fresh_file.txt")));

    dir.close().unwrap();
}
