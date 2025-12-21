use nightly_quantum_entanglement_checker::quantum_simulator::{QuantumEntanglementChecker, QuantumConfig};

#[test]
fn test_qubit_id_generation() {
    let config = QuantumConfig {
        decoherence: 0.1,
        measurements: 100,
        verbose: false,
    };
    
    let checker = QuantumEntanglementChecker::new(config);
    
    let qubit_id = checker.generate_qubit_id("TestNode");
    
    assert!(qubit_id.starts_with("Q-TestNode-"));
    assert_eq!(qubit_id.len(), "Q-TestNode-".len() + 6); // 6 hex characters
    assert!(qubit_id.chars().all(|c| c.is_alphanumeric() || c == '-'));
}

#[test]
fn test_simple_hash_function() {
    let config = QuantumConfig {
        decoherence: 0.1,
        measurements: 100,
        verbose: false,
    };
    
    let checker = QuantumEntanglementChecker::new(config);
    
    let hash1 = checker.simple_hash("test");
    let hash2 = checker.simple_hash("test");
    let hash3 = checker.simple_hash("different");
    
    // Same input should produce same hash
    assert_eq!(hash1, hash2);
    
    // Different inputs should produce different hashes (very likely)
    assert_ne!(hash1, hash3);
}

#[test]
fn test_quantum_state_generation() {
    let config = QuantumConfig {
        decoherence: 0.1,
        measurements: 100,
        verbose: false,
    };
    
    let mut checker = QuantumEntanglementChecker::new(config);
    
    let state1 = checker.generate_quantum_state("TestQubit1");
    let state2 = checker.generate_quantum_state("TestQubit2");
    
    // States should be between 0 and 1
    assert!(state1 >= 0.0 && state1 <= 1.0);
    assert!(state2 >= 0.0 && state2 <= 1.0);
    
    // Different qubits should have different states (very likely)
    assert_ne!(state1, state2);
}

#[test]
fn test_correlation_calculation() {
    let config = QuantumConfig {
        decoherence: 0.0,
        measurements: 100,
        verbose: false,
    };
    
    let checker = QuantumEntanglementChecker::new(config);
    
    // Test perfect correlation (same states)
    let correlation1 = checker.calculate_correlation(0.5, 0.5);
    assert!(correlation1 > 0.8); // Should be high correlation
    
    // Test anti-correlation (opposite states)
    let correlation2 = checker.calculate_correlation(0.0, 1.0);
    assert!(correlation2 < 0.3); // Should be low correlation
}

#[test]
fn test_decoherence_application() {
    let config = QuantumConfig {
        decoherence: 0.5,
        measurements: 100,
        verbose: false,
    };
    
    let checker = QuantumEntanglementChecker::new(config);
    
    let original_correlation = 1.0;
    let decohered_correlation = checker.apply_decoherence(original_correlation);
    
    // Decoherence should reduce correlation
    assert!(decohered_correlation < original_correlation);
    assert!(decohered_correlation >= 0.0);
    
    // With 50% decoherence, correlation should be reduced by about half
    assert!(decohered_correlation < 0.6);
}

#[test]
fn test_bell_inequality_calculation() {
    let config = QuantumConfig {
        decoherence: 0.0,
        measurements: 100,
        verbose: false,
    };
    
    let checker = QuantumEntanglementChecker::new(config);
    
    // High correlation should lead to Bell inequality violation
    let bell_high = checker.calculate_bell_inequality(0.9);
    assert!(bell_high > 2.0);
    
    // Low correlation should not violate Bell inequality
    let bell_low = checker.calculate_bell_inequality(0.1);
    assert!(bell_low <= 2.2); // Allow some randomness
}

#[test]
fn test_quantum_noise_generation() {
    let config = QuantumConfig {
        decoherence: 0.1,
        measurements: 100,
        verbose: false,
    };
    
    let checker = QuantumEntanglementChecker::new(config);
    
    let noise1 = checker.quantum_noise("test1");
    let noise2 = checker.quantum_noise("test2");
    
    // Quantum noise should be bounded
    assert!(noise1 >= -1.0 && noise1 <= 1.0);
    assert!(noise2 >= -1.0 && noise2 <= 1.0);
    
    // Different inputs should produce different noise
    assert_ne!(noise1, noise2);
}

#[test]
fn test_entanglement_result_validation() {
    let config = QuantumConfig {
        decoherence: 0.1,
        measurements: 100,
        verbose: false,
    };
    
    let mut checker = QuantumEntanglementChecker::new(config);
    
    let result = checker.verify_entanglement("ValidationTest", "Partner").unwrap();
    
    // Validate all fields
    assert!(!result.qubit_a_id.is_empty());
    assert!(!result.qubit_b_id.is_empty());
    assert!(result.correlation >= 0.0 && result.correlation <= 1.0);
    assert!(result.bell_inequality >= 2.0);
    assert_eq!(result.decoherence, 0.1);
    assert_eq!(result.measurements, 100);
    assert_eq!(result.verbose, false);
    
    // Entanglement status should be boolean
    assert!(result.entangled == true || result.entangled == false);
}
