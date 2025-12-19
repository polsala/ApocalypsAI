use nightly_quantum_entanglement_checker::*;

// Mock RNG for deterministic testing
struct MockRng {
    values: Vec<f64>,
    index: usize,
}

impl MockRng {
    fn new(values: Vec<f64>) -> Self {
        Self {
            values,
            index: 0,
        }
    }
}

impl DeterministicRng {
    fn with_mock_values(values: Vec<f64>) -> Self {
        let mut rng = DeterministicRng::new(42);
        // We'll override the state for testing
        rng.state = 0;
        // This is a bit of a hack, but we need to make the RNG deterministic
        // In a real implementation, we'd make the RNG injectable
        rng
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_entanglement_status_from_coherence() {
        // Mock rationale: Testing deterministic status mapping based on coherence thresholds
        assert_eq!(EntanglementStatus::from_coherence(0.8), EntanglementStatus::Entangled);
        assert_eq!(EntanglementStatus::from_coherence(0.75), EntanglementStatus::Entangled);
        assert_eq!(EntanglementStatus::from_coherence(0.6), EntanglementStatus::Weak);
        assert_eq!(EntanglementStatus::from_coherence(0.5), EntanglementStatus::Weak);
        assert_eq!(EntanglementStatus::from_coherence(0.4), EntanglementStatus::Broken);
        assert_eq!(EntanglementStatus::from_coherence(0.0), EntanglementStatus::Broken);
    }

    #[test]
    fn test_entanglement_status_emoji() {
        // Mock rationale: Testing emoji representation for different statuses
        assert_eq!(EntanglementStatus::Entangled.emoji(), "✨");
        assert_eq!(EntanglementStatus::Weak.emoji(), "⚠️");
        assert_eq!(EntanglementStatus::Broken.emoji(), "❌");
    }

    #[test]
    fn test_entanglement_status_description() {
        // Mock rationale: Testing text description for different statuses
        assert_eq!(EntanglementStatus::Entangled.description(), "ENTANGLED");
        assert_eq!(EntanglementStatus::Weak.description(), "WEAK");
        assert_eq!(EntanglementStatus::Broken.description(), "BROKEN");
    }

    #[test]
    fn test_deterministic_rng() {
        // Mock rationale: Testing that our RNG produces deterministic sequences
        let mut rng1 = DeterministicRng::new(42);
        let mut rng2 = DeterministicRng::new(42);
        
        // Generate sequences
        let values1: Vec<f64> = (0..5).map(|_| rng1.next_f64()).collect();
        let values2: Vec<f64> = (0..5).map(|_| rng2.next_f64()).collect();
        
        // They should be identical
        assert_eq!(values1, values2);
    }

    #[test]
    fn test_coherence_calculation() {
        // Mock rationale: Testing coherence calculation with known distances
        let mut checker = QuantumChecker::new(3, 1000.0, 0.7);
        
        // Node 0 to Node 1 (1000km distance)
        let coherence_01 = checker.calculate_coherence(0, 1);
        assert!(coherence_01 > 0.0 && coherence_01 < 1.0);
        
        // Node 0 to Node 2 (2000km distance) should have lower coherence
        let coherence_02 = checker.calculate_coherence(0, 2);
        assert!(coherence_02 <= coherence_01);
        
        // Same node should have maximum coherence
        let coherence_00 = checker.calculate_coherence(0, 0);
        assert_eq!(coherence_00, 1.0);
    }

    #[test]
    fn test_network_health_calculation() {
        // Mock rationale: Testing health calculation with known coherence values
        let checker = QuantumChecker::new(3, 1000.0, 0.7);
        
        let results = vec![
            (0, 1, 0.8, EntanglementStatus::Entangled),
            (0, 2, 0.6, EntanglementStatus::Weak),
            (1, 2, 0.9, EntanglementStatus::Entangled),
        ];
        
        let health = checker.calculate_network_health(&results);
        let expected_health = ((0.8 + 0.6 + 0.9) / 3.0) * 100.0;
        assert!((health - expected_health).abs() < 0.01);
    }

    #[test]
    fn test_recommendation_system() {
        // Mock rationale: Testing recommendation based on network health
        let checker = QuantumChecker::new(3, 1000.0, 0.7);
        
        assert!(checker.get_recommendation(80.0).contains("excellent"));
        assert!(checker.get_recommendation(60.0).contains("quantum repeaters"));
        assert!(checker.get_recommendation(30.0).contains("recalibrating"));
        assert!(checker.get_recommendation(10.0).contains("Emergency protocol"));
    }

    #[test]
    fn test_entanglement_verification() {
        // Mock rationale: Testing that verification produces correct number of pairs
        let mut checker = QuantumChecker::new(4, 1000.0, 0.7);
        let results = checker.verify_entanglement();
        
        // For 4 nodes, we should have 6 pairs: (0,1), (0,2), (0,3), (1,2), (1,3), (2,3)
        assert_eq!(results.len(), 6);
        
        // All coherences should be between 0 and 1
        for (_, _, coherence, _) in &results {
            assert!(*coherence >= 0.0 && *coherence <= 1.0);
        }
    }

    #[test]
    fn test_edge_cases() {
        // Mock rationale: Testing edge cases like minimum nodes and extreme distances
        
        // Minimum nodes (2)
        let mut checker = QuantumChecker::new(2, 1000.0, 0.7);
        let results = checker.verify_entanglement();
        assert_eq!(results.len(), 1);
        
        // Very large distance should result in low coherence
        let mut checker = QuantumChecker::new(2, 100000.0, 0.7);
        let coherence = checker.calculate_coherence(0, 1);
        assert!(coherence < 0.1);
        
        // Very small distance should result in high coherence
        let mut checker = QuantumChecker::new(2, 1.0, 0.7);
        let coherence = checker.calculate_coherence(0, 1);
        assert!(coherence > 0.9);
    }

    #[test]
    fn test_deterministic_output() {
        // Mock rationale: Testing that the same inputs produce the same outputs
        let mut checker1 = QuantumChecker::new(3, 1000.0, 0.7);
        let mut checker2 = QuantumChecker::new(3, 1000.0, 0.7);
        
        let results1 = checker1.verify_entanglement();
        let results2 = checker2.verify_entanglement();
        
        // Results should be identical due to deterministic RNG
        assert_eq!(results1.len(), results2.len());
        for (r1, r2) in results1.iter().zip(results2.iter()) {
            assert_eq!(r1.0, r2.0);
            assert_eq!(r1.1, r2.1);
            // Allow small floating point differences
            assert!((r1.2 - r2.2).abs() < 0.001);
            assert_eq!(r1.3, r2.3);
        }
    }
}
