use nightly_quantum_entanglement_checker::{QuantumSimulator, EntanglementChecker};

#[test]
fn test_full_quantum_workflow() {
    let mut simulator = QuantumSimulator::new();
    let mut checker = EntanglementChecker::new();
    
    // Mock rationale: Verify complete quantum workflow
    let state_a = simulator.generate_quantum_state(100);
    let state_b = simulator.generate_quantum_state(100);
    
    let result = checker.check_entanglement(&state_a, &state_b);
    
    // Results should be within valid ranges
    assert!(result.entanglement_score >= 0.0 && result.entanglement_score <= 1.0);
    assert!(result.bell_state_fidelity >= 0.0 && result.bell_state_fidelity <= 1.0);
    assert!(result.decoherence_level >= 0.0 && result.decoherence_level <= 1.0);
}

#[test]
fn test_quantum_gate_sequence() {
    let mut simulator = QuantumSimulator::new();
    let mut state = simulator.generate_quantum_state(50);
    
    // Mock rationale: Verify multiple quantum operations
    for _ in 0..5 {
        simulator.apply_quantum_gate(&mut state);
        simulator.introduce_decoherence(&mut state, 0.05);
    }
    
    // State should remain normalized
    let norm: f64 = state.iter().map(|x| x.powi(2)).sum();
    assert!((norm - 1.0).abs() < 1e-10);
}
