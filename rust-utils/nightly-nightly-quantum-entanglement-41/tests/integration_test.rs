use nightly_quantum_entanglement_checker::{QuantumEntanglementChecker, QuantumConfig, QuantumError};

#[test]
fn test_basic_entanglement_verification() {
    let config = QuantumConfig {
        decoherence: 0.1,
        measurements: 100,
        verbose: false,
    };
    
    let mut checker = QuantumEntanglementChecker::new(config);
    
    let result = checker.verify_entanglement("Alpha", "Beta").unwrap();
    
    // Basic validation
    assert_eq!(result.qubit_a_id.starts_with("Q-Alpha-"), true);
    assert_eq!(result.qubit_b_id.starts_with("Q-Beta-"), true);
    assert!(result.correlation >= 0.0 && result.correlation <= 1.0);
    assert!(result.bell_inequality >= 2.0);
    assert_eq!(result.decoherence, 0.1);
    assert_eq!(result.measurements, 100);
}

#[test]
fn test_decoherence_effects() {
    let config_low = QuantumConfig {
        decoherence: 0.0,
        measurements: 100,
        verbose: false,
    };
    
    let config_high = QuantumConfig {
        decoherence: 0.9,
        measurements: 100,
        verbose: false,
    };
    
    let mut checker_low = QuantumEntanglementChecker::new(config_low);
    let mut checker_high = QuantumEntanglementChecker::new(config_high);
    
    let result_low = checker_low.verify_entanglement("Node1", "Node2").unwrap();
    let result_high = checker_high.verify_entanglement("Node1", "Node2").unwrap();
    
    // Higher decoherence should generally result in lower correlation
    // Note: Due to quantum randomness, this is not always guaranteed, but should be true in most cases
    assert!(result_low.correlation >= result_high.correlation * 0.5);
}

#[test]
fn test_invalid_inputs() {
    let config = QuantumConfig {
        decoherence: 0.1,
        measurements: 100,
        verbose: false,
    };
    
    let mut checker = QuantumEntanglementChecker::new(config);
    
    // Test empty node names
    let result_empty = checker.verify_entanglement("", "Beta");
    assert!(result_empty.is_err());
    
    // Test very long node names
    let long_name = "A".repeat(51);
    let result_long = checker.verify_entanglement(&long_name, "Beta");
    assert!(result_long.is_err());
    
    if let Err(QuantumError::NodeNameTooLong) = result_long {
        // Expected error
    } else {
        panic!("Expected NodeNameTooLong error for long node name");
    }
}

#[test]
fn test_quantum_state_caching() {
    let config = QuantumConfig {
        decoherence: 0.1,
        measurements: 100,
        verbose: false,
    };
    
    let mut checker = QuantumEntanglementChecker::new(config);
    
    // First verification
    let result1 = checker.verify_entanglement("CacheTest", "CachePartner").unwrap();
    let qubit_id = &result1.qubit_a_id;
    
    // Check that state is cached
    let cached_state1 = checker.get_cached_state(qubit_id);
    assert!(cached_state1.is_some());
    
    // Clear cache
    checker.clear_cache();
    
    // Check that cache is cleared
    let cached_state2 = checker.get_cached_state(qubit_id);
    assert!(cached_state2.is_none());
}

#[test]
fn test_bell_inequality_violation() {
    let config = QuantumConfig {
        decoherence: 0.05, // Low decoherence for better entanglement
        measurements: 1000,
        verbose: false,
    };
    
    let mut checker = QuantumEntanglementChecker::new(config);
    
    // Run multiple tests to ensure we get quantum entanglement
    let mut entangled_count = 0;
    let total_tests = 10;
    
    for _ in 0..total_tests {
        let result = checker.verify_entanglement("BellTest", "Partner").unwrap();
        if result.entangled {
            entangled_count += 1;
        }
    }
    
    // We should get entanglement in most cases with low decoherence
    assert!(entangled_count >= total_tests / 2, 
           "Expected at least half of tests to show entanglement, got {}/{}", 
           entangled_count, total_tests);
}

#[test]
fn test_quantum_config_validation() {
    // Test valid config
    let valid_config = QuantumConfig {
        decoherence: 0.5,
        measurements: 100,
        verbose: false,
    };
    
    let checker = QuantumEntanglementChecker::new(valid_config);
    assert_eq!(checker.config.decoherence, 0.5);
    assert_eq!(checker.config.measurements, 100);
    
    // Test invalid decoherence (this will panic as intended)
    let invalid_config = QuantumConfig {
        decoherence: 1.5, // Invalid
        measurements: 100,
        verbose: false,
    };
    
    let result = std::panic::catch_unwind(|| {
        QuantumEntanglementChecker::new(invalid_config)
    });
    
    assert!(result.is_err(), "Expected panic for invalid decoherence");
    
    // Test invalid measurements
    let invalid_config2 = QuantumConfig {
        decoherence: 0.1,
        measurements: 0, // Invalid
        verbose: false,
    };
    
    let result2 = std::panic::catch_unwind(|| {
        QuantumEntanglementChecker::new(invalid_config2)
    });
    
    assert!(result2.is_err(), "Expected panic for zero measurements");
}
