use super::*;
use tempfile::tempdir;
use std::io::{self, Write, Read};
use std::fs::{self, File};
use std::time::{SystemTime, Duration};
use tar::Archive;

// Mock rationale: We create a temporary directory and populate it with files
// of specific ages and sizes to simulate a file system. This allows for
// deterministic and offline testing of the dust detection and collection logic
// without interacting with the actual file system or relying on external factors.

#[test]
fn test_is_dust_detection() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create an old, large file (should be dust)
    let old_large_file_path = path.join("old_large.log");
    File::create(&old_large_file_path)?.write_all(&vec![0; 15 * 1024 * 1024])?; // 15MB
    let thirty_one_days_ago = SystemTime::now() - DurationExt::from_days(31);
    filetime::set_file_mtime(&old_large_file_path, filetime::FileTime::from_system_time(thirty_one_days_ago))?;

    // Create a recent, large file (should not be dust due to age)
    let recent_large_file_path = path.join("recent_large.tmp");
    File::create(&recent_large_file_path)?.write_all(&vec![0; 15 * 1024 * 1024])?; // 15MB
    let one_day_ago = SystemTime::now() - DurationExt::from_days(1);
    filetime::set_file_mtime(&recent_large_file_path, filetime::FileTime::from_system_time(one_day_ago))?;

    // Create an old, small file (should not be dust due to size)
    let old_small_file_path = path.join("old_small.txt");
    File::create(&old_small_file_path)?.write_all(&vec![0; 5 * 1024 * 1024])?; // 5MB
    filetime::set_file_mtime(&old_small_file_path, filetime::FileTime::from_system_time(thirty_one_days_ago))?;

    // Create a directory (should not be dust)
    fs::create_dir(path.join("subdir"))?;

    // Scan with default criteria (age > 30 days, size > 10MB)
    let dust_particles = scan_for_dust_in_path(path, 30, 10 * 1024 * 1024);

    assert_eq!(dust_particles.len(), 1);
    assert_eq!(dust_particles[0].path, old_large_file_path);
    assert_eq!(dust_particles[0].size, 15 * 1024 * 1024);

    Ok(())
}

#[test]
fn test_collect_dust_to_archive_creation() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();
    let output_archive = path.join("stardust.tar.gz");

    // Create some dust files
    let dust_file1_path = path.join("dust1.log");
    File::create(&dust_file1_path)?.write_all(b"content of dust1")?;
    let thirty_one_days_ago = SystemTime::now() - DurationExt::from_days(31);
    filetime::set_file_mtime(&dust_file1_path, filetime::FileTime::from_system_time(thirty_one_days_ago))?;

    let dust_file2_path = path.join("dust2.tmp");
    File::create(&dust_file2_path)?.write_all(b"content of dust2")?;
    filetime::set_file_mtime(&dust_file2_path, filetime::FileTime::from_system_time(thirty_one_days_ago))?;

    // Create a non-dust file (recent, small)
    let non_dust_file_path = path.join("recent.txt");
    File::create(&non_dust_file_path)?.write_all(b"recent content")?;
    let one_day_ago = SystemTime::now() - DurationExt::from_days(1);
    filetime::set_file_mtime(&non_dust_file_path, filetime::FileTime::from_system_time(one_day_ago))?;


    let dust_particles = scan_for_dust_in_path(path, 30, 1); // min_size_bytes = 1 for these small files

    assert_eq!(dust_particles.len(), 2); // Should find dust1 and dust2

    collect_dust_to_archive(&dust_particles, &output_archive, path)?;

    assert!(output_archive.exists());

    // Verify archive contents
    let file = File::open(&output_archive)?;
    let mut archive = Archive::new(flate2::read::GzDecoder::new(file));

    let mut found_files = Vec::new();
    for entry_result in archive.entries()? {
        let mut entry = entry_result?;
        let entry_path = entry.path()?.to_path_buf();
        found_files.push(entry_path.clone());

        let mut content = String::new();
        entry.read_to_string(&mut content)?;

        if entry_path == PathBuf::from("dust1.log") {
            assert_eq!(content, "content of dust1");
        } else if entry_path == PathBuf::from("dust2.tmp") {
            assert_eq!(content, "content of dust2");
        } else {
            panic!("Unexpected file in archive: {:?}", entry_path);
        }
    }

    assert_eq!(found_files.len(), 2);
    assert!(found_files.contains(&PathBuf::from("dust1.log")));
    assert!(found_files.contains(&PathBuf::from("dust2.tmp")));

    Ok(())
}
