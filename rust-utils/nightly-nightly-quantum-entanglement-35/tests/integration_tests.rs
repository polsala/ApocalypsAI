use std::process::Command;

#[test]
fn test_check_bell_state() {
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--release", "--", "check", "--amplitudes", "0.7071", "0", "0", "0.7071"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Bell state"));
}

#[test]
fn test_check_separable_state() {
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--release", "--", "check", "--amplitudes", "0", "1", "0", "0"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("separable"));
}

#[test]
fn test_generate_entangled_state() {
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--release", "--", "generate", "--qubits", "3"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Generated 3-qubit entangled state:"));
    
    // Check that we have 8 amplitudes (2^3)
    let lines: Vec<&str> = stdout.lines().collect();
    assert!(lines.len() >= 9); // Header + 8 amplitudes
}

#[test]
fn test_entropy_calculation() {
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--release", "--", "entropy", "--amplitudes", "0.5", "0.5", "0.5", "0.5"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Entanglement entropy:"));
}

#[test]
fn test_invalid_state_validation() {
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--release", "--", "check", "--amplitudes", "1", "0", "0", "0"])
        .output()
        .expect("Failed to execute command");
    
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("not normalized"));
}

#[test]
fn test_help_command() {
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--release", "--", "--help"])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Detect quantum entanglement patterns"));
}
