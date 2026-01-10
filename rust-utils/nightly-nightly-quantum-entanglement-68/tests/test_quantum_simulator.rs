use nightly_quantum_entanglement_checker::quantum_simulator::QuantumSimulator;

#[test]
fn test_generate_quantum_state() {
    let mut simulator = QuantumSimulator::new();
    let state = simulator.generate_quantum_state(10);
    
    // Mock rationale: Verify state generation creates correct size
    assert_eq!(state.len(), 10);
    
    // Mock rationale: Verify state is normalized
    let norm: f64 = state.iter().map(|x| x.powi(2)).sum();
    assert!((norm - 1.0).abs() < 1e-10);
}

#[test]
fn test_apply_quantum_gate() {
    let mut simulator = QuantumSimulator::new();
    let mut state = vec![1.0, 0.0, 0.0, 0.0];
    
    // Mock rationale: Verify gate application doesn't crash
    simulator.apply_quantum_gate(&mut state);
    
    // Mock rationale: Verify state remains normalized after gate
    let norm: f64 = state.iter().map(|x| x.powi(2)).sum();
    assert!((norm - 1.0).abs() < 1e-10);
}

#[test]
fn test_introduce_decoherence() {
    let mut simulator = QuantumSimulator::new();
    let mut state = vec![1.0, 0.0, 0.0, 0.0];
    
    // Mock rationale: Verify decoherence application doesn't crash
    simulator.introduce_decoherence(&mut state, 0.1);
    
    // Mock rationale: Verify state remains normalized after decoherence
    let norm: f64 = state.iter().map(|x| x.powi(2)).sum();
    assert!((norm - 1.0).abs() < 1e-10);
}

#[test]
fn test_calculate_fidelity() {
    let simulator = QuantumSimulator::new();
    let state_a = vec![1.0, 0.0];
    let state_b = vec![1.0, 0.0];
    
    // Mock rationale: Verify fidelity calculation for identical states
    let fidelity = simulator.calculate_fidelity(&state_a, &state_b);
    assert_eq!(fidelity, 1.0);
}

#[test]
fn test_calculate_bell_fidelity() {
    let simulator = QuantumSimulator::new();
    let state_a = vec![1.0, 0.0];
    let state_b = vec![1.0, 0.0];
    
    // Mock rationale: Verify Bell fidelity calculation
    let bell_fidelity = simulator.calculate_bell_fidelity(&state_a, &state_b);
    assert_eq!(bell_fidelity, 1.0);
}
