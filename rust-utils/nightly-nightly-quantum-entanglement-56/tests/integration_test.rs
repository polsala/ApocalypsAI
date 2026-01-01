use std::process::Command;
use std::fs;
use tempfile::NamedTempFile;

#[test]
fn test_entanglement_check() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["--node-a", "service-a", "--node-b", "service-b"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Entanglement Verification Report"));
    assert!(stdout.contains("Node A: service-a"));
    assert!(stdout.contains("Node B: service-b"));
}

#[test]
fn test_json_output() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["--node-a", "service-a", "--node-b", "service-b", "--format", "json"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("{\"node_a\""));
    assert!(stdout.contains("\"node_b\""));
}

#[test]
fn test_cluster_file() {
    let mut cluster_file = NamedTempFile::new().expect("Failed to create temp file");
    writeln!(cluster_file, "service-a").expect("Failed to write to temp file");
    writeln!(cluster_file, "service-b").expect("Failed to write to temp file");
    writeln!(cluster_file, "service-c").expect("Failed to write to temp file");
    
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["--cluster", cluster_file.path().to_str().unwrap()])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Cluster Entanglement Report"));
    assert!(stdout.contains("service-a ↔ service-b"));
    assert!(stdout.contains("service-a ↔ service-c"));
    assert!(stdout.contains("service-b ↔ service-c"));
}

#[test]
fn test_invalid_threshold() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["--node-a", "service-a", "--node-b", "service-b", "--threshold", "1.5"])
        .output()
        .expect("Failed to execute command");
    
    // Should not crash, but may produce different results due to high threshold
    assert!(output.status.success());
}

#[test]
fn test_help() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["--help"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Simulates quantum entanglement verification"));
    assert!(stdout.contains("--node-a"));
    assert!(stdout.contains("--node-b"));
}
