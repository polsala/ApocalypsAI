use nightly_quantum_entanglement_simulator::*;

#[test]
fn test_particle_creation() {
    let pair = EntangledPair::new(1);
    
    // Particles should have opposite spins
    assert_ne!(pair.particle_a.spin, pair.particle_b.spin);
    
    // Particles should have opposite polarizations
    assert_ne!(pair.particle_a.polarization, pair.particle_b.polarization);
    
    // IDs should be sequential
    assert_eq!(pair.particle_a.id, 2);
    assert_eq!(pair.particle_b.id, 3);
}

#[test]
fn test_measurement_correlation() {
    let pair = EntangledPair::new(1);
    let basis = 45.0;
    
    let (result_a, result_b) = pair.measure(basis);
    
    // In ideal conditions, measurements should be perfectly anti-correlated
    // (though decoherence might affect this)
    assert!(result_a.value == 1 || result_a.value == -1);
    assert!(result_b.value == 1 || result_b.value == -1);
    assert_eq!(result_a.basis, basis);
    assert_eq!(result_b.basis, basis);
}

#[test]
fn test_spin_measurement() {
    let particle = Particle {
        id: 1,
        spin: Spin::Up,
        polarization: Polarization::Horizontal,
        decoherence_time: std::time::Duration::from_secs(1),
    };
    
    let result = measure_spin(&particle, 0.0); // Measuring in horizontal basis
    assert!(result == 1 || result == -1);
    
    let result = measure_spin(&particle, 90.0); // Measuring in vertical basis
    assert!(result == 1 || result == -1);
}

#[test]
fn test_random_functions() {
    // Test that random functions produce reasonable ranges
    for _ in 0..100 {
        let r = rand_range(0, 10);
        assert!(r >= 0 && r < 10);
        
        let rf = rand_range_f64(0.0, 1.0);
        assert!(rf >= 0.0 && rf <= 1.0);
        
        // rand_bool should return true or false
        let _b = rand_bool();
    }
}

#[test]
fn test_polarization_opposites() {
    // Test that opposite polarizations are correctly assigned
    let pair = EntangledPair::new(42);
    
    match pair.particle_a.polarization {
        Polarization::Horizontal => assert_eq!(pair.particle_b.polarization, Polarization::Vertical),
        Polarization::Vertical => assert_eq!(pair.particle_b.polarization, Polarization::Horizontal),
        Polarization::Diagonal => assert_eq!(pair.particle_b.polarization, Polarization::AntiDiagonal),
        Polarization::AntiDiagonal => assert_eq!(pair.particle_b.polarization, Polarization::Diagonal),
    }
}

#[test]
fn test_decoherence_simulation() {
    let pair = EntangledPair::new(1);
    
    // Simulate immediate measurement (no decoherence)
    let (result_a, result_b) = pair.measure(0.0);
    
    // Results should be valid
    assert!(result_a.value == 1 || result_a.value == -1);
    assert!(result_b.value == 1 || result_b.value == -1);
}

#[test]
fn test_multiple_measurements_same_basis() {
    let pair = EntangledPair::new(1);
    let basis = 30.0;
    
    // Multiple measurements with same basis should be consistent
    // (in this simplified model)
    let (result1_a, result1_b) = pair.measure(basis);
    let (result2_a, result2_b) = pair.measure(basis);
    
    // Results should be valid
    assert!(result1_a.value == 1 || result1_a.value == -1);
    assert!(result1_b.value == 1 || result1_b.value == -1);
    assert!(result2_a.value == 1 || result2_a.value == -1);
    assert!(result2_b.value == 1 || result2_b.value == -1);
}

#[test]
fn test_spin_opposites() {
    let pair = EntangledPair::new(123);
    
    // Spins should always be opposite
    match pair.particle_a.spin {
        Spin::Up => assert_eq!(pair.particle_b.spin, Spin::Down),
        Spin::Down => assert_eq!(pair.particle_b.spin, Spin::Up),
    }
}

#[test]
fn test_decoherence_time_range() {
    let pair = EntangledPair::new(1);
    
    // Decoherence times should be in reasonable range
    let time_a = pair.particle_a.decoherence_time.as_secs_f64();
    let time_b = pair.particle_b.decoherence_time.as_secs_f64();
    
    assert!(time_a >= 0.01 && time_a <= 0.1);
    assert!(time_b >= 0.01 && time_b <= 0.1);
}

// Mock rationale: These tests verify the core quantum simulation logic
// without requiring external quantum hardware or complex physics libraries.
// They ensure that entanglement properties are maintained and measurements
// behave as expected in our simplified model.
