use std::process::Command;

#[test]
fn test_check_command() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .arg("check")
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Entanglement Verification"));
}

#[test]
fn test_report_command() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["report", "--samples", "100"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Entanglement Analysis Report"));
    assert!(stdout.contains("Sample Size: 100"));
}

#[test]
fn test_distributed_command() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["distributed", "--nodes", "3", "--rounds", "50"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Distributed Quantum Entanglement Test"));
    assert!(stdout.contains("Nodes: 3"));
}

#[test]
fn test_help_command() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .arg("--help")
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Simulates quantum entanglement verification"));
    assert!(stdout.contains("check"));
    assert!(stdout.contains("report"));
    assert!(stdout.contains("distributed"));
}

#[test]
fn test_invalid_arguments() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(["invalid-command"])
        .output()
        .expect("Failed to execute command");
    
    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("error:"));
}

#[test]
fn test_version_command() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .arg("--version")
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("nightly-quantum-entanglement-checker 1.0.0"));
}
