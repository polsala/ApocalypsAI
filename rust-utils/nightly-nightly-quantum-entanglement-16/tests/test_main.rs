use std::process::Command;
use std::fs;
use std::io::Write;

#[test]
fn test_version() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "--version"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Nightly Quantum Entanglement Checker v"));
}

#[test]
fn test_help() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "--help"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Usage:"));
    assert!(stdout.contains("--signature"));
    assert!(stdout.contains("--text"));
}

#[test]
fn test_identical_files_entangled() {
    // Create two identical temporary files
    let temp_dir = std::env::temp_dir();
    let file1_path = temp_dir.join("test_file1.rs");
    let file2_path = temp_dir.join("test_file2.rs");
    
    let test_content = "fn main() { println!(\"Hello World!\"); }";
    
    let mut file1 = fs::File::create(&file1_path).expect("Failed to create test file 1");
    let mut file2 = fs::File::create(&file2_path).expect("Failed to create test file 2");
    
    write!(file1, "{}").expect("Failed to write to test file 1");
    write!(file2, "{}").expect("Failed to write to test file 2");
    
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", &file1_path.to_string_lossy().to_string(), &file2_path.to_string_lossy().to_string()])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    // Clean up
    fs::remove_file(&file1_path).ok();
    fs::remove_file(&file2_path).ok();
    
    assert!(stdout.contains("Quantum Entanglement Detected"));
    assert!(stdout.contains("✨"));
    assert!(stdout.contains("🌌"));
}

#[test]
fn test_different_files_not_entangled() {
    // Create two different temporary files
    let temp_dir = std::env::temp_dir();
    let file1_path = temp_dir.join("test_file1.rs");
    let file2_path = temp_dir.join("test_file2.rs");
    
    let test_content1 = "fn main() { println!(\"Hello World!\"); }";
    let test_content2 = "fn main() { println!(\"Goodbye World!\"); }";
    
    let mut file1 = fs::File::create(&file1_path).expect("Failed to create test file 1");
    let mut file2 = fs::File::create(&file2_path).expect("Failed to create test file 2");
    
    write!(file1, "{}").expect("Failed to write to test file 1");
    write!(file2, "{}").expect("Failed to write to test file 2");
    
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", &file1_path.to_string_lossy().to_string(), &file2_path.to_string_lossy().to_string()])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    // Clean up
    fs::remove_file(&file1_path).ok();
    fs::remove_file(&file2_path).ok();
    
    assert!(stdout.contains("Quantum Entanglement Not Found"));
    assert!(stdout.contains("❌"));
    assert!(stdout.contains("🚀"));
}

#[test]
fn test_identical_text_entangled() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "--text", "Hello World", "Hello World"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    assert!(stdout.contains("Quantum Entanglement Detected"));
    assert!(stdout.contains("✨"));
}

#[test]
fn test_different_text_not_entangled() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "--text", "Hello", "Goodbye"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    assert!(stdout.contains("Quantum Entanglement Not Found"));
    assert!(stdout.contains("❌"));
}

#[test]
fn test_signature_generation_file() {
    // Create a temporary file
    let temp_dir = std::env::temp_dir();
    let file_path = temp_dir.join("test_signature.rs");
    
    let test_content = "fn main() { println!(\"Test\"); }";
    
    let mut file = fs::File::create(&file_path).expect("Failed to create test file");
    write!(file, "{}").expect("Failed to write to test file");
    
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "--signature", &file_path.to_string_lossy().to_string()])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    // Clean up
    fs::remove_file(&file_path).ok();
    
    assert!(stdout.contains("Quantum Signature for file:"));
    assert!(stdout.len() > 50); // Should contain a hash
}

#[test]
fn test_signature_generation_text() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "--signature", "--text", "Test String"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    
    assert!(stdout.contains("Quantum Signature for text:"));
    assert!(stdout.len() > 50); // Should contain a hash
}

#[test]
fn test_error_file_not_found() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "nonexistent_file.rs", "another_nonexistent_file.rs"])
        .output()
        .expect("Failed to execute command");
    
    let stderr = String::from_utf8_lossy(&output.stderr);
    
    assert!(stderr.contains("Error reading file"));
}

#[test]
fn test_error_insufficient_arguments() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--"])
        .output()
        .expect("Failed to execute command");
    
    let stderr = String::from_utf8_lossy(&output.stderr);
    
    assert!(stderr.contains("Please provide"));
}

// Mock rationale: These tests use temporary files and command execution to verify
// the CLI behavior without requiring external dependencies or network access.
// The tests are deterministic and run in isolated environments.
