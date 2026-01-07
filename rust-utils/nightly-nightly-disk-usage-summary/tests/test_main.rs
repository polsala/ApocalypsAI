use std::process::Command;
use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

fn unique_temp_dir() -> PathBuf {
    let base = std::env::temp_dir();
    let pid = std::process::id();
    let nanos = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
    base.join(format!("nightly_disk_integration_{}_{}", pid, nanos))
}

#[test]
fn integration_output_contains_expected_lines() {
    let dir = unique_temp_dir();
    fs::create_dir_all(&dir).unwrap();
    let sub1 = dir.join("small_folder");
    fs::create_dir(&sub1).unwrap();
    let file1 = sub1.join("a.txt");
    let mut f1 = File::create(&file1).unwrap();
    f1.write_all(&vec![0u8; 500]).unwrap();

    let sub2 = dir.join("large_folder");
    fs::create_dir(&sub2).unwrap();
    let file2 = sub2.join("b.bin");
    let mut f2 = File::create(&file2).unwrap();
    f2.write_all(&vec![0u8; 2_500_000]).unwrap();

    // Build the binary
    let status = Command::new("cargo").args(&["build", "--quiet"]).status().expect("cargo build failed");
    assert!(status.success());

    // Run the binary against the temp dir
    let output = Command::new("cargo").args(&["run", "--quiet", "--", dir.to_str().unwrap()]).output().expect("cargo run failed");
    let stdout = String::from_utf8_lossy(&output.stdout);

    assert!(stdout.contains("small_folder"));
    assert!(stdout.contains("500 B"));
    assert!(stdout.contains("This folder is a barren wasteland!"));
    assert!(stdout.contains("large_folder"));
    assert!(stdout.contains("2.50 MB"));
    assert!(stdout.contains("This folder is moderately populated."));

    // Clean up
    fs::remove_dir_all(&dir).unwrap();
}
