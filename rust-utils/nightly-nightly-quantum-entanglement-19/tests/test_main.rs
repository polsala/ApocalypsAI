use nightly_quantum_entanglement_checker::*;

#[cfg(test)]
mod tests {
    use super::*;
    use std::io;
    use std::io::Write;

    #[test]
    fn test_quantum_state_creation() {
        let state = QuantumState::new(0.707, 0.707, 0.0);
        assert_eq!(state.amplitude_a, 0.707);
        assert_eq!(state.amplitude_b, 0.707);
        assert_eq!(state.phase, 0.0);
    }

    #[test]
    fn test_entanglement_fidelity_maximal() {
        // Maximally entangled state (Bell state)
        let state = QuantumState::new(1.0 / 2.0_f64.sqrt(), 1.0 / 2.0_f64.sqrt(), 0.0);
        let fidelity = state.entanglement_fidelity();
        assert!((fidelity - 1.0).abs() < 1e-10, "Expected fidelity ~1.0, got {}", fidelity);
    }

    #[test]
    fn test_entanglement_fidelity_separable() {
        // Separable state (only one amplitude)
        let state = QuantumState::new(1.0, 0.0, 0.0);
        let fidelity = state.entanglement_fidelity();
        assert_eq!(fidelity, 0.0, "Separable state should have zero fidelity");
    }

    #[test]
    fn test_entanglement_fidelity_partial() {
        // Partially entangled state
        let state = QuantumState::new(0.8, 0.6, 0.0);
        let fidelity = state.entanglement_fidelity();
        assert!(fidelity > 0.0 && fidelity < 1.0, "Expected partial fidelity, got {}", fidelity);
    }

    #[test]
    fn test_concurrence_maximal() {
        let state = QuantumState::new(1.0 / 2.0_f64.sqrt(), 1.0 / 2.0_f64.sqrt(), 0.0);
        let concurrence = state.concurrence();
        assert!((concurrence - 1.0).abs() < 1e-10, "Expected concurrence ~1.0, got {}", concurrence);
    }

    #[test]
    fn test_concurrence_separable() {
        let state = QuantumState::new(1.0, 0.0, 0.0);
        let concurrence = state.concurrence();
        assert_eq!(concurrence, 0.0, "Separable state should have zero concurrence");
    }

    #[test]
    fn test_tangle_calculation() {
        let state = QuantumState::new(1.0 / 2.0_f64.sqrt(), 1.0 / 2.0_f64.sqrt(), 0.0);
        let tangle = state.tangle();
        assert!((tangle - 1.0).abs() < 1e-10, "Expected tangle ~1.0, got {}", tangle);
    }

