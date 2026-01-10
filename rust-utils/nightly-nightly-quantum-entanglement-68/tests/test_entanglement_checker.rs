use nightly_quantum_entanglement_checker::entanglement_checker::{EntanglementChecker, EntanglementResult};

#[test]
fn test_check_entanglement_identical_states() {
    let mut checker = EntanglementChecker::new();
    let state_a = vec![1.0, 0.0];
    let state_b = vec![1.0, 0.0];
    
    // Mock rationale: Verify entanglement check for identical states
    let result = checker.check_entanglement(&state_a, &state_b);
    assert!(result.is_entangled);
    assert_eq!(result.entanglement_score, 1.0);
    assert_eq!(result.bell_state_fidelity, 1.0);
}

#[test]
fn test_check_entanglement_different_sizes() {
    let mut checker = EntanglementChecker::new();
    let state_a = vec![1.0, 0.0];
    let state_b = vec![1.0, 0.0, 0.0];
    
    // Mock rationale: Verify entanglement check rejects different sized states
    let result = checker.check_entanglement(&state_a, &state_b);
    assert!(!result.is_entangled);
    assert_eq!(result.entanglement_score, 0.0);
    assert_eq!(result.bell_state_fidelity, 0.0);
}

#[test]
fn test_check_entanglement_orthogonal_states() {
    let mut checker = EntanglementChecker::new();
    let state_a = vec![1.0, 0.0];
    let state_b = vec![0.0, 1.0];
    
    // Mock rationale: Verify entanglement check for orthogonal states
    let result = checker.check_entanglement(&state_a, &state_b);
    assert!(!result.is_entangled);
    assert_eq!(result.entanglement_score, 0.0);
    assert_eq!(result.bell_state_fidelity, 0.0);
}
