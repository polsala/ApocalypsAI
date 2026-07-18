use super::*;
use tempfile::{tempdir, NamedTempFile};
use std::io::Write;
use std::fs;

// Mock rationale: We need to test the file system traversal and aggregation logic
// without relying on the actual host file system, which would make tests non-deterministic
// and dependent on the test environment. Creating temporary files and directories
// provides a controlled, isolated, and deterministic environment for testing.

#[test]
fn test_parse_size_string() {
    assert_eq!(parse_size_string("100B").unwrap(), 100);
    assert_eq!(parse_size_string("1KB").unwrap(), 1024);
    assert_eq!(parse_size_string("1MB").unwrap(), 1024 * 1024);
    assert_eq!(parse_size_string("1.5GB").unwrap(), (1.5 * 1024.0 * 1024.0 * 1024.0) as u64);
    assert_eq!(parse_size_string("2TB").unwrap(), 2 * 1024 * 1024 * 1024 * 1024);
    assert!(parse_size_string("abc").is_err());
    assert!(parse_size_string("100ZZ").is_err());
}

#[test]
fn test_run_audit_basic() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create some dummy files
    fs::write(path.join("file1.txt"), "hello world")?; // 11 bytes
    fs::write(path.join("image.jpg"), vec![0; 1024 * 50])?; // 50KB
    fs::write(path.join("doc.pdf"), vec![0; 1024 * 100])?; // 100KB
    fs::create_dir(path.join("subdir"))?;
    fs::write(path.join("subdir/another.txt"), "more text")?; // 9 bytes
    fs::write(path.join("subdir/data.bin"), vec![0; 1024 * 200])?; // 200KB

    let args = Args {
        path: path.to_path_buf(),
        top_n: 5,
        min_size: None,
        extensions: None,
        verbose: false,
    };

    let result = run_audit(&args)?;

    assert_eq!(result.file_count, 5);
    assert_eq!(result.total_size, 11 + 50 * 1024 + 100 * 1024 + 9 + 200 * 1024);

    assert_eq!(result.extension_summary.get("txt").unwrap().1, 2);
    assert_eq!(result.extension_summary.get("jpg").unwrap().1, 1);
    assert_eq!(result.extension_summary.get("pdf").unwrap().1, 1);
    assert_eq!(result.extension_summary.get("bin").unwrap().1, 1);

    assert_eq!(result.extension_summary.get("txt").unwrap().0, 11 + 9);
    assert_eq!(result.extension_summary.get("jpg").unwrap().0, 50 * 1024);
    assert_eq!(result.extension_summary.get("pdf").unwrap().0, 100 * 1024);
    assert_eq!(result.extension_summary.get("bin").unwrap().0, 200 * 1024);

    assert!(result.largest_files.is_empty()); // verbose is false
    assert_eq!(result.largest_dirs.len(), 2); // root and subdir
    assert!(result.largest_dirs.iter().any(|(p, _)| p == path));
    assert!(result.largest_dirs.iter().any(|(p, _)| p == path.join("subdir")));

    Ok(())
}

#[test]
fn test_run_audit_with_filters() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    fs::write(path.join("small.txt"), "a")?; // 1 byte
    fs::write(path.join("medium.log"), vec![0; 1024 * 10])?; // 10KB
    fs::write(path.join("large.txt"), vec![0; 1024 * 50])?; // 50KB
    fs::write(path.join("huge.bin"), vec![0; 1024 * 100])?; // 100KB

    // Test with min_size and specific extensions
    let args = Args {
        path: path.to_path_buf(),
        top_n: 5,
        min_size: Some(parse_size_string("5KB")?),
        extensions: Some(vec!["txt".to_string(), "log".to_string()]),
        verbose: true,
    };

    let result = run_audit(&args)?;

    assert_eq!(result.file_count, 2); // large.txt, medium.log
    assert_eq!(result.total_size, 10 * 1024 + 50 * 1024);

    assert_eq!(result.extension_summary.get("txt").unwrap().1, 1);
    assert_eq!(result.extension_summary.get("log").unwrap().1, 1);
    assert_eq!(result.extension_summary.get("bin"), None); // Excluded by extension filter

    assert_eq!(result.largest_files.len(), 2);
    assert_eq!(result.largest_files[0].1, 50 * 1024); // large.txt
    assert_eq!(result.largest_files[1].1, 10 * 1024); // medium.log

    Ok(())
}

#[test]
fn test_run_audit_empty_dir() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let args = Args {
        path: path.to_path_buf(),
        top_n: 5,
        min_size: None,
        extensions: None,
        verbose: false,
    };

    let result = run_audit(&args)?;

    assert_eq!(result.file_count, 0);
    assert_eq!(result.total_size, 0);
    assert!(result.extension_summary.is_empty());
    assert!(result.largest_files.is_empty());
    assert_eq!(result.largest_dirs.len(), 1); // The root empty dir itself
    assert!(result.largest_dirs.iter().any(|(p, _)| p == path));

    Ok(())
}