    #[test]
    fn test_bell_state_phi_plus() {
        let state = BellState::PhiPlus;
        let ideal = state.ideal_state();
        assert!((ideal.amplitude_a - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
        assert!((ideal.amplitude_b - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
        assert_eq!(ideal.phase, 0.0);
    }

    #[test]
    fn test_bell_state_phi_minus() {
        let state = BellState::PhiMinus;
        let ideal = state.ideal_state();
        assert!((ideal.amplitude_a - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
        assert!((ideal.amplitude_b + 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
        assert_eq!(ideal.phase, 0.0);
    }

    #[test]
    fn test_bell_state_psi_plus() {
        let state = BellState::PsiPlus;
        let ideal = state.ideal_state();
        assert_eq!(ideal.amplitude_a, 0.0);
        assert!((ideal.amplitude_b - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
        assert_eq!(ideal.phase, std::f64::consts::PI / 2.0);
    }

    #[test]
    fn test_bell_state_psi_minus() {
        let state = BellState::PsiMinus;
        let ideal = state.ideal_state();
        assert!((ideal.amplitude_a - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
        assert!((ideal.amplitude_b + 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
        assert_eq!(ideal.phase, std::f64::consts::PI / 2.0);
    }

    #[test]
    fn test_bell_state_from_string() {
        assert_eq!(BellState::from_str("phi_plus"), Some(BellState::PhiPlus));
        assert_eq!(BellState::from_str("phi+"), Some(BellState::PhiPlus));
        assert_eq!(BellState::from_str("phi_minus"), Some(BellState::PhiMinus));
        assert_eq!(BellState::from_str("phi-"), Some(BellState::PhiMinus));
        assert_eq!(BellState::from_str("psi_plus"), Some(BellState::PsiPlus));
        assert_eq!(BellState::from_str("psi+"), Some(BellState::PsiPlus));
        assert_eq!(BellState::from_str("psi_minus"), Some(BellState::PsiMinus));
        assert_eq!(BellState::from_str("psi-"), Some(BellState::PsiMinus));
        assert_eq!(BellState::from_str("invalid"), None);
    }

    #[test]
    fn test_edge_case_zero_amplitudes() {
        let state = QuantumState::new(0.0, 0.0, 0.0);
        let fidelity = state.entanglement_fidelity();
        assert_eq!(fidelity, 0.0, "Zero amplitudes should give zero fidelity");
    }

    #[test]
    fn test_edge_case_negative_amplitudes() {
        let state = QuantumState::new(-0.5, 0.5, 0.0);
        let fidelity = state.entanglement_fidelity();
        assert!(fidelity >= 0.0, "Fidelity should be non-negative, got {}", fidelity);
    }

    #[test]
    fn test_normalization_independence() {
        // Different normalizations should give same relative fidelity
        let state1 = QuantumState::new(1.0, 1.0, 0.0);
        let state2 = QuantumState::new(0.5, 0.5, 0.0);
        
        let fidelity1 = state1.entanglement_fidelity();
        let fidelity2 = state2.entanglement_fidelity();
        
        assert!((fidelity1 - fidelity2).abs() < 1e-10, "Normalized states should have same fidelity");
    }

    #[test]
    fn test_concurrence_bounds() {
        // Test various amplitude combinations
        let test_cases = vec![
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.5, 0.5, 0.0),
            (1.0 / 2.0_f64.sqrt(), 1.0 / 2.0_f64.sqrt(), 0.0),
        ];
        
        for (a, b, expected_min) in test_cases {
            let state = QuantumState::new(a, b, 0.0);
            let concurrence = state.concurrence();
            assert!(concurrence >= 0.0, "Concurrence should be >= 0, got {} for ({}, {})", concurrence, a, b);
            assert!(concurrence <= 1.0, "Concurrence should be <= 1, got {} for ({}, {})", concurrence, a, b);
        }
    }

    #[test]
    fn test_performance_consistency() {
        // Quick performance test to ensure calculations are fast
        let start = std::time::Instant::now();
        
        for _ in 0..1000 {
            let state = QuantumState::new(0.707, 0.707, 0.0);
            let _ = state.entanglement_fidelity();
            let _ = state.concurrence();
            let _ = state.tangle();
        }
        
        let duration = start.elapsed();
        // Should complete 1000 calculations in well under 100ms
        assert!(duration.as_millis() < 100, "Performance test too slow: {:?}", duration);
    }

    #[test]
    fn test_mathematical_consistency() {
        // Tangle should equal concurrence squared
        let state = QuantumState::new(0.6, 0.8, 0.0);
        let concurrence = state.concurrence();
        let tangle = state.tangle();
        
        assert!((tangle - concurrence.powi(2)).abs() < 1e-10, "Tangle should equal concurrence squared");
    }

    #[test]
    fn test_bell_state_fidelities() {
        // All Bell states should have maximal entanglement
        let bell_states = vec![
            BellState::PhiPlus,
            BellState::PhiMinus,
            BellState::PsiPlus,
            BellState::PsiMinus,
        ];
        
        for state in bell_states {
            let ideal = state.ideal_state();
            let fidelity = ideal.entanglement_fidelity();
            assert!((fidelity - 1.0).abs() < 1e-10, "Bell state {:?} should have maximal fidelity", state);
        }
    }
}
