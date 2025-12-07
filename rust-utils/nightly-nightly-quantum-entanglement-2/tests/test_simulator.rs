use nightly_quantum_entanglement_checker::quantum_simulator::QuantumSimulator;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_simulator_empty() {
        let simulator = QuantumSimulator::new();
        assert_eq!(simulator.entanglement_count(), 0);
    }

    #[test]
    fn test_entanglement_fidelity_range() {
        let mut simulator = QuantumSimulator::new();
        let fidelity = simulator.check_entanglement("test1", "test2");
        
        // Should be in valid range
        assert!(fidelity >= 0.5 && fidelity <= 1.0, "Fidelity {} out of range", fidelity);
    }

    #[test]
    fn test_entanglement_state_access() {
        let mut simulator = QuantumSimulator::new();
        simulator.check_entanglement("node1", "node2");
        
        let state = simulator.get_entanglement_state("node1", "node2");
        assert!(state.is_some());
        
        let state = state.unwrap();
        assert!(state.contains_key("fidelity"));
        assert!(state.contains_key("phase"));
        assert!(state.contains_key("coherence"));
    }

    #[test]
    fn test_entanglement_order_independence() {
        let mut simulator = QuantumSimulator::new();
        
        // Check in one order
        let fidelity1 = simulator.check_entanglement("alpha", "beta");
        
        // Check in reverse order
        let fidelity2 = simulator.check_entanglement("beta", "alpha");
        
        // Should be the same
        assert_eq!(fidelity1, fidelity2, "Entanglement should be order-independent");
    }
}
