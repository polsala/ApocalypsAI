use nightly_quantum_entanglement_checker::{BellState, QuantumState, Complex};
use rand::SeedableRng;
use rand::rngs::StdRng;

#[test]
fn test_bell_state_strings() {
    assert_eq!(BellState::PhiPlus.to_string(), "|Φ⁺⟩ (Phi Plus)");
    assert_eq!(BellState::PhiMinus.to_string(), "|Φ⁻⟩ (Phi Minus)");
    assert_eq!(BellState::PsiPlus.to_string(), "|Ψ⁺⟩ (Psi Plus)");
    assert_eq!(BellState::PsiMinus.to_string(), "|Ψ⁻⟩ (Psi Minus)");
}

#[test]
fn test_bell_state_notation() {
    assert_eq!(BellState::PhiPlus.notation(), "|Φ⁺⟩ = (|00⟩ + |11⟩)/√2");
    assert_eq!(BellState::PhiMinus.notation(), "|Φ⁻⟩ = (|00⟩ - |11⟩)/√2");
    assert_eq!(BellState::PsiPlus.notation(), "|Ψ⁺⟩ = (|01⟩ + |10⟩)/√2");
    assert_eq!(BellState::PsiMinus.notation(), "|Ψ⁻⟩ = (|01⟩ - |10⟩)/√2");
}

#[test]
fn test_complex_operations() {
    let mut c = Complex::new(3.0, 4.0);
    assert_eq!(c.magnitude_squared(), 25.0);
    
    c.normalize(5.0);
    assert!((c.real - 0.6).abs() < 1e-10);
    assert!((c.imag - 0.8).abs() < 1e-10);
}

#[test]
fn test_quantum_state_creation() {
    let phi_plus = QuantumState::phi_plus();
    let phi_minus = QuantumState::phi_minus();
    let psi_plus = QuantumState::psi_plus();
    let psi_minus = QuantumState::psi_minus();

    // Check that states are properly normalized
    let norm_phi_plus = phi_plus.amplitude_00.magnitude_squared() + phi_plus.amplitude_11.magnitude_squared();
    let norm_phi_minus = phi_minus.amplitude_00.magnitude_squared() + phi_minus.amplitude_11.magnitude_squared();
    let norm_psi_plus = psi_plus.amplitude_01.magnitude_squared() + psi_plus.amplitude_10.magnitude_squared();
    let norm_psi_minus = psi_minus.amplitude_01.magnitude_squared() + psi_minus.amplitude_10.magnitude_squared();

    assert!((norm_phi_plus - 1.0).abs() < 1e-10);
    assert!((norm_phi_minus - 1.0).abs() < 1e-10);
    assert!((norm_psi_plus - 1.0).abs() < 1e-10);
    assert!((norm_psi_minus - 1.0).abs() < 1e-10);
}

#[test]
fn test_quantum_state_measurement() {
    let mut rng = StdRng::seed_from_u64(42);
    let state = QuantumState::phi_plus();

    // Measure the state multiple times
    let mut phi_plus_count = 0;
    let mut phi_minus_count = 0;
    let mut psi_plus_count = 0;
    let mut psi_minus_count = 0;

    for _ in 0..1000 {
        let result = state.measure(&mut rng);
        match result {
            BellState::PhiPlus => phi_plus_count += 1,
            BellState::PhiMinus => phi_minus_count += 1,
            BellState::PsiPlus => psi_plus_count += 1,
            BellState::PsiMinus => psi_minus_count += 1,
        }
    }

    // For |Φ⁺⟩ state, we should mostly get |Φ⁺⟩ measurements
    // (with some randomness due to the simulation)
    assert!(phi_plus_count > 200);
    assert!(phi_plus_count > phi_minus_count);
    assert!(phi_plus_count > psi_plus_count);
    assert!(phi_plus_count > psi_minus_count);
}

#[test]
fn test_hadamard_gate() {
    let mut state = QuantumState::phi_plus();
    state.hadamard_first_qubit();

    // After Hadamard on first qubit, |Φ⁺⟩ should become |+0⟩ + |+1⟩
    // This is a simplified test - in reality we'd need more complex verification
    let probabilities = state.measurement_probabilities();
    let total_prob = probabilities.0 + probabilities.1 + probabilities.2 + probabilities.3;
    assert!((total_prob - 1.0).abs() < 1e-10);
}

#[test]
fn test_random_entangled_state() {
    let mut rng = StdRng::seed_from_u64(123);
    let state = QuantumState::random_entangled(&mut rng);

    // Check that the state is normalized
    let probabilities = state.measurement_probabilities();
    let total_prob = probabilities.0 + probabilities.1 + probabilities.2 + probabilities.3;
    assert!((total_prob - 1.0).abs() < 1e-10);
}

#[test]
fn test_bell_state_theoretical_probability() {
    assert_eq!(BellState::theoretical_probability(), 0.25);
}
