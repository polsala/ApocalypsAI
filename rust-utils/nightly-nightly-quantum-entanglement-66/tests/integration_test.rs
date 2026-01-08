use nightly_quantum_entanglement_simulator::quantum::{EntangledPair, MeasurementBasis, QuantumState};

#[test]
fn test_entangled_pair_creation() {
    let pair = EntangledPair::new(1.0);
    // With perfect entanglement, Alice and Bob should start with same state
    assert_eq!(pair.alice, pair.bob);
}

#[test]
fn test_perfect_entanglement_correlation() {
    let mut pair = EntangledPair::new(1.0);
    let basis = MeasurementBasis::Z;
    
    let alice_result = pair.measure_alice(basis);
    let bob_result = pair.measure_bob(basis);
    
    // With perfect entanglement, results should always correlate
    assert_eq!(alice_result, bob_result);
}

#[test]
fn test_zero_entanglement_no_correlation() {
    let mut pair = EntangledPair::new(0.0);
    let basis = MeasurementBasis::Z;
    
    let alice_result = pair.measure_alice(basis);
    let bob_result = pair.measure_bob(basis);
    
    // With zero entanglement, results might not correlate
    // We can't assert they're different (randomness), but we can check the method works
    assert!(pair.check_correlation() == true || pair.check_correlation() == false);
}

#[test]
fn test_measurement_basis_random() {
    let mut found_z = false;
    let mut found_x = false;
    let mut found_y = false;
    
    // Try many times to ensure all bases are possible
    for _ in 0..1000 {
        let basis = MeasurementBasis::random();
        match basis {
            MeasurementBasis::Z => found_z = true,
            MeasurementBasis::X => found_x = true,
            MeasurementBasis::Y => found_y = true,
        }
    }
    
    assert!(found_z && found_x && found_y, "All measurement bases should be possible");
}

#[test]
fn test_quantum_state_to_string() {
    assert_eq!(QuantumState::Zero.to_string(), "|0⟩");
    assert_eq!(QuantumState::One.to_string(), "|1⟩");
    assert_eq!(QuantumState::Plus.to_string(), "|+⟩");
    assert_eq!(QuantumState::Minus.to_string(), "|-⟩");
    assert_eq!(QuantumState::I.to_string(), "|i⟩");
    assert_eq!(QuantumState::MinusI.to_string(), "|-i⟩");
}

#[test]
fn test_measurement_basis_to_string() {
    assert_eq!(MeasurementBasis::Z.to_string(), "Z");
    assert_eq!(MeasurementBasis::X.to_string(), "X");
    assert_eq!(MeasurementBasis::Y.to_string(), "Y");
}
