use nightly_quantum_entanglement_checker::quantum_metrics::*;

#[test]
fn test_fidelity_ideal_case() {
    // Perfect Bell state distribution
    let fidelity = calculate_fidelity(250, 250, 250, 250, 1000);
    assert!((fidelity - 1.0).abs() < 1e-10);
}

#[test]
fn test_fidelity_biased_case() {
    // Completely biased towards one state
    let fidelity = calculate_fidelity(1000, 0, 0, 0, 1000);
    assert!(fidelity < 0.6);
    assert!(fidelity > 0.4); // Should still have some overlap
}

#[test]
fn test_fidelity_extreme_case() {
    // Only one type of measurement
    let fidelity = calculate_fidelity(500, 500, 0, 0, 1000);
    // Should be lower than ideal but higher than completely biased
    assert!(fidelity > 0.5);
    assert!(fidelity < 1.0);
}

#[test]
fn test_concurrence_ideal_case() {
    // For a perfect Bell state, concurrence should be high
    let concurrence = calculate_concurrence(250, 250, 250, 250, 1000);
    // Note: This is a simplified calculation
    assert!(concurrence >= 0.0);
    assert!(concurrence <= 1.0);
}

#[test]
fn test_concurrence_separable_case() {
    // For a separable state (only one outcome), concurrence should be 0
    let concurrence = calculate_concurrence(1000, 0, 0, 0, 1000);
    assert_eq!(concurrence, 0.0);
}

#[test]
fn test_entropy_maximal() {
    // Equal probabilities should give maximum entropy (normalized to 1.0)
    let entropy = calculate_entropy(250, 250, 250, 250, 1000);
    assert!((entropy - 1.0).abs() < 1e-10);
}

#[test]
fn test_entropy_minimal() {
    // Completely biased distribution should give low entropy
    let entropy = calculate_entropy(1000, 0, 0, 0, 1000);
    assert!(entropy < 0.1);
    assert!(entropy >= 0.0);
}

#[test]
fn test_entropy_partial() {
    // Partial bias should give intermediate entropy
    let entropy = calculate_entropy(500, 500, 0, 0, 1000);
    assert!(entropy > 0.4);
    assert!(entropy < 0.8);
}

#[test]
fn test_quantum_discord() {
    // Test quantum discord calculation
    let discord = calculate_quantum_discord(250, 250, 250, 250, 1000);
    assert!(discord >= 0.0);
    assert!(discord <= 1.0);

    let discord_biased = calculate_quantum_discord(1000, 0, 0, 0, 1000);
    assert!(discord_biased < discord); // Biased state should have less quantum correlation
}

#[test]
fn test_tangle() {
    // Test tangle calculation (should be concurrence squared)
    let concurrence = calculate_concurrence(250, 250, 250, 250, 1000);
    let tangle = calculate_tangle(250, 250, 250, 250, 1000);
    
    assert!((tangle - concurrence * concurrence).abs() < 1e-10);
}

#[test]
fn test_linear_entropy() {
    // Test linear entropy calculation
    let linear_entropy = calculate_linear_entropy(250, 250, 250, 250, 1000);
    assert!(linear_entropy >= 0.0);
    assert!(linear_entropy <= 1.0);

    // Should be lower for more uniform distributions
    let linear_entropy_biased = calculate_linear_entropy(1000, 0, 0, 0, 1000);
    assert!(linear_entropy_biased > linear_entropy);
}

#[test]
fn test_mutual_information() {
    // Test mutual information calculation
    let mutual_info = calculate_mutual_information(250, 250, 250, 250, 1000);
    assert!(mutual_info >= 0.0);
    assert!(mutual_info <= 2.0); // Maximum for 2-qubit system

    // Should be higher for more correlated states
    let mutual_info_biased = calculate_mutual_information(500, 0, 0, 500, 1000);
    assert!(mutual_info_biased > mutual_info);
}

#[test]
fn test_metrics_consistency() {
    // Test that all metrics are in valid ranges for various distributions
    let test_cases = vec![
        (250, 250, 250, 250, 1000), // Uniform
        (500, 500, 0, 0, 1000),     // Partial
        (1000, 0, 0, 0, 1000),     // Biased
        (300, 300, 200, 200, 1000), // Mixed
    ];

    for (phi_plus, phi_minus, psi_plus, psi_minus, total) in test_cases {
        let fidelity = calculate_fidelity(phi_plus, phi_minus, psi_plus, psi_minus, total);
        let concurrence = calculate_concurrence(phi_plus, phi_minus, psi_plus, psi_minus, total);
        let entropy = calculate_entropy(phi_plus, phi_minus, psi_plus, psi_minus, total);
        let linear_entropy = calculate_linear_entropy(phi_plus, phi_minus, psi_plus, psi_minus, total);

        assert!(fidelity >= 0.0 && fidelity <= 1.0, "Fidelity out of range: {}", fidelity);
        assert!(concurrence >= 0.0 && concurrence <= 1.0, "Concurrence out of range: {}", concurrence);
        assert!(entropy >= 0.0 && entropy <= 1.0, "Entropy out of range: {}", entropy);
        assert!(linear_entropy >= 0.0 && linear_entropy <= 1.0, "Linear entropy out of range: {}", linear_entropy);
    }
}

#[test]
fn test_edge_cases() {
    // Test edge cases
    
    // Zero measurements
    let fidelity = calculate_fidelity(0, 0, 0, 0, 0);
    assert!(fidelity.is_nan() || fidelity == 0.0);

    // Single measurement
    let fidelity = calculate_fidelity(1, 0, 0, 0, 1);
    assert!(fidelity >= 0.0 && fidelity <= 1.0);

    // Large numbers
    let fidelity = calculate_fidelity(250000, 250000, 250000, 250000, 1000000);
    assert!((fidelity - 1.0).abs() < 1e-10);
}
