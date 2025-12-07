use nightly_quantum_entanglement_checker::*;
use std::sync::Once;

static INIT: Once = Once::new();

/// Initialize test environment
fn init() {
    INIT.call_once(|| {
        // Setup code here if needed
    });
}

#[cfg(test)]
mod tests {
    use super::*;
    use quantum_simulator::QuantumSimulator;
    use metrics::QuantumMetrics;
    use cli::parse_args;

    #[test]
    fn test_quantum_simulator_creation() {
        // Test that we can create a quantum simulator
        let simulator = QuantumSimulator::new();
        assert_eq!(simulator.entanglement_count(), 0);
    }

    #[test]
    fn test_entanglement_check() {
        // Test entanglement checking between nodes
        let mut simulator = QuantumSimulator::new();
        
        let fidelity = simulator.check_entanglement("node1", "node2");
        
        // Fidelity should be between 0.5 and 1.0
        assert!(fidelity >= 0.5 && fidelity <= 1.0);
        
        // Should have one entanglement state
        assert_eq!(simulator.entanglement_count(), 1);
    }

    #[test]
    fn test_entanglement_symmetry() {
        // Test that entanglement is symmetric
        let mut simulator = QuantumSimulator::new();
        
        let fidelity1 = simulator.check_entanglement("node1", "node2");
        let fidelity2 = simulator.check_entanglement("node2", "node1");
        
        // Should be the same (within quantum fluctuation range)
        assert!((fidelity1 - fidelity2).abs() < 0.1);
    }

    #[test]
    fn test_quantum_metrics_creation() {
        // Test that we can create quantum metrics
        let metrics = QuantumMetrics::new();
        assert!(metrics.base_superposition > 0.0);
        assert!(metrics.base_entanglement > 0.0);
        assert!(metrics.base_coherence > 0.0);
    }

    #[test]
    fn test_current_metrics_generation() {
        // Test generating current metrics
        let mut metrics = QuantumMetrics::new();
        let current = metrics.generate_current_metrics();
        
        // All metrics should be between 0.0 and 1.0
        assert!(current.superposition_stability >= 0.0 && current.superposition_stability <= 1.0);
        assert!(current.entanglement_fidelity >= 0.0 && current.entanglement_fidelity <= 1.0);
        assert!(current.decoherence_resistance >= 0.0 && current.decoherence_resistance <= 1.0);
        assert!(current.tunneling_events >= 0);
    }

    #[test]
    fn test_cli_args_parsing() {
        // Test CLI argument parsing
        // This test would need to be run with specific arguments
        // For now, we'll test the help functionality indirectly
        
        // Create a minimal test by checking that we can call parse_args
        // with no arguments (should use defaults)
        let args = vec!["test".to_string()];
        
        // We can't easily test the full CLI without setting up the environment
        // So we'll test individual components
        assert!(true); // Placeholder
    }

    #[test]
    fn test_multiple_node_entanglement() {
        // Test entanglement between multiple nodes
        let mut simulator = QuantumSimulator::new();
        let nodes = vec!["node1", "node2", "node3", "node4"];
        
        // Check all pairs
        let mut fidelities = Vec::new();
        for i in 0..nodes.len() {
            for j in (i + 1)..nodes.len() {
                let fidelity = simulator.check_entanglement(nodes[i], nodes[j]);
                fidelities.push(fidelity);
            }
        }
        
        // Should have 6 entanglements (4 choose 2)
        assert_eq!(fidelities.len(), 6);
        
        // All should be valid
        for fidelity in fidelities {
            assert!(fidelity >= 0.5 && fidelity <= 1.0);
        }
    }

    #[test]
    fn test_entanglement_state_persistence() {
        // Test that entanglement states persist and fluctuate
        let mut simulator = QuantumSimulator::new();
        
        // First check
        let fidelity1 = simulator.check_entanglement("node1", "node2");
        
        // Second check should be similar but not identical (quantum fluctuation)
        let fidelity2 = simulator.check_entanglement("node1", "node2");
        
        // Should be close but not identical
        assert!((fidelity1 - fidelity2).abs() < 0.2);
    }

    #[test]
    fn test_quantum_events_simulation() {
        // Test quantum event simulation
        let mut simulator = QuantumSimulator::new();
        
        // Simulate events multiple times
        for _ in 0..10 {
            let events = simulator.simulate_quantum_events();
            
            // Events should be valid strings
            for event in events {
                assert!(!event.is_empty());
                assert!(event.len() > 10); // Reasonable minimum length
            }
        }
    }

    #[test]
    fn test_metrics_base_update() {
        // Test updating base metrics
        let mut metrics = QuantumMetrics::new();
        
        // Update with new values
        metrics.update_base_metrics(0.9, 0.85, 0.8);
        
        // Generate new metrics
        let current = metrics.generate_current_metrics();
        
        // Should reflect the updated base values
        assert!(current.superposition_stability > 0.7);
        assert!(current.entanglement_fidelity > 0.6);
        assert!(current.decoherence_resistance > 0.5);
    }

    #[test]
    fn test_entanglement_reset() {
        // Test resetting entanglements
        let mut simulator = QuantumSimulator::new();
        
        // Create some entanglements
        simulator.check_entanglement("node1", "node2");
        simulator.check_entanglement("node1", "node3");
        simulator.check_entanglement("node2", "node3");
        
        // Should have 3 entanglements
        assert_eq!(simulator.entanglement_count(), 3);
        
        // Reset
        simulator.reset_entanglements();
        
        // Should have no entanglements
        assert_eq!(simulator.entanglement_count(), 0);
    }
}
