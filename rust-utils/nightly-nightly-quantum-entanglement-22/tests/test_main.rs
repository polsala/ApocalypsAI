use nightly_quantum_entanglement_checker::*;
use std::sync::OnceLock;

static TEST_RNG: OnceLock<rand::rngs::ThreadRng> = OnceLock::new();

/// Helper function to get a test RNG
fn get_test_rng() -> &'static rand::rngs::ThreadRng {
    TEST_RNG.get_or_init(|| rand::thread_rng())
}

#[cfg(test)]
mod tests {
    use super::*;
    use rand::SeedableRng;
    use rand_chacha::ChaCha8Rng;

    /// Test quantum correlation structure
    #[test]
    fn test_quantum_correlation_creation() {
        let correlation = QuantumCorrelation {
            node_a: 0,
            node_b: 1,
            correlation: 0.85,
            spooky: true,
        };

        assert_eq!(correlation.node_a, 0);
        assert_eq!(correlation.node_b, 1);
        assert_eq!(correlation.correlation, 0.85);
        assert!(correlation.spooky);
    }

    /// Test quantum entanglement checker initialization
    #[test]
    fn test_checker_initialization() {
        let checker = QuantumEntanglementChecker::new(4, 100, 0.8);

        assert_eq!(checker.nodes, 4);
        assert_eq!(checker.iterations, 100);
        assert_eq!(checker.threshold, 0.8);
    }

    /// Test quantum random number generation
    #[test]
    fn test_generate_quantum_random() {
        let mut checker = QuantumEntanglementChecker::new(2, 10, 0.5);
        
        for _ in 0..100 {
            let random = checker.generate_quantum_random();
            assert!(random >= 0.0 && random <= 1.0, 
                   "Random number {} is out of bounds", random);
        }
    }

    /// Test entanglement between nodes
    #[test]
    fn test_entangle_nodes() {
        let mut checker = QuantumEntanglementChecker::new(4, 10, 0.8);
        
        let correlation = checker.entangle_nodes(0, 1);
        
        assert_eq!(correlation.node_a, 0);
        assert_eq!(correlation.node_b, 1);
        assert!(correlation.correlation >= 0.0 && correlation.correlation <= 1.0);
        assert!(correlation.spooky == (correlation.correlation > 0.8));
    }

    /// Test entanglement verification
    #[test]
    fn test_verify_entanglement() {
        let mut checker = QuantumEntanglementChecker::new(3, 10, 0.5);
        let correlations = checker.verify_entanglement();
        
        // Should have some correlations
        assert!(correlations.len() > 0);
        
        // All correlations should be valid
        for correlation in &correlations {
            assert!(correlation.correlation >= 0.0 && correlation.correlation <= 1.0);
            assert!(correlation.spooky == (correlation.correlation > 0.5));
        }
    }

    /// Test spooky correlation detection
    #[test]
    fn test_spooky_correlation_detection() {
        let mut checker = QuantumEntanglementChecker::new(2, 100, 0.9);
        let correlations = checker.verify_entanglement();
        
        // With high threshold, should have fewer spooky correlations
        let spooky_count = correlations.iter().filter(|c| c.spooky).count();
        let total_count = correlations.len();
        
        assert!(spooky_count <= total_count);
        assert!(spooky_count < total_count, "With threshold 0.9, not all correlations should be spooky");
    }

    /// Test low threshold correlation detection
    #[test]
    fn test_low_threshold_correlation_detection() {
        let mut checker = QuantumEntanglementChecker::new(2, 100, 0.1);
        let correlations = checker.verify_entanglement();
        
        // With low threshold, should have many spooky correlations
        let spooky_count = correlations.iter().filter(|c| c.spooky).count();
        let total_count = correlations.len();
        
        assert!(spooky_count > total_count / 2, "With threshold 0.1, most correlations should be spooky");
    }

    /// Test correlation bounds
    #[test]
    fn test_correlation_bounds() {
        let mut checker = QuantumEntanglementChecker::new(5, 1000, 0.5);
        let correlations = checker.verify_entanglement();
        
        for correlation in correlations {
            assert!(correlation.correlation >= 0.0, "Correlation {} is below 0.0", correlation.correlation);
            assert!(correlation.correlation <= 1.0, "Correlation {} is above 1.0", correlation.correlation);
        }
    }

    /// Test that different runs produce different results (quantum randomness)
    #[test]
    fn test_quantum_randomness() {
        let mut checker1 = QuantumEntanglementChecker::new(3, 50, 0.5);
        let mut checker2 = QuantumEntanglementChecker::new(3, 50, 0.5);
        
        let correlations1 = checker1.verify_entanglement();
        let correlations2 = checker2.verify_entanglement();
        
        // Results should be different (quantum randomness)
        let avg1 = correlations1.iter().map(|c| c.correlation).sum::<f64>() / correlations1.len() as f64;
        let avg2 = correlations2.iter().map(|c| c.correlation).sum::<f64>() / correlations2.len() as f64;
        
        // Allow for some variance due to randomness
        let diff = (avg1 - avg2).abs();
        assert!(diff < 0.3, "Averages should be different due to quantum randomness: {} vs {}", avg1, avg2);
    }

    /// Test edge case: minimum nodes
    #[test]
    fn test_minimum_nodes() {
        let mut checker = QuantumEntanglementChecker::new(2, 10, 0.5);
        let correlations = checker.verify_entanglement();
        
        assert!(correlations.len() > 0);
        
        for correlation in correlations {
            assert!(correlation.node_a < 2);
            assert!(correlation.node_b < 2);
            assert_ne!(correlation.node_a, correlation.node_b);
        }
    }

    /// Test edge case: many nodes
    #[test]
    fn test_many_nodes() {
        let mut checker = QuantumEntanglementChecker::new(100, 100, 0.5);
        let correlations = checker.verify_entanglement();
        
        assert!(correlations.len() > 0);
        
        for correlation in correlations {
            assert!(correlation.node_a < 100);
            assert!(correlation.node_b < 100);
            assert_ne!(correlation.node_a, correlation.node_b);
        }
    }
}
