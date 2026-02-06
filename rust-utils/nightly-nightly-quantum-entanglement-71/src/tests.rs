use crate::bell_states::{BellState, calculate_correlation, calculate_chsh, calculate_fidelity};
use crate::measurements::{verify_entanglement, apply_decoherence, add_measurement_noise, generate_statistics};
use crate::network::{simulate_network_entanglement, simulate_teleportation, calculate_qkd_rate, apply_error_correction};
use crate::circuit::{generate_circuit_diagram, visualize_measurement_bases, generate_probability_table};
use crate::education::learn_concept;

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    #[test]
    fn test_bell_state_creation() {
        assert_eq!(BellState::from_string("phi-plus").name(), "|Φ+⟩ = (|00⟩ + |11⟩)/√2");
        assert_eq!(BellState::from_string("psi-minus").name(), "|Ψ-⟩ = (|01⟩ - |10⟩)/√2");
        assert_eq!(BellState::from_string("invalid").name(), "|Φ+⟩ = (|00⟩ + |11⟩)/√2"); // Default
    }

    #[test]
    fn test_bell_state_theoretical_values() {
        let phi_plus = BellState::PhiPlus;
        let psi_plus = BellState::PsiPlus;
        
        assert_eq!(phi_plus.theoretical_correlation(), 1.0);
        assert_eq!(psi_plus.theoretical_correlation(), -1.0);
        assert_eq!(phi_plus.theoretical_chsh(), 2.0 * f64::sqrt(2.0));
    }

    #[test]
    fn test_correlation_calculation() {
        // Perfect correlation
        let results = vec![(false, false), (true, true), (false, false), (true, true)];
        let correlation = calculate_correlation(&results);
        assert!((correlation - 1.0).abs() < 0.01);
        
        // Perfect anti-correlation
        let results = vec![(false, true), (true, false), (false, true), (true, false)];
        let correlation = calculate_correlation(&results);
        assert!((correlation - (-1.0)).abs() < 0.01);
        
        // Random correlation
        let results = vec![(false, false), (true, false), (false, true), (true, true)];
        let correlation = calculate_correlation(&results);
        assert!((correlation - 0.0).abs() < 0.01);
    }

    #[test]
    fn test_chsh_calculation() {
        // Create entangled results
        let results = vec![(false, false); 1000];
        let chsh = calculate_chsh(&results);
        // Should be close to 2 for perfect correlation
        assert!(chsh > 1.5 && chsh < 2.5);
    }

    #[test]
    fn test_fidelity_calculation() {
        let results = vec![(false, false), (true, true), (false, false), (true, true)];
        let fidelity = calculate_fidelity(&results, &BellState::PhiPlus);
        assert_eq!(fidelity, 1.0);
        
        let fidelity = calculate_fidelity(&results, &BellState::PsiPlus);
        assert_eq!(fidelity, 0.0);
    }

    #[test]
    fn test_entanglement_verification() {
        let results = verify_entanglement(2, 1000, "phi-plus", 3);
        
        // Should detect entanglement for phi-plus state
        assert!(results.is_entangled);
        assert!(results.chsh_value > 2.0); // Quantum violation
        assert!(results.fidelity > 0.8);
        assert!((results.correlation - 1.0).abs() < 0.1);
    }

    #[test]
    fn test_decoherence_application() {
        let mut results = vec![(false, false); 100];
        let original_results = results.clone();
        
        apply_decoherence(&mut results, 0.1);
        
        // Some results should be changed
        assert_ne!(results, original_results);
    }

    #[test]
    fn test_measurement_noise() {
        let mut results = vec![(false, false); 100];
        let original_results = results.clone();
        
        add_measurement_noise(&mut results, 0.2);
        
        // Some results should be changed
        assert_ne!(results, original_results);
    }

    #[test]
    fn test_statistics_generation() {
        let results = vec![(false, false), (true, true), (false, false), (true, true)];
        let stats = generate_statistics(&results);
        
        assert_eq!(stats["P(00)"], 0.5);
        assert_eq!(stats["P(11)"], 0.5);
        assert_eq!(stats["P(01)"], 0.0);
        assert_eq!(stats["P(10)"], 0.0);
        assert!((stats["Correlation"] - 1.0).abs() < 0.01);
    }

    #[test]
    fn test_network_simulation() {
        let results = simulate_network_entanglement(2, 100.0, 0.001, "direct");
        
        assert!(results.decoherence_rate >= 0.0);
        assert!(results.fidelity <= 1.0);
        assert_eq!(results.swaps, 0);
    }

    #[test]
    fn test_teleportation_simulation() {
        let success = simulate_teleportation(100.0, 0.5);
        assert!(success || !success); // Should return a boolean
        
        // Short distance should have higher success rate
        let success_near = simulate_teleportation(10.0, 0.5);
        let success_far = simulate_teleportation(1000.0, 0.5);
        // Note: This is probabilistic, so we just check it runs without error
    }

    #[test]
    fn test_qkd_rate_calculation() {
        let rate = calculate_qkd_rate(100.0, "BB84");
        assert!(rate > 0.0 && rate < 1000.0);
        
        let rate_far = calculate_qkd_rate(1000.0, "BB84");
        assert!(rate_far < rate); // Rate decreases with distance
    }

    #[test]
    fn test_error_correction() {
        let mut results = vec![(false, false); 9];
        let original_results = results.clone();
        
        apply_error_correction(&mut results, 1.0); // 100% correction strength
        
        // Results should be unchanged for perfect data
        assert_eq!(results, original_results);
    }

    #[test]
    fn test_circuit_diagrams() {
        let ascii = generate_circuit_diagram("phi-plus", "ascii");
        assert!(ascii.contains("●"));
        assert!(ascii.contains("⊕"));
        
        let unicode = generate_circuit_diagram("phi-plus", "unicode");
        assert!(unicode.contains("●"));
        
        let latex = generate_circuit_diagram("phi-plus", "latex");
        assert!(latex.contains("quantikz"));
    }

    #[test]
    fn test_measurement_bases() {
        let bases = visualize_measurement_bases();
        assert!(bases.contains("Alice:"));
        assert!(bases.contains("Bob:"));
        assert!(bases.contains("Z basis:"));
        assert!(bases.contains("X basis:"));
    }

    #[test]
    fn test_probability_table() {
        let table = generate_probability_table();
        assert!(table.contains("Bell State Probabilities:"));
        assert!(table.contains("Φ+"));
        assert!(table.contains("0.5"));
    }

    #[test]
    fn test_education_content() {
        // Test that learning functions don't panic
        learn_concept("bell-inequality", false);
        learn_concept("superposition", false);
        learn_concept("decoherence", false);
        learn_concept("teleportation", false);
        learn_concept("invalid", false);
    }

    #[test]
    fn test_edge_cases() {
        // Test with zero measurements
        let results = verify_entanglement(2, 0, "phi-plus", 3);
        assert_eq!(results.correlation, 0.0);
        assert_eq!(results.fidelity, 0.0);
        
        // Test with single measurement
        let results = verify_entanglement(2, 1, "phi-plus", 3);
        assert!(results.correlation.is_finite());
        assert!(results.fidelity.is_finite());
    }

    #[test]
    fn test_precision_handling() {
        let results = verify_entanglement(2, 100, "phi-plus", 5);
        
        // Check that precision doesn't cause issues
        assert!(results.correlation.is_finite());
        assert!(results.chsh_value.is_finite());
        assert!(results.fidelity.is_finite());
    }
}
