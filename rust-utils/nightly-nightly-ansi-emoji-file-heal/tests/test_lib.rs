use std::fs::{self, File};
use std::io::Write;
use std::path::Path;

use crate::analyze_path;

#[test]
fn test_analyze_path() {
    let base = std::env::temp_dir().join("nightly-ansi-emoji-file-health-test");
    let _ = fs::remove_dir_all(&base);
    fs::create_dir_all(&base).unwrap();

    let file1_path = base.join("small.txt");
    let mut file1 = File::create(&file1_path).unwrap();
    writeln!(file1, "Hello").unwrap();
    writeln!(file1, "World").unwrap();

    let file2_path = base.join("large.txt");
    let mut file2 = File::create(&file2_path).unwrap();
    for _ in 0..2000 {
        writeln!(file2, "Line").unwrap();
    }

    let results = analyze_path(&base).unwrap();
    assert_eq!(results.len(), 2);
    let small = results.iter().find(|f| f.path.ends_with("small.txt")).unwrap();
    assert!(small.healthy);
    let large = results.iter().find(|f| f.path.ends_with("large.txt")).unwrap();
    assert!(!large.healthy);
}
