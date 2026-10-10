use super::*;
use tempfile::tempdir;
use std::io::Write;
use std::time::{Duration, SystemTime};
use filetime::{set_file_mtime, FileTime};

// Mock rationale: To ensure deterministic and offline testing, file system operations are simulated
// using a temporary directory populated with known files and metadata, and SystemTime::now() is
// mocked by passing a fixed `now` parameter to the functions, avoiding actual system interaction or external dependencies.

#[test]
fn test_calculate_rot_score() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("test_file.txt");
    let mut file = fs::File::create(&file_path).unwrap();
    file.write_all(&vec![0; 20 * 1024 * 1024]).unwrap(); // 20 MB

    let fixed_now = SystemTime::UNIX_EPOCH + Duration::from_secs(365 * 2 * 24 * 60 * 60); // 2 years after epoch
    let modified_time = SystemTime::UNIX_EPOCH + Duration::from_secs(365 * 1 * 24 * 60 * 60); // 1 year after epoch
    set_file_mtime(&file_path, FileTime::from_system_time(modified_time)).unwrap();

    let metadata = fs::metadata(&file_path).unwrap();

    // File is 1 year old (365 days), 20MB. Min age 365 days, min size 10MB.
    // Age: (2 years - 1 year) = 1 year = 365 days
    // Score: 365 days * 20 MB = 7300
    assert_eq!(calculate_rot_score(&metadata, 365, 10, fixed_now), Some(7300));

    // File too young (min_age_days = 730, but file is only 365 days old)
    assert_eq!(calculate_rot_score(&metadata, 730, 10, fixed_now), None);

    // File too small (min_size_mb = 30, but file is only 20MB)
    assert_eq!(calculate_rot_score(&metadata, 365, 30, fixed_now), None);

    // File just meets criteria
    assert_eq!(calculate_rot_score(&metadata, 365, 20, fixed_now), Some(7300));
}

#[test]
fn test_find_rot_files() {
    let dir = tempdir().unwrap();
    let fixed_now = SystemTime::UNIX_EPOCH + Duration::from_secs(365 * 3 * 24 * 60 * 60); // 3 years after epoch

    // File 1: 2 years old, 15MB. Score: 730 (days) * 15 (MB) = 10950
    let file1_path = dir.path().join("old_large.log");
    let mut file1 = fs::File::create(&file1_path).unwrap();
    file1.write_all(&vec![0; 15 * 1024 * 1024]).unwrap(); // 15 MB
    let modified_time1 = SystemTime::UNIX_EPOCH + Duration::from_secs(365 * 1 * 24 * 60 * 60); // 1 year after epoch
    set_file_mtime(&file1_path, FileTime::from_system_time(modified_time1)).unwrap();

    // File 2: ~6 months old, 50MB. Too young (age is 0.5 years, min_age_days is 365).
    let file2_path = dir.path().join("young_large.data");
    let mut file2 = fs::File::create(&file2_path).unwrap();
    file2.write_all(&vec![0; 50 * 1024 * 1024]).unwrap(); // 50 MB
    let modified_time2 = SystemTime::UNIX_EPOCH + Duration::from_secs((365 * 2) * 24 * 60 * 60 + 180 * 24 * 60 * 60); // 2.5 years after epoch
    set_file_mtime(&file2_path, FileTime::from_system_time(modified_time2)).unwrap();

    // File 3: 2 years old, 5MB. Too small (size is 5MB, min_size_mb is 10).
    let file3_path = dir.path().join("old_small.txt");
    let mut file3 = fs::File::create(&file3_path).unwrap();
    file3.write_all(&vec![0; 5 * 1024 * 1024]).unwrap(); // 5 MB
    let modified_time3 = SystemTime::UNIX_EPOCH + Duration::from_secs(365 * 1 * 24 * 60 * 60); // 1 year after epoch
    set_file_mtime(&file3_path, FileTime::from_system_time(modified_time3)).unwrap();

    // File 4: 2 years old, 25MB. Score: 730 (days) * 25 (MB) = 18250
    let file4_path = dir.path().join("another_old_large.bak");
    let mut file4 = fs::File::create(&file4_path).unwrap();
    file4.write_all(&vec![0; 25 * 1024 * 1024]).unwrap(); // 25 MB
    let modified_time4 = SystemTime::UNIX_EPOCH + Duration::from_secs(365 * 1 * 24 * 60 * 60); // 1 year after epoch
    set_file_mtime(&file4_path, FileTime::from_system_time(modified_time4)).unwrap();

    let rot_files = find_rot_files(dir.path(), 365, 10, fixed_now);

    assert_eq!(rot_files.len(), 2);

    // Expected scores (sorted descending):
    // file4: age_days = 365 * 2 = 730, size_mb = 25. Score = 730 * 25 = 18250
    // file1: age_days = 365 * 2 = 730, size_mb = 15. Score = 730 * 15 = 10950

    assert_eq!(rot_files[0].rot_score, 18250);
    assert_eq!(rot_files[0].path, file4_path);
    assert_eq!(rot_files[0].size_mb, 25);
    assert_eq!(rot_files[0].age_days, 730);

    assert_eq!(rot_files[1].rot_score, 10950);
    assert_eq!(rot_files[1].path, file1_path);
    assert_eq!(rot_files[1].size_mb, 15);
    assert_eq!(rot_files[1].age_days, 730);
}

#[test]
fn test_find_rot_files_empty_dir() {
    let dir = tempdir().unwrap();
    let fixed_now = SystemTime::UNIX_EPOCH + Duration::from_secs(365 * 3 * 24 * 60 * 60);

    let rot_files = find_rot_files(dir.path(), 365, 10, fixed_now);
    assert!(rot_files.is_empty());
}

#[test]
fn test_find_rot_files_nested_dir() {
    let dir = tempdir().unwrap();
    let nested_dir = dir.path().join("nested");
    fs::create_dir(&nested_dir).unwrap();

    let fixed_now = SystemTime::UNIX_EPOCH + Duration::from_secs(365 * 3 * 24 * 60 * 60);

    // File in nested dir: 2 years old, 12MB. Score: 730 (days) * 12 (MB) = 8760
    let nested_file_path = nested_dir.join("nested_rot.data");
    let mut nested_file = fs::File::create(&nested_file_path).unwrap();
    nested_file.write_all(&vec![0; 12 * 1024 * 1024]).unwrap(); // 12 MB
    let modified_time = SystemTime::UNIX_EPOCH + Duration::from_secs(365 * 1 * 24 * 60 * 60); // 1 year after epoch
    set_file_mtime(&nested_file_path, FileTime::from_system_time(modified_time)).unwrap();

    let rot_files = find_rot_files(dir.path(), 365, 10, fixed_now);

    assert_eq!(rot_files.len(), 1);
    assert_eq!(rot_files[0].rot_score, 8760);
    assert_eq!(rot_files[0].path, nested_file_path);
}
