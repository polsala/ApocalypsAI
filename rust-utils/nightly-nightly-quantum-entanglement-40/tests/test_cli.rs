use std::process::Command;
use std::fs;
use std::path::Path;

#[test]
fn test_check_command_basic() {
    let output = Command::new("cargo")
        .args(&["run", "--release", "--", "check", "--qubits", "2", "--measurements", "100"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Entanglement Verification Report"));
    assert!(stdout.contains("Bell State Analysis:"));
}

#[test]
fn test_check_command_json_output() {
    let temp_file = "/tmp/test_quantum_output.json";
    
    // Clean up any existing file
    let _ = fs::remove_file(temp_file);
    
    let output = Command::new("cargo")
        .args(&[
            "run", "--release", "--", "check", 
            "--qubits", "2", 
            "--measurements", "50",
            "--output-format", "json",
            "--output-file", temp_file
        ])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    
    // Check that file was created
    assert!(Path::new(temp_file).exists());
    
    // Read and parse JSON
    let content = fs::read_to_string(temp_file).expect("Failed to read output file");
    let json: serde_json::Value = serde_json::from_str(&content).expect("Invalid JSON output");
    
    assert!(json["configuration"]["qubits"] == 2);
    assert!(json["configuration"]["measurements"] == 50);
    
    // Clean up
    let _ = fs::remove_file(temp_file);
}

#[test]
fn test_bell_test_command() {
    let output = Command::new("cargo")
        .args(&[
            "run", "--release", "--", "bell-test",
            "--angle-a", "0",
            "--angle-b", "45",
            "--angle-a-prime", "22.5",
            "--angle-b-prime", "67.5",
            "--trials", "100"
        ])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Bell Inequality Test Results"));
    assert!(stdout.contains("S-value:"));
    assert!(stdout.contains("Classical Limit:"));
}

#[test]
fn test_invalid_arguments() {
    // Test invalid number of qubits
    let output = Command::new("cargo")
        .args(&["run", "--release", "--", "check", "--qubits", "1"])
        .output()
        .expect("Failed to execute command");

    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Number of qubits must be at least 2"));

    // Test invalid basis
    let output = Command::new("cargo")
        .args(&["run", "--release", "--", "check", "--basis", "invalid"])
        .output()
        .expect("Failed to execute command");

    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Basis must be 'computational' or 'hadamard'"));
}

#[test]
fn test_yaml_output() {
    let temp_file = "/tmp/test_quantum_output.yaml";
    
    // Clean up any existing file
    let _ = fs::remove_file(temp_file);
    
    let output = Command::new("cargo")
        .args(&[
            "run", "--release", "--", "check", 
            "--qubits", "2", 
            "--measurements", "50",
            "--output-format", "yaml",
            "--output-file", temp_file
        ])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    
    // Check that file was created
    assert!(Path::new(temp_file).exists());
    
    // Read and parse YAML
    let content = fs::read_to_string(temp_file).expect("Failed to read output file");
    let yaml: serde_yaml::Value = serde_yaml::from_str(&content).expect("Invalid YAML output");
    
    assert!(yaml["configuration"]["qubits"] == 2);
    assert!(yaml["configuration"]["measurements"] == 50);
    
    // Clean up
    let _ = fs::remove_file(temp_file);
}

#[test]
fn test_help_command() {
    let output = Command::new("cargo")
        .args(&["run", "--release", "--", "--help"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("nightly-quantum-entanglement-checker"));
    assert!(stdout.contains("check"));
    assert!(stdout.contains("bell-test"));
}
