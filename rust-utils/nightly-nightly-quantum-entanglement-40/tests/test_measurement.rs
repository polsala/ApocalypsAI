use nightly_quantum_entanglement_checker::{MeasurementBasis, QuantumMeasurement, BellState};
use rand::SeedableRng;
use rand::rngs::StdRng;

#[test]
fn test_measurement_basis_display() {
    assert_eq!(format!("{}", MeasurementBasis::Computational), "Computational");
    assert_eq!(format!("{}", MeasurementBasis::Hadamard), "Hadamard");
}

#[test]
fn test_quantum_measurement_creation() {
    let measurement = QuantumMeasurement::new(2, MeasurementBasis::Computational);
    assert_eq!(measurement.qubits, 2);
}

#[test]
fn test_single_measurement_computational() {
    let mut rng = StdRng::seed_from_u64(42);
    let measurement = QuantumMeasurement::new(2, MeasurementBasis::Computational);

    let result = measurement.measure(&mut rng);
    // Should return one of the four Bell states
    match result {
        BellState::PhiPlus | BellState::PhiMinus | BellState::PsiPlus | BellState::PsiMinus => {},
        _ => panic!("Unexpected Bell state result"),
    }
}

#[test]
fn test_single_measurement_hadamard() {
    let mut rng = StdRng::seed_from_u64(42);
    let measurement = QuantumMeasurement::new(2, MeasurementBasis::Hadamard);

    let result = measurement.measure(&mut rng);
    // Should return one of the four Bell states
    match result {
        BellState::PhiPlus | BellState::PhiMinus | BellState::PsiPlus | BellState::PsiMinus => {},
        _ => panic!("Unexpected Bell state result"),
    }
}

#[test]
fn test_multiple_measurements() {
    let mut rng = StdRng::seed_from_u64(42);
    let measurement = QuantumMeasurement::new(2, MeasurementBasis::Computational);

    let (phi_plus, phi_minus, psi_plus, psi_minus) = measurement.measure_multiple(&mut rng, 1000);

    // Should have measured all states
    assert!(phi_plus + phi_minus + psi_plus + psi_minus == 1000);
    assert!(phi_plus > 0);
    assert!(phi_minus > 0);
    assert!(psi_plus > 0);
    assert!(psi_minus > 0);
}

#[test]
fn test_measurement_with_noise() {
    let mut rng = StdRng::seed_from_u64(42);
    let measurement = QuantumMeasurement::new(2, MeasurementBasis::Computational);

    // Test with 100% noise (should be completely random)
    let result = measurement.measure_with_noise(&mut rng, 1.0);
    match result {
        BellState::PhiPlus | BellState::PhiMinus | BellState::PsiPlus | BellState::PsiMinus => {},
        _ => panic!("Unexpected Bell state result"),
    }
}

#[test]
fn test_fidelity_calculation() {
    let measurement = QuantumMeasurement::new(2, MeasurementBasis::Computational);

    // Perfect Bell state measurements
    let fidelity = measurement.calculate_fidelity((250, 250, 250, 250), 1000);
    assert!(fidelity > 0.9);

    // Completely biased measurements
    let fidelity = measurement.calculate_fidelity((1000, 0, 0, 0), 1000);
    assert!(fidelity < 0.5);
}

#[test]
fn test_basis_description() {
    let computational = QuantumMeasurement::new(2, MeasurementBasis::Computational);
    assert!(computational.basis_description().contains("Computational"));
    assert!(computational.basis_description().contains("|0⟩"));
    assert!(computational.basis_description().contains("|1⟩"));

    let hadamard = QuantumMeasurement::new(2, MeasurementBasis::Hadamard);
    assert!(hadamard.basis_description().contains("Hadamard"));
    assert!(hadamard.basis_description().contains("|+⟩"));
    assert!(hadamard.basis_description().contains("|-⟩"));
}

#[test]
fn test_decoherence_simulation() {
    let mut rng = StdRng::seed_from_u64(42);
    let measurement = QuantumMeasurement::new(2, MeasurementBasis::Computational);

    // Test with 50% decoherence
    let results = measurement.simulate_decoherence(&mut rng, 0.5, 100);
    assert_eq!(results.len(), 100);

    // All results should be valid Bell states
    for result in results {
        match result {
            BellState::PhiPlus | BellState::PhiMinus | BellState::PsiPlus | BellState::PsiMinus => {},
            _ => panic!("Unexpected Bell state result"),
        }
    }
}

#[test]
fn test_measurement_statistics() {
    let mut rng = StdRng::seed_from_u64(42);
    let measurement = QuantumMeasurement::new(2, MeasurementBasis::Computational);

    // Perform many measurements to check statistical properties
    let (phi_plus, phi_minus, psi_plus, psi_minus) = measurement.measure_multiple(&mut rng, 10000);

    let total = phi_plus + phi_minus + psi_plus + psi_minus;
    assert_eq!(total, 10000);

    // In a fair simulation, all states should be roughly equally likely
    let expected = 2500;
    let tolerance = 200; // Allow some variation due to randomness

    assert!((phi_plus as i32 - expected as i32).abs() < tolerance);
    assert!((phi_minus as i32 - expected as i32).abs() < tolerance);
    assert!((psi_plus as i32 - expected as i32).abs() < tolerance);
    assert!((psi_minus as i32 - expected as i32).abs() < tolerance);
}
