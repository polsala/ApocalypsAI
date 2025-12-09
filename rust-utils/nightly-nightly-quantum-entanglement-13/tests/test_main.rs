use std::process::Command;

#[test]
fn test_bell_state_verification() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--state", "00 11", "--method", "bell"])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("ENTANGLED"));
    assert!(stdout.contains("Bell State Verification"));
}

#[test]
fn test_chsh_inequality_violation() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--chsh", "2.5"])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("VIOLATION DETECTED"));
    assert!(stdout.contains("CHSH Inequality Test"));
}

#[test]
fn test_chsh_inequality_no_violation() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--chsh", "1.5"])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("NO VIOLATION"));
}

#[test]
fn test_entanglement_entropy_maximal() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--entropy", "[0.707, 0.707]"])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("MAXIMALLY ENTANGLED"));
    assert!(stdout.contains("Entanglement Entropy"));
}

#[test]
fn test_entanglement_entropy_separable() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--entropy", "[1.0, 0.0]"])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("SEPARABLE"));
}

#[test]
fn test_help_output() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--help"])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Entanglement Checker"));
    assert!(stdout.contains("--state"));
    assert!(stdout.contains("--chsh"));
    assert!(stdout.contains("--entropy"));
}

#[test]
fn test_version_output() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--version"])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Entanglement Checker v"));
}

#[test]
fn test_invalid_chsh_value() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--chsh", "invalid"])
        .output()
        .expect("Failed to execute quantum-check");

    // Should fail with invalid input
    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Invalid CHSH value"));
}

#[test]
fn test_invalid_entropy_format() {
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--entropy", "[invalid]"])
        .output()
        .expect("Failed to execute quantum-check");

    // Should fail with invalid format
    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Invalid amplitude"));
}

#[test]
fn test_batch_mode() {
    // Create a temporary batch file for testing
    use std::fs;
    use std::path::Path;
    
    let batch_file = "test_batch.txt";
    let batch_content = "# Test batch file\nbell 00 11\nchsh 2.5\nentropy [0.707, 0.707]\n";
    
    fs::write(batch_file, batch_content).expect("Failed to create test batch file");
    
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--batch", batch_file])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Processing batch file"));
    assert!(stdout.contains("ENTANGLED"));
    assert!(stdout.contains("VIOLATION"));
    
    // Clean up
    fs::remove_file(batch_file).expect("Failed to remove test batch file");
}

#[test]
fn test_interactive_mode_exit() {
    // Test that interactive mode can be started and exited
    // This is a basic test to ensure the interactive mode doesn't crash
    let mut child = std::process::Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--interactive"])
        .spawn()
        .expect("Failed to start interactive mode");
    
    // Send 'quit' command to exit
    use std::io::Write;
    if let Some(stdin) = child.stdin.as_mut() {
        writeln!(stdin, "quit").expect("Failed to write to stdin");
    }
    
    let output = child.wait_with_output().expect("Failed to wait for child");
    assert!(output.status.success());
}

#[test]
fn test_bell_state_patterns() {
    let patterns = vec![
        "00 11", "00+11", "00|11",
        "01 10", "01+10", "01|10",
        "11 00", "11+00", "11|00",
        "10 01", "10+01", "10|01",
    ];
    
    for pattern in patterns {
        let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
            .args(["--state", pattern, "--method", "bell"])
            .output()
            .expect("Failed to execute quantum-check");

        assert!(output.status.success());
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("ENTANGLED"), "Pattern '{}' should be entangled", pattern);
    }
}

#[test]
fn test_chsh_bounds() {
    // Test exactly at classical bound (should not violate)
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--chsh", "2.0"])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("NO VIOLATION"));
    
    // Test at quantum bound (should violate maximally)
    let quantum_bound = 2.0 * std::f64::consts::SQRT_2;
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args([&format!("--chsh", quantum_bound)])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("VIOLATION DETECTED"));
}

#[test]
fn test_entropy_calculation() {
    // Test with different amplitude distributions
    
    // Equal amplitudes (maximal entanglement)
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--entropy", "[0.5, 0.5, 0.5, 0.5]"])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("ENTANGLED"));
    
    // One amplitude is 1, others are 0 (separable)
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--entropy", "[1.0, 0.0, 0.0, 0.0]"])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("SEPARABLE"));
}

#[test]
fn test_error_handling() {
    // Test missing arguments
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--state"])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("requires"));
    
    // Test unknown option
    let output = Command::new(env!("CARGO_BIN_EXE_quantum-check"))
        .args(["--unknown", "value"])
        .output()
        .expect("Failed to execute quantum-check");

    assert!(!output.status.success());
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Unknown option"));
}
