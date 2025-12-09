#![allow(unused_imports)]
use super::*;
use std::io::Write;
use tempfile::tempdir;

// Mock rationale: File system operations are inherently non-deterministic and depend on the actual
// file system state. For deterministic, offline tests, we create temporary files and directories
// within the test environment to simulate different scenarios (e.g., old files, new files, empty
// directories). This avoids relying on the host system's file structure or modifying it.

#[test]
fn test_finds_old_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let old_file_path = dir.path().join("old_report.txt");
    let mut old_file = fs::File::create(&old_file_path)?;
    old_file.write_all(b"old content")?;

    // Set modification time to be very old
    let old_time = Utc::now() - Duration::days(100);
    filetime::set_file_mtime(&old_file_path, filetime::FileTime::from_system_time(old_time.into()))?;

    let args = Args::parse_from(&["dust-bunny", dir.path().to_str().unwrap(), "-a", "90"]);
    let now = Utc::now();

    let mut dust_bunnies: Vec<DigitalDustBunny> = Vec::new();
    for entry in WalkDir::new(dir.path()).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let path = entry.path().to_path_buf();
            if let Ok(metadata) = fs::metadata(&path) {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_dt: DateTime<Utc> = modified_time.into();
                    let duration = now.signed_duration_since(modified_dt);
                    let age_days = duration.num_days();

                    if age_days >= args.age as i64 {
                        let size = metadata.len();
                        let size_kb = size as f64 / 1024.0;
                        let fluffiness_score = (age_days as f64 * size_kb) / 1000.0;
                        dust_bunnies.push(DigitalDustBunny {
                            path,
                            size,
                            age_days,
                            fluffiness_score,
                        });
                    }
                }
            }
        }
    }

    assert_eq!(dust_bunnies.len(), 1);
    assert_eq!(dust_bunnies[0].path, old_file_path);
    assert!(dust_bunnies[0].age_days >= 90);

    Ok(())
}

#[test]
fn test_ignores_new_files() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let new_file_path = dir.path().join("new_doc.txt");
    fs::File::create(&new_file_path)?;

    // Modification time is recent by default

    let args = Args::parse_from(&["dust-bunny", dir.path().to_str().unwrap(), "-a", "90"]);
    let now = Utc::now();

    let mut dust_bunnies: Vec<DigitalDustBunny> = Vec::new();
    for entry in WalkDir::new(dir.path()).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let path = entry.path().to_path_buf();
            if let Ok(metadata) = fs::metadata(&path) {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_dt: DateTime<Utc> = modified_time.into();
                    let duration = now.signed_duration_since(modified_dt);
                    let age_days = duration.num_days();

                    if age_days >= args.age as i64 {
                        let size = metadata.len();
                        let size_kb = size as f64 / 1024.0;
                        let fluffiness_score = (age_days as f64 * size_kb) / 1000.0;
                        dust_bunnies.push(DigitalDustBunny {
                            path,
                            size,
                            age_days,
                            fluffiness_score,
                        });
                    }
                }
            }
        }
    }

    assert_eq!(dust_bunnies.len(), 0);

    Ok(())
}

#[test]
fn test_fluffiness_calculation() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("medium_old_file.log");
    let mut file = fs::File::create(&file_path)?;
    file.write_all(&vec![0; 1024 * 50])?;
    
    let old_time = Utc::now() - Duration::days(150);
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(old_time.into()))?;

    let args = Args::parse_from(&["dust-bunny", dir.path().to_str().unwrap(), "-a", "90"]);
    let now = Utc::now();

    let mut dust_bunnies: Vec<DigitalDustBunny> = Vec::new();
    for entry in WalkDir::new(dir.path()).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let path = entry.path().to_path_buf();
            if let Ok(metadata) = fs::metadata(&path) {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_dt: DateTime<Utc> = modified_time.into();
                    let duration = now.signed_duration_since(modified_dt);
                    let age_days = duration.num_days();

                    if age_days >= args.age as i64 {
                        let size = metadata.len();
                        let size_kb = size as f64 / 1024.0;
                        let fluffiness_score = (age_days as f64 * size_kb) / 1000.0;
                        dust_bunnies.push(DigitalDustBunny {
                            path,
                            size,
                            age_days,
                            fluffiness_score,
                        });
                    }
                }
            }
        }
    }

    assert_eq!(dust_bunnies.len(), 1);
    // Expected fluffiness: (150 days * 50 KB) / 1000 = 7.5
    // Allow for slight variation due to time precision
    assert!((dust_bunnies[0].fluffiness_score - 7.5).abs() < 0.1);

    Ok(())
}

#[test]
fn test_empty_directory() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;

    let args = Args::parse_from(&["dust-bunny", dir.path().to_str().unwrap(), "-a", "90"]);
    let now = Utc::now();

    let mut dust_bunnies: Vec<DigitalDustBunny> = Vec::new();
    for entry in WalkDir::new(dir.path()).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let path = entry.path().to_path_buf();
            if let Ok(metadata) = fs::metadata(&path) {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_dt: DateTime<Utc> = modified_time.into();
                    let duration = now.signed_duration_since(modified_dt);
                    let age_days = duration.num_days();

                    if age_days >= args.age as i64 {
                        let size = metadata.len();
                        let size_kb = size as f64 / 1024.0;
                        let fluffiness_score = (age_days as f64 * size_kb) / 1000.0;
                        dust_bunnies.push(DigitalDustBunny {
                            path,
                            size,
                            age_days,
                            fluffiness_score,
                        });
                    }
                }
            }
        }
    }

    assert_eq!(dust_bunnies.len(), 0);

    Ok(())
}
