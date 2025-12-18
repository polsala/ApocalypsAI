use std::process::Command;
use tempfile::NamedTempFile;
use std::io::Write;

#[test]
fn test_entangled_files() {
    // Create two identical temporary files
    let mut file1 = NamedTempFile::new().unwrap();
    let mut file2 = NamedTempFile::new().unwrap();
    
    let content = b"fn test() { assert_eq!(1 + 1, 2); }";
    file1.write_all(content).unwrap();
    file2.write_all(content).unwrap();
    
    // Run the CLI tool
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "quantum-entanglement-checker",
            file1.path().to_str().unwrap(),
            file2.path().to_str().unwrap(),
        ])
        .output()
        .expect("Failed to execute command");
    
    // Verify success exit code
    assert!(output.status.success());
    
    // Verify output contains entanglement message
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("QUANTUM ENTANGLEMENT DETECTED"));
    assert!(stdout.contains("perfectly synchronized"));
}

#[test]
fn test_decohered_files() {
    // Create two different temporary files
    let mut file1 = NamedTempFile::new().unwrap();
    let mut file2 = NamedTempFile::new().unwrap();
    
    file1.write_all(b"fn test() { assert_eq!(1 + 1, 2); }\").unwrap();
    file2.write_all(b"fn test() { assert_eq!(2 + 2, 4); }\").unwrap();
    
    // Run the CLI tool
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "quantum-entanglement-checker",
            file1.path().to_str().unwrap(),
            file2.path().to_str().unwrap(),
        ])
        .output()
        .expect("Failed to execute command");
    
    // Verify failure exit code
    assert!(!output.status.success());
    
    // Verify output contains decoherence message
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("QUANTUM DECOHERENCE OBSERVED"));
    assert!(stdout.contains("different quantum states"));
}

#[test]
fn test_nonexistent_file() {
    // Run the CLI tool with a non-existent file
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "quantum-entanglement-checker",
            "nonexistent_file.rs",
            "file2.rs",
        ])
        .output()
        .expect("Failed to execute command");
    
    // Verify failure exit code
    assert!(!output.status.success());
    
    // Verify error message
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("does not exist"));
}

#[test]
fn test_invalid_arguments() {
    // Run the CLI tool with no arguments
    let output = Command::new(env!("CARGO"))
        .args(&[
            "run",
            "--bin",
            "quantum-entanglement-checker",
        ])
        .output()
        .expect("Failed to execute command");
    
    // Verify failure exit code
    assert!(!output.status.success());
    
    // Verify usage message
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Usage:"));
}
