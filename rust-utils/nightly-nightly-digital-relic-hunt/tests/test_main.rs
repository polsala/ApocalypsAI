use super::{parse_size_string, parse_duration_string, format_bytes, find_relics_in_path};
use chrono::{Utc, Duration, DateTime};
use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use tempfile::tempdir;

// Mock rationale: File system operations are non-deterministic and depend on the host environment.
// Using a temporary directory with controlled file creation ensures deterministic and isolated tests.

#[test]
fn test_parse_size_string() {
    assert_eq!(parse_size_string("100").unwrap(), 100);
    assert_eq!(parse_size_string("100B").unwrap(), 100);
    assert_eq!(parse_size_string("1K").unwrap(), 1024);
    assert_eq!(parse_size_string("1KB").unwrap(), 1024);
    assert_eq!(parse_size_string("2M").unwrap(), 2 * 1024 * 1024);
    assert_eq!(parse_size_string("2MB").unwrap(), 2 * 1024 * 1024);
    assert_eq!(parse_size_string("3G").unwrap(), 3 * 1024 * 1024 * 1024);
    assert_eq!(parse_size_string("3GB").unwrap(), 3 * 1024 * 1024 * 1024);
    assert_eq!(parse_size_string("4T").unwrap(), 4 * 1024 * 1024 * 1024 * 1024);
    assert!(parse_size_string("abc").is_err());
    assert!(parse_size_string("100X").is_err());
}

#[test]
fn test_parse_duration_string() {
    assert_eq!(parse_duration_string("10d").unwrap(), Duration::days(10));
    assert_eq!(parse_duration_string("2w").unwrap(), Duration::weeks(2));
    assert_eq!(parse_duration_string("1y").unwrap(), Duration::days(365));
    assert!(parse_duration_string("abc").is_err());
    assert!(parse_duration_string("10h").is_err());
}

#[test]
fn test_format_bytes() {
    assert_eq!(format_bytes(0), "0 B");
    assert_eq!(format_bytes(500), "500 B");
    assert_eq!(format_bytes(1024), "1.00 KB");
    assert_eq!(format_bytes(1536), "1.50 KB");
    assert_eq!(format_bytes(1024 * 1024), "1.00 MB");
    assert_eq!(format_bytes(1024 * 1024 * 1024), "1.00 GB");
    assert_eq!(format_bytes(1024 * 1024 * 1024 * 1024), "1.00 TB");
}

#[test]
fn test_find_relics_size_filter() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path().to_path_buf();

    // Create mock files with different sizes
    File::create(path.join("small.txt"))?.write_all(&[0; 100])?;
    File::create(path.join("medium.txt"))?.write_all(&[0; 1024])?;
    File::create(path.join("large.txt"))?.write_all(&[0; 2048])?;

    let now = Utc::now();

    // Test 1: min_size = 1KB (1024 bytes)
    let relics = find_relics_in_path(&path, 1024, None, now)?;
    assert_eq!(relics.len(), 2);
    assert!(relics.iter().any(|(p, _, _)| p.ends_with("medium.txt")));
    assert!(relics.iter().any(|(p, _, _)| p.ends_with("large.txt")));

    // Test 2: min_size = 2KB (2048 bytes)
    let relics = find_relics_in_path(&path, 2048, None, now)?;
    assert_eq!(relics.len(), 1);
    assert!(relics.iter().any(|(p, _, _)| p.ends_with("large.txt")));

    // Test 3: min_size = 0 (no size filter)
    let relics = find_relics_in_path(&path, 0, None, now)?;
    assert_eq!(relics.len(), 3);

    Ok(())
}

#[test]
fn test_find_relics_age_filter() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path().to_path_buf();

    let now = Utc::now();

    // Create mock files with controlled modification times
    let old_file_path = path.join("old.txt");
    File::create(&old_file_path)?.write_all(&[0; 500])?;
    // Set modification time to 60 days ago
    let sixty_days_ago = now - Duration::days(60);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(sixty_days_ago.into()))?;

    let recent_file_path = path.join("recent.txt");
    File::create(&recent_file_path)?.write_all(&[0; 500])?;
    // Set modification time to 10 days ago
    let ten_days_ago = now - Duration::days(10);
    filetime::set_file_mtime(&recent_file_path, filetime::FileTime::from_system_time(ten_days_ago.into()))?;

    // Test 1: max_age = 30 days (files older than 30 days)
    let relics = find_relics_in_path(&path, 0, Some(Duration::days(30)), now)?;
    assert_eq!(relics.len(), 1);
    assert!(relics.iter().any(|(p, _, _)| p.ends_with("old.txt")));

    // Test 2: max_age = 90 days (files older than 90 days - none should match)
    let relics = find_relics_in_path(&path, 0, Some(Duration::days(90)), now)?;
    assert_eq!(relics.len(), 0);

    // Test 3: max_age = 5 days (both should match)
    let relics = find_relics_in_path(&path, 0, Some(Duration::days(5)), now)?;
    assert_eq!(relics.len(), 2);
    assert!(relics.iter().any(|(p, _, _)| p.ends_with("old.txt")));
    assert!(relics.iter().any(|(p, _, _)| p.ends_with("recent.txt")));

    Ok(())
}

#[test]
fn test_find_relics_combined_filter() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path().to_path_buf();

    let now = Utc::now();

    // File 1: Large & Old
    let file1_path = path.join("large_old.bin");
    File::create(&file1_path)?.write_all(&[0; 5000])?;
    let sixty_days_ago = now - Duration::days(60);
    filetime::set_file_mtime(&file1_path, filetime::FileTime::from_system_time(sixty_days_ago.into()))?;

    // File 2: Small & Old
    let file2_path = path.join("small_old.txt");
    File::create(&file2_path)?.write_all(&[0; 100])?;
    filetime::set_file_mtime(&file2_path, filetime::FileTime::from_system_time(sixty_days_ago.into()))?;

    // File 3: Large & Recent
    let file3_path = path.join("large_recent.bin");
    File::create(&file3_path)?.write_all(&[0; 5000])?;
    let ten_days_ago = now - Duration::days(10);
    filetime::set_file_mtime(&file3_path, filetime::FileTime::from_system_time(ten_days_ago.into()))?;

    // Test: min_size = 1KB (1024 bytes), max_age = 30 days
    let relics = find_relics_in_path(&path, 1024, Some(Duration::days(30)), now)?;
    assert_eq!(relics.len(), 1);
    assert!(relics.iter().any(|(p, _, _)| p.ends_with("large_old.bin")));

    Ok(())
}
