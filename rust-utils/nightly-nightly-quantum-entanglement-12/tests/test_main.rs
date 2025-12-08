use nightly_quantum_entanglement_checker::*;
use std::fs;
use std::io::Write;
use tempfile::NamedTempFile;

#[test]
fn test_quantum_energy_from_size() {
    assert_eq!(QuantumEnergy::from_size(100), QuantumEnergy::Low);
    assert_eq!(QuantumEnergy::from_size(5000), QuantumEnergy::Medium);
    assert_eq!(QuantumEnergy::from_size(2000000), QuantumEnergy::High);
}

#[test]
fn test_quantum_energy_to_string() {
    assert_eq!(QuantumEnergy::Low.to_string(), "Low");
    assert_eq!(QuantumEnergy::Medium.to_string(), "Medium");
    assert_eq!(QuantumEnergy::High.to_string(), "High");
}

#[test]
fn test_quantum_state_new() {
    let mut temp_file = NamedTempFile::new().unwrap();
    writeln!(temp_file, "Hello, quantum world!").unwrap();
    
    let state = QuantumState::new(temp_file.path()).unwrap();
    assert_eq!(state.size, 22); // "Hello, quantum world!\n" is 22 bytes
    assert_eq!(state.energy, QuantumEnergy::Low);
    assert_eq!(state.get_hash_prefix().len(), 12);
    
    // Verify hash is valid SHA-256 (64 hex chars)
    assert_eq!(state.hash.len(), 64);
}

#[test]
fn test_quantum_state_different_files() {
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    writeln!(temp_file1, "File content 1").unwrap();
    writeln!(temp_file2, "File content 2").unwrap();
    
    let state1 = QuantumState::new(temp_file1.path()).unwrap();
    let state2 = QuantumState::new(temp_file2.path()).unwrap();
    
    // Different content should have different hashes
    assert_ne!(state1.hash, state2.hash);
    assert_ne!(state1.get_hash_prefix(), state2.get_hash_prefix());
}

#[test]
fn test_quantum_state_same_files() {
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    let content = "Identical quantum content";
    writeln!(temp_file1, "{}").unwrap();
    writeln!(temp_file2, "{}").unwrap();
    
    let state1 = QuantumState::new(temp_file1.path()).unwrap();
    let state2 = QuantumState::new(temp_file2.path()).unwrap();
    
    // Same content should have identical hashes
    assert_eq!(state1.hash, state2.hash);
    assert_eq!(state1.get_hash_prefix(), state2.get_hash_prefix());
    assert_eq!(state1.size, state2.size);
}

#[test]
fn test_entanglement_result_identical() {
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    writeln!(temp_file1, "Identical content").unwrap();
    writeln!(temp_file2, "Identical content").unwrap();
    
    let state1 = QuantumState::new(temp_file1.path()).unwrap();
    let state2 = QuantumState::new(temp_file2.path()).unwrap();
    
    let result = EntanglementResult::new(&state1, &state2, 0.5);
    assert_eq!(result.probability, 100.0);
    assert!(result.entangled);
    assert_eq!(result.explanation, "Identical quantum states detected!");
}

#[test]
fn test_entanglement_result_different() {
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    writeln!(temp_file1, "Different content 1").unwrap();
    writeln!(temp_file2, "Different content 2").unwrap();
    
    let state1 = QuantumState::new(temp_file1.path()).unwrap();
    let state2 = QuantumState::new(temp_file2.path()).unwrap();
    
    let result = EntanglementResult::new(&state1, &state2, 0.5);
    assert!(result.probability >= 0.0 && result.probability <= 100.0);
    assert_eq!(result.explanation, "Different quantum states, but quantum uncertainty allows for entanglement!");
}

#[test]
fn test_entanglement_result_threshold_high() {
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    writeln!(temp_file1, "Content A").unwrap();
    writeln!(temp_file2, "Content B").unwrap();
    
    let state1 = QuantumState::new(temp_file1.path()).unwrap();
    let state2 = QuantumState::new(temp_file2.path()).unwrap();
    
    // With threshold 1.0, should never be entangled for different content
    let result = EntanglementResult::new(&state1, &state2, 1.0);
    assert!(!result.entangled);
}

#[test]
fn test_entanglement_result_threshold_low() {
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    writeln!(temp_file1, "Content A").unwrap();
    writeln!(temp_file2, "Content B").unwrap();
    
    let state1 = QuantumState::new(temp_file1.path()).unwrap();
    let state2 = QuantumState::new(temp_file2.path()).unwrap();
    
    // With threshold 0.0, should always be entangled
    let result = EntanglementResult::new(&state1, &state2, 0.0);
    assert!(result.entangled);
}

#[test]
fn test_quantum_state_empty_file() {
    let temp_file = NamedTempFile::new().unwrap();
    
    let state = QuantumState::new(temp_file.path()).unwrap();
    assert_eq!(state.size, 0);
    assert_eq!(state.energy, QuantumEnergy::Low);
}

#[test]
fn test_quantum_state_large_file() {
    let mut temp_file = NamedTempFile::new().unwrap();
    
    // Write 2MB of data
    let large_content = "x".repeat(2 * 1024 * 1024);
    writeln!(temp_file, "{}").unwrap();
    
    let state = QuantumState::new(temp_file.path()).unwrap();
    assert_eq!(state.size, large_content.len() as u64 + 1); // +1 for newline
    assert_eq!(state.energy, QuantumEnergy::High);
}

#[test]
fn test_quantum_state_error_nonexistent_file() {
    let result = QuantumState::new(Path::new("nonexistent_file.txt"));
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Failed to read file"));
}

#[test]
fn test_entanglement_result_probability_range() {
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    writeln!(temp_file1, "Content 1").unwrap();
    writeln!(temp_file2, "Content 2").unwrap();
    
    let state1 = QuantumState::new(temp_file1.path()).unwrap();
    let state2 = QuantumState::new(temp_file2.path()).unwrap();
    
    // Test multiple times to ensure probability is random
    let mut probabilities = Vec::new();
    for _ in 0..10 {
        let result = EntanglementResult::new(&state1, &state2, 0.5);
        assert!(result.probability >= 0.0 && result.probability <= 100.0);
        probabilities.push(result.probability);
    }
    
    // Check that we got different probabilities (quantum uncertainty)
    let unique_probabilities: std::collections::HashSet<_> = probabilities.iter().cloned().collect();
    assert!(unique_probabilities.len() > 1, "Expected some variation in probabilities due to quantum uncertainty");
}

#[test]
fn test_entanglement_result_deterministic_for_same_content() {
    // This test verifies that identical content always produces the same result
    let mut temp_file1 = NamedTempFile::new().unwrap();
    let mut temp_file2 = NamedTempFile::new().unwrap();
    
    writeln!(temp_file1, "Deterministic content").unwrap();
    writeln!(temp_file2, "Deterministic content").unwrap();
    
    let state1 = QuantumState::new(temp_file1.path()).unwrap();
    let state2 = QuantumState::new(temp_file2.path()).unwrap();
    
    // Multiple calls should always return the same result for identical content
    for _ in 0..10 {
        let result = EntanglementResult::new(&state1, &state2, 0.5);
        assert_eq!(result.probability, 100.0);
        assert!(result.entangled);
        assert_eq!(result.explanation, "Identical quantum states detected!");
    }
}
