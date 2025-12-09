use std::process::Command;
use tempfile::NamedTempFile;
use std::io::Write;

#[test]
fn test_cli_identical_files() {
    let mut temp1 = NamedTempFile::new().unwrap();
    let mut temp2 = NamedTempFile::new().unwrap();
    
    let content = b"Identical content for quantum entanglement test";
    temp1.write_all(content).unwrap();
    temp2.write_all(content).unwrap();
    
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--release",
            "--",
            "--file1",
            temp1.path().to_str().unwrap(),
            "--file2",
            temp2.path().to_str().unwrap(),
            "--verbose",
        ])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("quantum-entangled"));
    assert!(stdout.contains("IDENTICAL"));
}

#[test]
fn test_cli_different_files() {
    let mut temp1 = NamedTempFile::new().unwrap();
    let mut temp2 = NamedTempFile::new().unwrap();
    
    temp1.write_all(b"File A content").unwrap();
    temp2.write_all(b"File B content").unwrap();
    
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--release",
            "--",
            "--file1",
            temp1.path().to_str().unwrap(),
            "--file2",
            temp2.path().to_str().unwrap(),
        ])
        .output()
        .expect("Failed to execute command");
    
    // Should exit with code 1 for not entangled
    assert!(!output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("not quantum-entangled"));
    assert!(stdout.contains("DIFFERENT"));
}

#[test]
fn test_cli_nonexistent_file() {
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--release",
            "--",
            "--file1",
            "nonexistent1.txt",
            "--file2",
            "nonexistent2.txt",
        ])
        .output()
        .expect("Failed to execute command");
    
    // Should exit with error
    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("File not found"));
}

#[test]
fn test_cli_threshold_parameter() {
    let mut temp1 = NamedTempFile::new().unwrap();
    let mut temp2 = NamedTempFile::new().unwrap();
    
    temp1.write_all(b"Content A").unwrap();
    temp2.write_all(b"Content B").unwrap();
    
    // Test with very low threshold - should be considered entangled
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--release",
            "--",
            "--file1",
            temp1.path().to_str().unwrap(),
            "--file2",
            temp2.path().to_str().unwrap(),
            "--threshold",
            "0.001",
        ])
        .output()
        .expect("Failed to execute command");
    
    // With very low threshold, even different files might be considered uncertain
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum State:"));
}

#[test]
fn test_cli_help() {
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--release",
            "--",
            "--help",
        ])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Usage:"));
    assert!(stdout.contains("--file1"));
    assert!(stdout.contains("--file2"));
}
