use std::process::Command;
use std::fs;
use tempfile::NamedTempFile;
use std::io::Write;

#[test]
fn test_cli_basic_entanglement() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-entanglement-checker"))
        .args(["--nodes", "node1,node2", "--strength", "0.9"])
        .output()
        .expect("Failed to execute CLI");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("ENTANGLEMENT CONFIRMED"));
    assert!(stdout.contains("Bell State Fidelity:"));
}

#[test]
fn test_cli_weak_entanglement() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-entanglement-checker"))
        .args(["--nodes", "node1,node2", "--strength", "0.3"])
        .output()
        .expect("Failed to execute CLI");
    
    assert!(!output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("ENTANGLEMENT FAILED"));
}

#[test]
fn test_cli_distributed_mode() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-entanglement-checker"))
        .args(["--nodes", "node1,node2", "--distributed", "--latency", "50ms"])
        .output()
        .expect("Failed to execute CLI");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("ENTANGLEMENT CONFIRMED"));
}

#[test]
fn test_cli_config_file() {
    let mut temp_file = NamedTempFile::new().unwrap();
    writeln!(temp_file, r#"
[nodes]
primary = "node1"
secondary = "node2"

[quantum]
entanglement_strength = 0.85
coherence_threshold = 0.9
latency_simulation = "100ms"
"#).unwrap();
    
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-entanglement-checker"))
        .args(["--config", temp_file.path().to_str().unwrap()])
        .output()
        .expect("Failed to execute CLI");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("ENTANGLEMENT CONFIRMED"));
}

#[test]
fn test_cli_verbose_mode() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-entanglement-checker"))
        .args(["--nodes", "node1,node2", "--verbose"])
        .output()
        .expect("Failed to execute CLI");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Initializing Quantum Entanglement Checker"));
    assert!(stdout.contains("Nodes:"));
    assert!(stdout.contains("Entanglement Strength:"));
}

#[test]
fn test_cli_detailed_report() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-entanglement-checker"))
        .args(["--nodes", "node1,node2", "--report", "detailed"])
        .output()
        .expect("Failed to execute CLI");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("ENTANGLEMENT CONFIRMED"));
    assert!(stdout.contains("Additional Analysis:"));
    assert!(stdout.contains("Entanglement Threshold:"));
}

#[test]
fn test_cli_help() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-entanglement-checker"))
        .args(["--help"])
        .output()
        .expect("Failed to execute CLI");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Entanglement Checker"));
    assert!(stdout.contains("--nodes"));
    assert!(stdout.contains("--strength"));
}

#[test]
fn test_cli_version() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-entanglement-checker"))
        .args(["--version"])
        .output()
        .expect("Failed to execute CLI");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains(env!("CARGO_PKG_VERSION")));
}
