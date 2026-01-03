use super::{calculate_decay_score, FileDecayInfo};
use std::fs;
use std::path::PathBuf;
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use tempfile::tempdir;

// Mock rationale: Using tempfile::tempdir to create isolated, temporary directories
// and files allows for deterministic testing of file system interactions without
// affecting the actual file system or relying on external state. Timestamps are
// explicitly set or derived from a controlled 'now' for consistent decay score calculation.

#[test]
fn test_calculate_decay_score() {
    let now = SystemTime::now();

    // File modified 10 days ago, accessed 5 days ago
    let mtime_10_days_ago = now - Duration::from_secs(10 * 24 * 60 * 60);
    let atime_5_days_ago = now - Duration::from_secs(5 * 24 * 60 * 60);
    let score = calculate_decay_score(mtime_10_days_ago, atime_5_days_ago);
    // Expected: (10 * 0.8) + (5 * 0.2) = 8 + 1 = 9
    assert!((score - 9.0).abs() < 0.001, "Score for 10 days mtime, 5 days atime should be ~9.0");

    // File modified 1 day ago, accessed 1 day ago
    let mtime_1_day_ago = now - Duration::from_secs(1 * 24 * 60 * 60);
    let atime_1_day_ago = now - Duration::from_secs(1 * 24 * 60 * 60);
    let score = calculate_decay_score(mtime_1_day_ago, atime_1_day_ago);
    // Expected: (1 * 0.8) + (1 * 0.2) = 0.8 + 0.2 = 1
    assert!((score - 1.0).abs() < 0.001, "Score for 1 day mtime, 1 day atime should be ~1.0");

    // File modified in the future (should result in 0 decay)
    let mtime_future = now + Duration::from_secs(100);
    let atime_future = now + Duration::from_secs(50);
    let score = calculate_decay_score(mtime_future, atime_future);
    assert!((score - 0.0).abs() < 0.001, "Score for future timestamps should be ~0.0");
}

#[test]
fn test_file_decay_info_partial_ordering() {
    let now = SystemTime::now();

    let file1 = FileDecayInfo {
        path: PathBuf::from("file1.txt"),
        decay_score: 10.5,
        mtime: now - Duration::from_secs(1000),
        atime: now - Duration::from_secs(500),
    };
    let file2 = FileDecayInfo {
        path: PathBuf::from("file2.txt"),
        decay_score: 5.2,
        mtime: now - Duration::from_secs(2000),
        atime: now - Duration::from_secs(1000),
    };
    let file3 = FileDecayInfo {
        path: PathBuf::from("file3.txt"),
        decay_score: 10.5,
        mtime: now - Duration::from_secs(1000),
        atime: now - Duration::from_secs(500),
    };

    assert!(file1 > file2);
    assert!(file2 < file1);
    assert!(file1 == file3);
}

#[test]
fn test_file_system_interaction_and_metadata_reading() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path_old = dir.path().join("old_file.txt");
    let file_path_recent = dir.path().join("recent_file.txt");
    let subdir = dir.path().join("subdir");
    let subdir_file = subdir.join("subdir_file.txt");

    fs::create_dir(&subdir)?;
    fs::write(&file_path_old, "old content")?;
    fs::write(&file_path_recent, "recent content")?;
    fs::write(&subdir_file, "subdir content")?;

    // Verify that `fs::metadata` works and `calculate_decay_score` can be called.
    let metadata_old = fs::metadata(&file_path_old)?;
    let score_old = calculate_decay_score(metadata_old.modified()?, metadata_old.accessed()?);
    assert!(score_old >= 0.0, "Score should be non-negative");

    let metadata_recent = fs::metadata(&file_path_recent)?;
    let score_recent = calculate_decay_score(metadata_recent.modified()?, metadata_recent.accessed()?);
    assert!(score_recent >= 0.0, "Score should be non-negative");

    // Verify that `WalkDir` finds the files
    let mut found_files = Vec::new();
    for entry in walkdir::WalkDir::new(dir.path())
        .into_iter()
        .filter_map(|e| e.ok())
    {
        if entry.path().is_file() {
            found_files.push(entry.path().to_path_buf());
        }
    }
    assert_eq!(found_files.len(), 3, "Should find 3 files");
    assert!(found_files.contains(&file_path_old));
    assert!(found_files.contains(&file_path_recent));
    assert!(found_files.contains(&subdir_file));

    Ok(())
}
