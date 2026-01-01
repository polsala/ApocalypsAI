use nightly_quantum_entanglement_checker::quantum::*;

#[test]
fn test_quantum_state_normalization() {
    let state = QuantumState::new();
    let norm = state.amplitude_00.powi(2) + state.amplitude_01.powi(2) + 
               state.amplitude_10.powi(2) + state.amplitude_11.powi(2);
    
    // Check that the state is normalized (within floating point precision)
    assert!((norm - 1.0).abs() < 1e-10);
}

#[test]
fn test_fidelity_calculation() {
    let mut state_a = QuantumState::new();
    let mut state_b = QuantumState::new();
    
    // Set identical states for perfect fidelity
    state_a.amplitude_00 = 1.0;
    state_a.amplitude_01 = 0.0;
    state_a.amplitude_10 = 0.0;
    state_a.amplitude_11 = 0.0;
    
    state_b.amplitude_00 = 1.0;
    state_b.amplitude_01 = 0.0;
    state_b.amplitude_10 = 0.0;
    state_b.amplitude_11 = 0.0;
    
    let fidelity = state_a.fidelity_with(&state_b);
    assert!((fidelity - 1.0).abs() < 1e-10);
}

#[test]
fn test_bell_state_determination() {
    let mut state = QuantumState::new();
    
    // Test |Ψ⁻⟩ state
    state.amplitude_01 = 1.0 / 2f64.sqrt();
    state.amplitude_10 = -1.0 / 2f64.sqrt();
    state.amplitude_00 = 0.0;
    state.amplitude_11 = 0.0;
    
    let bell_state = state.determine_bell_state();
    assert!(matches!(bell_state, BellState::PsiMinus));
}

#[test]
fn test_decoherence_risk_calculation() {
    let mut checker = QuantumEntanglementChecker::new();
    
    // Test with perfect fidelity
    let risk = checker.calculate_decoherence_risk("node-a", "node-b", 1.0);
    assert!(matches!(risk, DecoherenceRisk::Low));
    
    // Test with poor fidelity
    let risk = checker.calculate_decoherence_risk("node-a", "node-b", 0.1);
    assert!(matches!(risk, DecoherenceRisk::Critical));
}

#[test]
fn test_entanglement_verification() {
    let mut checker = QuantumEntanglementChecker::new();
    
    let result = checker.verify_entanglement("service-a", "service-b", 0.8);
    
    // Check that all fields are populated
    assert!(result.fidelity >= 0.0 && result.fidelity <= 1.0);
    assert!(result.correlation >= 0.0 && result.correlation <= 1.0);
    assert!(result.measurement_correlation >= 0.0 && result.measurement_correlation <= 1.0);
    
    // Check that recommended action is not empty
    assert!(!result.recommended_action.is_empty());
}

#[test]
fn test_bell_state_display() {
    let psi_minus = BellState::PsiMinus;
    assert_eq!(format!("{}", psi_minus), "|Ψ⁻⟩ = (|01⟩ - |10⟩)/√2");
    
    let phi_plus = BellState::PhiPlus;
    assert_eq!(format!("{}", phi_plus), "|Φ⁺⟩ = (|00⟩ + |11⟩)/√2");
}

#[test]
fn test_decoherence_risk_display() {
    assert_eq!(format!("{}", DecoherenceRisk::Low), "LOW");
    assert_eq!(format!("{}", DecoherenceRisk::Critical), "CRITICAL");
}
