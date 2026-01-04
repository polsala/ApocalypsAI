use std::process::Command;
use std::fs;

#[test]
fn test_cli_basic_functionality() {
    // Test basic entanglement check
    let output = Command::new("cargo")
        .args(&["run", "--bin", "quantum-entanglement-checker", "--", "--nodes", "node1,node2,node3"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("timestamp"));
    assert!(stdout.contains("nodes"));
    assert!(stdout.contains("entanglement_level"));
}

#[test]
fn test_cli_with_certificate() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "quantum-entanglement-checker", "--", "--nodes", "node1,node2", "--certificate"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("QUANTUM ENTANGLEMENT CERTIFICATE"));
    assert!(stdout.contains("✓"));
}

#[test]
fn test_cli_with_threshold() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "quantum-entanglement-checker", "--", "--nodes", "node1,node2", "--threshold", "0.9"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("timestamp"));
}

#[test]
fn test_cli_help() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "quantum-entanglement-checker", "--", "--help"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Entanglement Checker"));
    assert!(stdout.contains("--nodes"));
    assert!(stdout.contains("--threshold"));
}

#[test]
fn test_config_file_parsing() {
    let config_content = r#"
[network]
threshold = 0.9
monitor_interval = 30

[nodes]
participating = ["config1", "config2"]
"#;
    
    fs::write("test_quantum.toml", config_content).expect("Failed to write test config");
    
    let output = Command::new("cargo")
        .args(&["run", "--bin", "quantum-entanglement-checker", "--", "--config", "test_quantum.toml"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    
    fs::remove_file("test_quantum.toml").expect("Failed to clean up test config");
}

#[test]
fn test_invalid_threshold() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "quantum-entanglement-checker", "--", "--nodes", "node1", "--threshold", "invalid"])
        .output()
        .expect("Failed to execute command");
    
    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Threshold must be a valid number"));
}

#[test]
fn test_invalid_interval() {
    let output = Command::new("cargo")
        .args(&["run", "--bin", "quantum-entanglement-checker", "--", "--nodes", "node1", "--monitor", "--interval", "invalid"])
        .output()
        .expect("Failed to execute command");
    
    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Interval must be a valid number"));
}
