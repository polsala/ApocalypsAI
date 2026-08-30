#![allow(unused_imports)] // Allow unused imports for test setup

use super::*;
use std::fs::{self, File};
use std::io::Write;
use std::time::{SystemTime, UNIX_EPOCH};
use tempfile::tempdir;
use filetime::{set_file_mtime, FileTime};

// Mock rationale: File system operations are inherently non-deterministic (timestamps change, actual files exist).
// Using a temporary directory and creating files with controlled metadata allows for deterministic, offline testing.

fn create_test_file(path: &Path, size_bytes: u64, mtime: SystemTime) -> Result<(), Box<dyn std::error::Error>> {
    let mut file = File::create(path)?;
    // Write some content to reach the desired size
    let content = vec![0; size_bytes as usize];
    file.write_all(&content)?;
    file.sync_all()?;

    // Set modification time
    let ft = FileTime::from_system_time(mtime);
    set_file_mtime(path, ft)?;
    Ok(())
}

#[test]
fn test_dust_bunny_identification() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let base_path = temp_dir.path();

    let now = SystemTime::now();
    let one_day_ago = now - Duration::from_secs(24 * 60 * 60);
    let two_years_ago = now - Duration::from_secs(730 * 24 * 60 * 60);
    let one_year_ago = now - Duration::from_secs(365 * 24 * 60 * 60);
    let six_months_ago = now - Duration::from_secs(180 * 24 * 60 * 60);

    // File 1: Old & Large (should be a dust bunny)
    let old_large_path = base_path.join("old_large.log");
    create_test_file(&old_large_path, 150 * 1024 * 1024, two_years_ago)?;

    // File 2: Old & Small (should be a dust bunny if age threshold met)
    let old_small_path = base_path.join("old_small.txt");
    create_test_file(&old_small_path, 5 * 1024 * 1024, one_year_ago)?;

    // File 3: Recent & Large (should be a dust bunny if size threshold met)
    let recent_large_path = base_path.join("recent_large.zip");
    create_test_file(&recent_large_path, 200 * 1024 * 1024, one_day_ago)?;

    // File 4: Recent & Small (should NOT be a dust bunny)
    let recent_small_path = base_path.join("recent_small.md");
    create_test_file(&recent_small_path, 1 * 1024 * 1024, one_day_ago)?;

    // File 5: Old & Small, in a subdirectory (should be a dust bunny if age threshold met)
    let sub_dir = base_path.join("subdir");
    fs::create_dir(&sub_dir)?;
    let sub_old_small_path = sub_dir.join("sub_old_small.conf");
    create_test_file(&sub_old_small_path, 2 * 1024 * 1024, six_months_ago)?;

    // Test Case 1: Default thresholds (age=365 days, size=100 MB)
    let mut bunnies = Vec::new();
    for entry in WalkDir::new(base_path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = path.metadata() {
                if let Some(bunny) = DustBunny::new(path.to_path_buf(), &metadata) {
                    if bunny.is_old(365) || bunny.is_large(100) {
                        bunnies.push(bunny);
                    }
                }
            }
        }
    }
    assert_eq!(bunnies.len(), 3, "Expected 3 dust bunnies with default thresholds");
    assert!(bunnies.iter().any(|b| b.path == old_large_path));
    assert!(bunnies.iter().any(|b| b.path == old_small_path)); // 1 year old (365 days) is >= 365 days
    assert!(bunnies.iter().any(|b| b.path == recent_large_path));
    assert!(!bunnies.iter().any(|b| b.path == recent_small_path));
    assert!(!bunnies.iter().any(|b| b.path == sub_old_small_path)); // 6 months old is < 365 days, 2MB is < 100MB

    // Test Case 2: Only age threshold (e.g., 180 days), no size limit (size=0)
    let mut bunnies_age_only = Vec::new();
    for entry in WalkDir::new(base_path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = path.metadata() {
                if let Some(bunny) = DustBunny::new(path.to_path_buf(), &metadata) {
                    if bunny.is_old(180) || bunny.is_large(0) {
                        bunnies_age_only.push(bunny);
                    }
                }
            }
        }
    }
    assert_eq!(bunnies_age_only.len(), 3, "Expected 3 dust bunnies with age-only threshold (180 days)");
    assert!(bunnies_age_only.iter().any(|b| b.path == old_large_path));
    assert!(bunnies_age_only.iter().any(|b| b.path == old_small_path));
    assert!(bunnies_age_only.iter().any(|b| b.path == sub_old_small_path)); // 6 months old (180 days) is >= 180 days
    assert!(!bunnies_age_only.iter().any(|b| b.path == recent_large_path));
    assert!(!bunnies_age_only.iter().any(|b| b.path == recent_small_path));

    // Test Case 3: Only size threshold (e.g., 10 MB), no age limit (age=0)
    let mut bunnies_size_only = Vec::new();
    for entry in WalkDir::new(base_path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = path.metadata() {
                if let Some(bunny) = DustBunny::new(path.to_path_buf(), &metadata) {
                    if bunny.is_old(0) || bunny.is_large(10) {
                        bunnies_size_only.push(bunny);
                    }
                }
            }
        }
    }
    assert_eq!(bunnies_size_only.len(), 2, "Expected 2 dust bunnies with size-only threshold (10 MB)");
    assert!(bunnies_size_only.iter().any(|b| b.path == old_large_path));
    assert!(bunnies_size_only.iter().any(|b| b.path == recent_large_path));
    assert!(!bunnies_size_only.iter().any(|b| b.path == old_small_path));
    assert!(!bunnies_size_only.iter().any(|b| b.path == recent_small_path));
    assert!(!bunnies_size_only.iter().any(|b| b.path == sub_old_small_path));

    Ok(())
}

#[test]
fn test_dust_bunny_report_line() -> Result<(), Box<dyn std::error::Error>> {
    let temp_dir = tempdir()?;
    let base_path = temp_dir.path();

    let now = SystemTime::now();
    let two_years_ago = now - Duration::from_secs(730 * 24 * 60 * 60);

    let test_path = base_path.join("report_test_file.log");
    create_test_file(&test_path, 123_456_789, two_years_ago)?;

    let metadata = test_path.metadata()?;
    let bunny = DustBunny::new(test_path.to_path_buf(), &metadata).unwrap();

    let report = bunny.report_line();
    // Check for path, size (approx 117.74 MB), and age (approx 730 days ago)
    assert!(report.contains(&format!("{}", test_path.display())));
    assert!(report.contains("117.74 MB")); // 123456789 / (1024*1024) = 117.738... MB
    assert!(report.contains("last modified 730 days ago") || report.contains("last modified 729 days ago")); // Due to slight time differences during test execution

    Ok(())
}
