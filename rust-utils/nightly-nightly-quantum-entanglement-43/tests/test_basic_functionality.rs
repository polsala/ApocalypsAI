use nightly_quantum_entanglement_simulator::*;
use quantum_simulator::{QuantumSimulator, Gate, Complex};

#[test]
fn test_basic_hadamard_gate() {
    let mut simulator = QuantumSimulator::new(1);
    simulator.apply_gate(&Gate::Hadamard(0));
    
    let state = simulator.get_state();
    assert!(state.amplitudes[0].magnitude() > 0.6);
    assert!(state.amplitudes[1].magnitude() > 0.6);
}

#[test]
fn test_bell_state_creation() {
    let mut simulator = QuantumSimulator::new(2);
    simulator.apply_gate(&Gate::Hadamard(0));
    simulator.apply_gate(&Gate::CNOT(0, 1));
    
    let state = simulator.get_state();
    assert!(state.is_entangled());
    
    // Should have equal probabilities for |00⟩ and |11⟩
    let prob_00 = state.probability(0); // |00⟩
    let prob_11 = state.probability(3); // |11⟩
    
    assert!(prob_00 > 0.4);
    assert!(prob_11 > 0.4);
    assert!(prob_00 + prob_11 > 0.99);
}

#[test]
fn test_ghz_state_creation() {
    let mut simulator = QuantumSimulator::new(3);
    simulator.apply_gate(&Gate::Hadamard(0));
    simulator.apply_gate(&Gate::CNOT(0, 1));
    simulator.apply_gate(&Gate::CNOT(1, 2));
    
    let state = simulator.get_state();
    assert!(state.is_entangled());
    
    // Should have equal probabilities for |000⟩ and |111⟩
    let prob_000 = state.probability(0); // |000⟩
    let prob_111 = state.probability(7); // |111⟩
    
    assert!(prob_000 > 0.4);
    assert!(prob_111 > 0.4);
    assert!(prob_000 + prob_111 > 0.99);
}

#[test]
fn test_measurement_consistency() {
    let mut simulator = QuantumSimulator::new(2);
    simulator.apply_gate(&Gate::Hadamard(0));
    simulator.apply_gate(&Gate::CNOT(0, 1));
    
    let measurements = simulator.measure(1000);
    
    // Should only get |00⟩ and |11⟩ outcomes
    for (outcome, _) in &measurements {
        assert!(outcome == "00" || outcome == "11");
    }
    
    // Should have roughly equal distribution
    let count_00 = measurements.get("00").unwrap_or(&0);
    let count_11 = measurements.get("11").unwrap_or(&0);
    
    let diff = (count_00 - count_11).abs();
    assert!(diff < 100); // Allow some variance in random sampling
}

#[test]
fn test_circuit_parser() {
    let gates = vec!["h(0)".to_string(), "cx(0,1)".to_string()];
    let parsed = circuit_parser::parse_circuit(&gates);
    
    assert_eq!(parsed.len(), 2);
    assert_eq!(parsed[0], Gate::Hadamard(0));
    assert_eq!(parsed[1], Gate::CNOT(0, 1));
}

#[test]
fn test_entanglement_detection() {
    // Test separable state
    let mut simulator = QuantumSimulator::new(2);
    simulator.apply_gate(&Gate::Hadamard(0));
    let state = simulator.get_state();
    assert!(!state.is_entangled());
    
    // Test entangled state
    let mut simulator = QuantumSimulator::new(2);
    simulator.apply_gate(&Gate::Hadamard(0));
    simulator.apply_gate(&Gate::CNOT(0, 1));
    let state = simulator.get_state();
    assert!(state.is_entangled());
}

#[test]
fn test_swap_gate() {
    let mut simulator = QuantumSimulator::new(2);
    
    // Create state |01⟩
    simulator.apply_gate(&Gate::PauliX(1));
    
    let state = simulator.get_state();
    assert!(state.probability(1) > 0.99); // |01⟩
    
    // Apply SWAP
    simulator.apply_gate(&Gate::SWAP(0, 1));
    
    let state = simulator.get_state();
    assert!(state.probability(2) > 0.99); // |10⟩
}
