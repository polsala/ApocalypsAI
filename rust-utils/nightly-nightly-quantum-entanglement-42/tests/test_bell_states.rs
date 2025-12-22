use nightly_quantum_entanglement_checker::bell_states::{BellState, BellStateType};
use nightly_quantum_entanglement_checker::quantum::{QuantumState, MeasurementBasis};

#[test]
fn test_bell_state_creation() {
    let bell_state = BellState::new(BellStateType::PhiPlus);
    assert_eq!(bell_state.get_type(), "|Φ⁺⟩");
}

#[test]
fn test_phi_plus_state() {
    let bell_state = BellState::new(BellStateType::PhiPlus);
    
    // PhiPlus should have equal amplitudes
    assert!((bell_state.qubit1.alpha - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
    assert!((bell_state.qubit1.beta - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
    assert!((bell_state.qubit2.alpha - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
    assert!((bell_state.qubit2.beta - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
}

#[test]
fn test_phi_minus_state() {
    let bell_state = BellState::new(BellStateType::PhiMinus);
    
    // PhiMinus should have opposite phase for second qubit
    assert!((bell_state.qubit1.alpha - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
    assert!((bell_state.qubit1.beta - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
    assert!((bell_state.qubit2.alpha - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
    assert!((bell_state.qubit2.beta + 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
}

#[test]
fn test_psi_plus_state() {
    let bell_state = BellState::new(BellStateType::PsiPlus);
    
    // PsiPlus should have different amplitudes
    assert!((bell_state.qubit1.alpha - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
    assert!((bell_state.qubit1.beta + 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
    assert!((bell_state.qubit2.alpha - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
    assert!((bell_state.qubit2.beta - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
}

#[test]
fn test_psi_minus_state() {
    let bell_state = BellState::new(BellStateType::PsiMinus);
    
    // PsiMinus should have both opposite phases
    assert!((bell_state.qubit1.alpha - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
    assert!((bell_state.qubit1.beta + 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
    assert!((bell_state.qubit2.alpha - 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
    assert!((bell_state.qubit2.beta + 1.0 / 2.0_f64.sqrt()).abs() < 1e-10);
}

#[test]
fn test_bell_measurement() {
    let mut bell_state = BellState::new(BellStateType::PhiPlus);
    let (result1, result2) = bell_state.apply_bell_measurement();
    
    // For PhiPlus, measurements should be correlated
    // Both should be true or both should be false
    assert_eq!(result1, result2);
}

#[test]
fn test_fidelity_with_ideal() {
    let bell_state = BellState::new(BellStateType::PhiPlus);
    let fidelity = bell_state.fidelity_with_ideal();
    
    // Perfect Bell state should have fidelity close to 1
    assert!(fidelity > 0.99);
}

#[test]
fn test_measurement_analysis() {
    let bell_state = BellState::new(BellStateType::PhiPlus);
    let correlations = bell_state.analyze_measurements(100);
    
    // Should have correlations for all basis combinations
    assert!(correlations.contains_key("Z-Z"));
    assert!(correlations.contains_key("X-X"));
    assert!(correlations.contains_key("Z-X"));
    assert!(correlations.contains_key("X-Z"));
    
    // Z-Z correlation should be high for PhiPlus
    assert!(correlations["Z-Z"].abs() > 0.5);
}

#[test]
fn test_bell_state_types() {
    let types = [
        BellStateType::PhiPlus,
        BellStateType::PhiMinus,
        BellStateType::PsiPlus,
        BellStateType::PsiMinus,
    ];
    
    for state_type in types.iter() {
        let bell_state = BellState::new(*state_type);
        assert_eq!(bell_state.state_type, *state_type);
    }
}
