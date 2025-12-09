use super::*;
use rand::rngs::StdRng;
use rand::SeedableRng;

#[test]
fn test_complex_magnitude() {
    let c = Complex::new(3.0, 4.0);
    assert_eq!(c.magnitude_squared(), 25.0);
    assert_eq!(c.magnitude(), 5.0);
}

#[test]
fn test_complex_arithmetic() {
    let c1 = Complex::new(1.0, 2.0);
    let c2 = Complex::new(3.0, 4.0);
    
    let sum = c1.add(&c2);
    assert_eq!(sum.real, 4.0);
    assert_eq!(sum.imag, 6.0);
    
    let product = c1.multiply(&c2);
    assert_eq!(product.real, -5.0); // (1*3 - 2*4)
    assert_eq!(product.imag, 10.0); // (1*4 + 2*3)
}

#[test]
fn test_quantum_state_creation() {
    let mut rng = StdRng::seed_from_u64(42);
    let state = QuantumState::new_random(&mut rng);
    
    // After normalization, probabilities should sum to 1
    let p0 = state.probability_0();
    let p1 = state.probability_1();
    assert!((p0 + p1 - 1.0).abs() < 1e-10);
}

#[test]
fn test_quantum_state_normalization() {
    let mut state = QuantumState {
        amplitude_0: Complex::new(2.0, 0.0),
        amplitude_1: Complex::new(2.0, 0.0),
    };
    
    state.normalize();
    
    let p0 = state.probability_0();
    let p1 = state.probability_1();
    assert!((p0 + p1 - 1.0).abs() < 1e-10);
    assert!((p0 - 0.5).abs() < 1e-10);
    assert!((p1 - 0.5).abs() < 1e-10);
}

#[test]
fn test_entangled_pair_creation() {
    let mut rng = StdRng::seed_from_u64(42);
    let (state_a, state_b) = create_entangled_pair(&mut rng);
    
    // Both states should be normalized
    assert!((state_a.probability_0() + state_a.probability_1() - 1.0).abs() < 1e-10);
    assert!((state_b.probability_0() + state_b.probability_1() - 1.0).abs() < 1e-10);
}

#[test]
fn test_correlation_calculation() {
    // Perfect correlation
    let measurements = vec![0, 0, 1, 1, 0, 0];
    let correlation = calculate_correlation(&measurements);
    assert_eq!(correlation, 1.0);
    
    // No correlation
    let measurements = vec![0, 1, 0, 1, 0, 1];
    let correlation = calculate_correlation(&measurements);
    assert_eq!(correlation, 0.0);
}

#[test]
fn test_bell_inequality_violation() {
    // Test with maximally entangled state
    let (s, violates) = verify_bell_inequality(0.707, 0.707, 1000);
    
    // Bell parameter should be close to 2.828 (quantum prediction)
    assert!(s.abs() > 2.0); // Should violate classical limit
    assert!(violates);
}

#[test]
fn test_decoherence_detection() {
    // Short duration test
    let (has_decohered, coherence) = detect_decoherence(0.1, 1);
    
    // Coherence should be high for short duration
    assert!(coherence > 0.9);
    assert!(!has_decohered);
}

#[test]
fn test_benchmark_performance() {
    // Quick benchmark test
    let (ops_per_sec, avg_correlation) = benchmark_entanglement(2, 100);
    
    // Should complete quickly and maintain correlation
    assert!(ops_per_sec > 0.0);
    assert!(avg_correlation > 0.5); // Should maintain some correlation
}

#[test]
fn test_deterministic_behavior_with_seed() {
    // Test that using the same seed produces consistent results
    let (is_entangled_1, correlation_1) = check_entanglement(3, 100, Some(42));
    let (is_entangled_2, correlation_2) = check_entanglement(3, 100, Some(42));
    
    assert_eq!(is_entangled_1, is_entangled_2);
    assert!((correlation_1 - correlation_2).abs() < 1e-10);
}

#[test]
fn test_edge_cases() {
    // Test with minimum values
    let (is_entangled, correlation) = check_entanglement(1, 1, Some(42));
    assert!(correlation >= 0.0 && correlation <= 1.0);
    
    // Test Bell inequality with edge case coefficients
    let (s, _) = verify_bell_inequality(1.0, 0.0, 100);
    assert!(s.is_finite());
    
    // Test decoherence with minimum duration
    let (has_decohered, _) = detect_decoherence(0.5, 0);
    assert!(!has_decohered);
}

#[test]
fn test_quantum_state_measurements() {
    let mut rng = StdRng::seed_from_u64(42);
    let state = QuantumState::new_random(&mut rng);
    
    // Measure multiple times and check statistics
    let mut counts = [0, 0];
    for _ in 0..1000 {
        let result = state.measure(&mut rng);
        counts[result] += 1;
    }
    
    let p0_estimated = counts[0] as f64 / 1000.0;
    let p0_expected = state.probability_0();
    
    // Should be close (within 3 standard deviations for binomial distribution)
    let std_dev = (p0_expected * (1.0 - p0_expected) / 1000.0).sqrt();
    assert!((p0_estimated - p0_expected).abs() < 3.0 * std_dev);
}

#[test]
fn test_complex_zero_handling() {
    let mut state = QuantumState {
        amplitude_0: Complex::new(0.0, 0.0),
        amplitude_1: Complex::new(0.0, 0.0),
    };
    
    // Normalization should handle zero case gracefully
    state.normalize();
    
    // Should not crash and maintain valid state
    let p0 = state.probability_0();
    let p1 = state.probability_1();
    assert!(p0.is_finite() && p1.is_finite());
}

#[test]
fn test_concurrent_benchmark_safety() {
    // Test that concurrent execution doesn't cause data races
    let num_threads = 4;
    let operations_per_thread = 100;
    
    let mut handles = Vec::new();
    
    for _ in 0..num_threads {
        handles.push(std::thread::spawn(move || {
            benchmark_entanglement(1, operations_per_thread);
        }));
    }
    
    for handle in handles {
        handle.join().unwrap();
    }
    
    // If we reach here without panicking, the test passes
    assert!(true);
}

// Mock rationale: These tests use deterministic seeds and mathematical
// properties to verify quantum simulation correctness without external
// dependencies. The mock quantum states follow predictable probability
// distributions that can be statistically verified.
