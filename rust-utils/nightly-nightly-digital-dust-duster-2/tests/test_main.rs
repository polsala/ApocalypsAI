use super::*;
use tempfile::{tempdir, NamedTempFile};
use std::fs::{self, File};
use std::io::Write;
use std::time::{Duration, SystemTime};

// Mock rationale: Using tempfile crate to create a controlled, isolated, and deterministic
// temporary file system for tests. This avoids side effects on the actual file system
// and ensures tests are repeatable and offline.
// The `filetime` crate (added as a dev-dependency in Cargo.toml) is used to precisely set
// access/modification times, which is crucial for deterministic "dustiness" calculations in tests.

#[test]
fn test_sort_field_from_str() {
    assert_eq!("path".parse::<SortField>().unwrap(), SortField::Path);
    assert_eq!("SIZE".parse::<SortField>().unwrap(), SortField::Size);
    assert_eq!("dustiness".parse::<SortField>().unwrap(), SortField::Dustiness);
    assert!("invalid".parse::<SortField>().is_err());
}

#[test]
fn test_truncate_path() {
    let path1 = PathBuf::from("/a/b/c/d/e/f/g/h/i/j/k/l/m/n/o/p/q/r/s/t/u/v/w/x/y/z/file.txt");
    assert_eq!(truncate_path(&path1, 10), "...z/file.txt");
    let path2 = PathBuf::from("/short/file.txt");
    assert_eq!(truncate_path(&path2, 20), "/short/file.txt");
    let path3 = PathBuf::from("/a/b/c.txt");
    assert_eq!(truncate_path(&path3, 10), "/a/b/c.txt");
}

#[test]
fn test_dusty_file_detection() -> io::Result<()> {
    let dir = tempdir()?;
    let root_path = dir.path();

    let now = SystemTime::now();

    // Create a file that is 100 days old (dusty)
    let dusty_file_path = root_path.join("dusty_old_file.txt");
    File::create(&dusty_file_path)?.write_all(b"old content")?;
    let hundred_days_ago = now - Duration::from_secs(100 * 24 * 60 * 60);
    filetime::set_file_times(&dusty_file_path, hundred_days_ago.into(), hundred_days_ago.into())?;

    // Create a file that is 10 days old (not dusty by default min_dustiness=30)
    let fresh_file_path = root_path.join("fresh_file.txt");
    File::create(&fresh_file_path)?.write_all(b"fresh content")?;
    let ten_days_ago = now - Duration::from_secs(10 * 24 * 60 * 60);
    filetime::set_file_times(&fresh_file_path, ten_days_ago.into(), ten_days_ago.into())?;

    // Create a subdirectory and a dusty file inside it
    let sub_dir_path = root_path.join("subdir");
    fs::create_dir(&sub_dir_path)?;
    let sub_dusty_file_path = sub_dir_path.join("sub_dusty_file.txt");
    File::create(&sub_dusty_file_path)?.write_all(b"sub old content")?;
    filetime::set_file_times(&sub_dusty_file_path, hundred_days_ago.into(), hundred_days_ago.into())?;

    // Test with default min_dustiness (30 days)
    let args = Args {
        path: root_path.to_path_buf(),
        min_dustiness: 30,
        max_depth: None,
        sort_by: SortField::Dustiness,
        reverse: false,
    };

    let dusty_files = run(args, now)?;

    assert_eq!(dusty_files.len(), 2); // Should find dusty_old_file.txt and sub_dusty_file.txt

    // Check paths and dustiness (order might vary based on OS file system iteration, so check both)
    let expected_dusty_file = DustyFile {
        path: dusty_file_path.clone(),
        size: 11, // "old content".len()
        dustiness_days: 100,
    };
    let expected_sub_dusty_file = DustyFile {
        path: sub_dusty_file_path.clone(),
        size: 15, // "sub old content".len()
        dustiness_days: 100,
    };

    // Since sorting is by dustiness, and both are 100, their relative order might depend on path.
    // We'll check if both expected files are present.
    assert!(dusty_files.contains(&expected_dusty_file));
    assert!(dusty_files.contains(&expected_sub_dusty_file));

    // Test with a higher min_dustiness (e.g., 120 days) - should find nothing
    let args_high_min = Args {
        path: root_path.to_path_buf(),
        min_dustiness: 120,
        max_depth: None,
        sort_by: SortField::Dustiness,
        reverse: false,
    };
    let dusty_files_high_min = run(args_high_min, now)?;
    assert!(dusty_files_high_min.is_empty());

    // Test with max_depth = 0 (only root)
    let args_depth_0 = Args {
        path: root_path.to_path_buf(),
        min_dustiness: 30,
        max_depth: Some(0),
        sort_by: SortField::Dustiness,
        reverse: false,
    };
    let dusty_files_depth_0 = run(args_depth_0, now)?;
    assert_eq!(dusty_files_depth_0.len(), 1);
    assert_eq!(dusty_files_depth_0[0].path, dusty_file_path);
    assert_eq!(dusty_files_depth_0[0].dustiness_days, 100);

    // Test sorting by size, reverse
    let args_sort_size_rev = Args {
        path: root_path.to_path_buf(),
        min_dustiness: 30,
        max_depth: None,
        sort_by: SortField::Size,
        reverse: true,
    };
    let sorted_by_size_rev = run(args_sort_size_rev, now)?;
    assert_eq!(sorted_by_size_rev.len(), 2);
    assert_eq!(sorted_by_size_rev[0].path, sub_dusty_file_path); // Larger file first
    assert_eq!(sorted_by_size_rev[1].path, dusty_file_path);

    // Test sorting by path
    let args_sort_path = Args {
        path: root_path.to_path_buf(),
        min_dustiness: 30,
        max_depth: None,
        sort_by: SortField::Path,
        reverse: false,
    };
    let sorted_by_path = run(args_sort_path, now)?;
    assert_eq!(sorted_by_path.len(), 2);
    // Paths will be sorted lexicographically.
    // dusty_old_file.txt vs subdir/sub_dusty_file.txt
    assert_eq!(sorted_by_path[0].path, dusty_file_path);
    assert_eq!(sorted_by_path[1].path, sub_dusty_file_path);


    Ok(())
}
