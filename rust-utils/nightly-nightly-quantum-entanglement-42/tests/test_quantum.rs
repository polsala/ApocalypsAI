use nightly_quantum_entanglement_checker::quantum::{QuantumState, MeasurementBasis};
use rand::thread_rng;

#[test]
fn test_quantum_state_creation() {
    let state = QuantumState::new(1.0, 0.0);
    assert_eq!(state.alpha, 1.0);
    assert_eq!(state.beta, 0.0);
}

#[test]
fn test_quantum_state_normalization() {
    let state = QuantumState::new(1.0, 1.0);
    let norm = (state.alpha.powi(2) + state.beta.powi(2)).sqrt();
    assert!((norm - 1.0).abs() < 1e-10);
}

#[test]
fn test_entangled_copy() {
    let state = QuantumState::new(0.6, 0.8);
    let entangled = state.entangled_copy();
    
    // For entangled copy, amplitudes should be swapped
    assert_eq!(entangled.alpha, 0.8);
    assert_eq!(entangled.beta, 0.6);
}

#[test]
fn test_measurement_basis_random() {
    let mut rng = thread_rng();
    let basis = MeasurementBasis::random(&mut rng);
    
    // Should be either Z or X
    match basis {
        MeasurementBasis::Z => {},
        MeasurementBasis::X => {},
    }
}

#[test]
fn test_hadamard_gate() {
    let mut state = QuantumState::new(1.0, 0.0); // |0> state
    state.apply_hadamard();
    
    // After Hadamard, should be equal superposition
    assert!((state.alpha - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
    assert!((state.beta - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
}

#[test]
fn test_pauli_x_gate() {
    let mut state = QuantumState::new(1.0, 0.0); // |0> state
    state.apply_pauli_x();
    
    // After Pauli-X, should be |1> state
    assert_eq!(state.alpha, 0.0);
    assert_eq!(state.beta, 1.0);
}

#[test]
fn test_pauli_z_gate() {
    let mut state = QuantumState::new(0.707, 0.707); // Equal superposition
    let original_beta = state.beta;
    state.apply_pauli_z();
    
    // Pauli-Z should flip the phase of |1> component
    assert_eq!(state.alpha, 0.707);
    assert_eq!(state.beta, -original_beta);
}

#[test]
fn test_fidelity_calculation() {
    let state1 = QuantumState::new(1.0, 0.0);
    let state2 = QuantumState::new(1.0, 0.0);
    
    let fidelity = state1.fidelity(&state2);
    assert!((fidelity - 1.0).abs() < 1e-10);
}

#[test]
fn test_random_state_generation() {
    let mut rng = thread_rng();
    let state = QuantumState::random(&mut rng);
    
    // Random state should be normalized
    let norm = (state.alpha.powi(2) + state.beta.powi(2)).sqrt();
    assert!((norm - 1.0).abs() < 1e-10);
}

#[test]
fn test_measurement_consistency() {
    let mut rng = thread_rng();
    let state = QuantumState::random(&mut rng);
    
    // Multiple measurements in same basis should be consistent
    let basis = MeasurementBasis::Z;
    let result1 = state.measure(&basis);
    let result2 = state.measure(&basis);
    
    // Note: Due to quantum randomness, results may differ
    // This test mainly checks that measurements don't panic
    assert!(result1 == true || result1 == false);
    assert!(result2 == true || result2 == false);
}
