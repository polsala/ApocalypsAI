use quantum_entanglement_checker::*;

#[test]
fn test_complex_operations() {
    let c1 = Complex::new(1.0, 2.0);
    let c2 = Complex::new(3.0, 4.0);
    
    // Test conjugate
    let conj = c1.conjugate();
    assert_eq!(conj.real, 1.0);
    assert_eq!(conj.imag, -2.0);
    
    // Test multiplication
    let product = c1.multiply(&c2);
    assert!((product.real - (-5.0)).abs() < 1e-10);
    assert!((product.imag - 10.0).abs() < 1e-10);
    
    // Test magnitude squared
    let mag_sq = c1.magnitude_squared();
    assert!((mag_sq - 5.0).abs() < 1e-10);
}

#[test]
fn test_quantum_state_creation() {
    let state = QuantumState::new_random(2);
    
    // Should have 2^2 = 4 amplitudes
    assert_eq!(state.amplitudes.len(), 4);
    
    // Should be normalized
    let norm_sq: f64 = state.amplitudes.iter().map(|a| a.magnitude_squared()).sum();
    assert!((norm_sq - 1.0).abs() < 1e-10);
}

#[test]
fn test_quantum_state_normalization() {
    let mut amplitudes = vec![
        Complex::new(1.0, 0.0),
        Complex::new(2.0, 0.0),
        Complex::new(3.0, 0.0),
        Complex::new(4.0, 0.0),
    ];
    
    QuantumState::normalize(&mut amplitudes);
    
    let norm_sq: f64 = amplitudes.iter().map(|a| a.magnitude_squared()).sum();
    assert!((norm_sq - 1.0).abs() < 1e-10);
}

#[test]
fn test_fidelity_calculation() {
    let state1 = QuantumState::new_random(2);
    let state2 = QuantumState::new_random(2);
    
    let fidelity = state1.calculate_fidelity(&state2);
    
    // Fidelity should be between 0 and 1
    assert!(fidelity >= 0.0 && fidelity <= 1.0);
}

#[test]
fn test_fidelity_identical_states() {
    let state1 = QuantumState::new_random(2);
    let state2 = state1.clone();
    
    let fidelity = state1.calculate_fidelity(&state2);
    
    // Identical states should have fidelity close to 1
    assert!(fidelity > 0.99);
}

#[test]
fn test_measurements() {
    let state = QuantumState::new_random(2);
    let measurements = state.measure_bell_state(100);
    
    // Should have 100 measurements
    assert_eq!(measurements.len(), 100);
    
    // All measurements should be between 0 and 1
    for measurement in measurements {
        assert!(measurement >= 0.0 && measurement <= 1.0);
    }
}

#[test]
fn test_analyze_measurements() {
    let measurements = vec![0.25, 0.25, 0.25, 0.25];
    let (mean, std_dev) = analyze_measurements(&measurements);
    
    // Mean should be 0.25
    assert!((mean - 0.25).abs() < 1e-10);
    
    // Standard deviation should be 0 for identical values
    assert!(std_dev < 1e-10);
}

#[test]
fn test_complex_magnitude_edge_cases() {
    // Test zero complex number
    let zero = Complex::new(0.0, 0.0);
    assert_eq!(zero.magnitude_squared(), 0.0);
    
    // Test purely real number
    let real = Complex::new(5.0, 0.0);
    assert_eq!(real.magnitude_squared(), 25.0);
    
    // Test purely imaginary number
    let imag = Complex::new(0.0, 3.0);
    assert_eq!(imag.magnitude_squared(), 9.0);
}

#[test]
fn test_quantum_state_edge_cases() {
    // Test single particle state
    let state = QuantumState::new_random(1);
    assert_eq!(state.amplitudes.len(), 2);
    
    // Test larger state
    let state = QuantumState::new_random(4);
    assert_eq!(state.amplitudes.len(), 16);
}

#[test]
fn test_fidelity_different_sizes() {
    let state1 = QuantumState::new_random(2);
    let state2 = QuantumState::new_random(3);
    
    let fidelity = state1.calculate_fidelity(&state2);
    
    // Different sized states should have zero fidelity
    assert_eq!(fidelity, 0.0);
}

#[test]
fn test_measurement_consistency() {
    let state = QuantumState::new_random(2);
    
    // Multiple measurement runs should produce valid results
    for _ in 0..5 {
        let measurements = state.measure_bell_state(50);
        assert_eq!(measurements.len(), 50);
        for measurement in measurements {
            assert!(measurement >= 0.0 && measurement <= 1.0);
        }
    }
}
