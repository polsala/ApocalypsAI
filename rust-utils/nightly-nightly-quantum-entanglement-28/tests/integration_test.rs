use nightly_quantum_entanglement_checker::*;
use std::fs;
use std::process::Command;

#[test]
fn test_full_workflow() {
    // Clean up any existing test file
    let test_file = "integration_test_pairs.json";
    if fs::Path::new(test_file).exists() {
        fs::remove_file(test_file).ok();
    }

    // Test generate command
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "generate"])
        .output()
        .expect("Failed to execute generate command");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Entanglement Pair Generated!"));
    assert!(stdout.contains("Pair ID: QEP-"));
    assert!(stdout.contains("Particle A: |0⟩"));
    assert!(stdout.contains("Particle B: |1⟩"));
    assert!(stdout.contains("Entanglement Strength:"));
    assert!(stdout.contains("Quantum Coherence: Stable"));

    // Extract pair ID from output
    let pair_id = stdout.lines()
        .find(|line| line.contains("Pair ID:"))
        .unwrap()
        .split_whitespace()
        .nth(2)
        .unwrap()
        .to_string();

    // Test verify command
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "verify", &pair_id])
        .output()
        .expect("Failed to execute verify command");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains(&format!("✓ Quantum entanglement verified for pair: {}", pair_id)));

    // Test list command
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "list"])
        .output()
        .expect("Failed to execute list command");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Entanglement Pairs (1 found):"));
    assert!(stdout.contains(&pair_id));

    // Test visualize command
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "visualize", &pair_id])
        .output()
        .expect("Failed to execute visualize command");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Entanglement Visualization"));
    assert!(stdout.contains(&pair_id));
    assert!(stdout.contains("Spacetime Entanglement Status: ✓ CONNECTED"));

    // Clean up
    if fs::Path::new(test_file).exists() {
        fs::remove_file(test_file).ok();
    }
}

#[test]
fn test_invalid_commands() {
    // Test unknown command
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "invalid"])
        .output()
        .expect("Failed to execute invalid command");

    assert!(!output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Unknown command: invalid"));
    assert!(stdout.contains("Usage:"));

    // Test verify without ID
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "verify"])
        .output()
        .expect("Failed to execute verify without ID");

    assert!(!output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Please provide a pair ID to verify"));

    // Test visualize without ID
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "visualize"])
        .output()
        .expect("Failed to execute visualize without ID");

    assert!(!output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Please provide a pair ID to visualize"));
}

#[test]
fn test_nonexistent_pair() {
    let nonexistent_id = "QEP-00000000-0000-0000-0000-000000000000";

    // Test verify nonexistent pair
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "verify", nonexistent_id])
        .output()
        .expect("Failed to execute verify nonexistent pair");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains(&format!("No quantum entanglement pair found with ID: {}", nonexistent_id)));

    // Test visualize nonexistent pair
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "visualize", nonexistent_id])
        .output()
        .expect("Failed to execute visualize nonexistent pair");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains(&format!("No quantum entanglement pair found with ID: {}", nonexistent_id)));
}

#[test]
fn test_multiple_pairs() {
    // Clean up any existing test file
    let test_file = "multiple_pairs_test.json";
    if fs::Path::new(test_file).exists() {
        fs::remove_file(test_file).ok();
    }

    // Generate multiple pairs
    for i in 0..3 {
        let output = Command::new(env!("CARGO"))
            .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "generate"])
            .output()
            .expect(&format!("Failed to execute generate command #{}", i));
        assert!(output.status.success());
    }

    // Test list shows all pairs
    let output = Command::new(env!("CARGO"))
        .args(&["run", "--bin", "nightly-quantum-entanglement-checker", "--", "list"])
        .output()
        .expect("Failed to execute list command for multiple pairs");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Quantum Entanglement Pairs (3 found):"));
    assert!(stdout.matches("QEP-").count() >= 3);

    // Clean up
    if fs::Path::new(test_file).exists() {
        fs::remove_file(test_file).ok();
    }
}
