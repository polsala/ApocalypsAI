use nightly_quantum_entanglement_checker::metrics::{QuantumMetrics, CurrentMetrics};

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_metrics_creation() {
        let metrics = QuantumMetrics::new();
        assert_eq!(metrics.base_superposition, 0.95);
        assert_eq!(metrics.base_entanglement, 0.90);
        assert_eq!(metrics.base_coherence, 0.88);
    }

    #[test]
    fn test_current_metrics_validity() {
        let mut metrics = QuantumMetrics::new();
        let current = metrics.generate_current_metrics();
        
        // All percentages should be between 0 and 1
        assert!(current.superposition_stability >= 0.0 && current.superposition_stability <= 1.0);
        assert!(current.entanglement_fidelity >= 0.0 && current.entanglement_fidelity <= 1.0);
        assert!(current.decoherence_resistance >= 0.0 && current.decoherence_resistance <= 1.0);
        
        // Tunneling events should be non-negative
        assert!(current.tunneling_events >= 0);
    }

    #[test]
    fn test_base_metrics_update() {
        let mut metrics = QuantumMetrics::new();
        
        // Update with valid values
        metrics.update_base_metrics(0.95, 0.92, 0.89);
        
        // Generate new metrics
        let current = metrics.generate_current_metrics();
        
        // Should be reasonable
        assert!(current.superposition_stability > 0.7);
        assert!(current.entanglement_fidelity > 0.7);
        assert!(current.decoherence_resistance > 0.7);
    }

    #[test]
    fn test_base_metrics_clamping() {
        let mut metrics = QuantumMetrics::new();
        
        // Try to set values outside valid range
        metrics.update_base_metrics(1.5, -0.1, 0.5);
        
        // Should be clamped to valid range
        let current = metrics.generate_current_metrics();
        assert!(current.superposition_stability <= 1.0);
        assert!(current.entanglement_fidelity >= 0.0);
    }

    #[test]
    fn test_tunneling_events_range() {
        let mut metrics = QuantumMetrics::new();
        
        // Generate multiple times to test range
        for _ in 0..100 {
            let current = metrics.generate_current_metrics();
            
            // Should be reasonable number of events
            assert!(current.tunneling_events >= 20 && current.tunneling_events <= 50);
        }
    }
}
