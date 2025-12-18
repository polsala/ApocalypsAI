use nightly_quantum_entanglement_checker::*;
use std::collections::HashMap;

#[test]
fn test_quantum_simulator_creation() {
    let simulator = QuantumSimulator::new(4, 1000);
    assert_eq!(simulator.num_nodes, 4);
    assert_eq!(simulator.num_measurements, 1000);
}

#[test]
fn test_simulate_entanglement_returns_correct_pairs() {
    let simulator = QuantumSimulator::new(3, 10);
    let measurements = simulator.simulate_entanglement();
    
    // For 3 nodes, we should have 3 pairs: (0,1), (0,2), (1,2)
    assert_eq!(measurements.len(), 3);
    assert!(measurements.contains_key(&(0, 1)));
    assert!(measurements.contains_key(&(0, 2)));
    assert!(measurements.contains_key(&(1, 2)));
}

#[test]
fn test_measurement_count_consistency() {
    let simulator = QuantumSimulator::new(3, 50);
    let measurements = simulator.simulate_entanglement();
    
    for ((node1, node2), measurement_pairs) in measurements.iter() {
        assert_eq!(measurement_pairs.len(), 50, "Pair ({}, {}) has wrong measurement count", node1, node2);
    }
}

#[test]
fn test_measurement_outcomes_valid() {
    let simulator = QuantumSimulator::new(2, 100);
    let measurements = simulator.simulate_entanglement();
    
    let measurement_pairs = measurements.get(&(0, 1)).unwrap();
    
    for (outcome1, outcome2) in measurement_pairs {
        // Valid outcomes are Zero or One
        assert!(matches!(outcome1, MeasurementOutcome::Zero | MeasurementOutcome::One));
        assert!(matches!(outcome2, MeasurementOutcome::Zero | MeasurementOutcome::One));
    }
}

#[test]
fn test_measurement_basis_angle_difference() {
    let basis1 = MeasurementBasis::new(0.0);
    let basis2 = MeasurementBasis::new(std::f64::consts::PI / 2.0);
    
    let diff = basis1.angle_difference(&basis2);
    assert!((diff - std::f64::consts::PI / 2.0).abs() < 1e-10);
    
    // Test wrap-around
    let basis3 = MeasurementBasis::new(std::f64::consts::PI * 0.75);
    let basis4 = MeasurementBasis::new(std::f64::consts::PI * 0.25);
    let diff2 = basis3.angle_difference(&basis4);
    assert!((diff2 - std::f64::consts::PI / 2.0).abs() < 1e-10);
}

#[test]
fn test_fidelity_calculator_creation() {
    let calculator = FidelityCalculator::new(0.8);
    assert_eq!(calculator.fidelity_threshold, 0.8);
}

#[test]
fn test_fidelity_calculation_perfect_correlation() {
    let calculator = FidelityCalculator::new(0.8);
    
    // Perfect correlation: all measurements are the same
    let measurements = vec![
        (MeasurementOutcome::Zero, MeasurementOutcome::Zero);
        50
    ];
    measurements.extend(vec![
        (MeasurementOutcome::One, MeasurementOutcome::One);
        50
    ]);
    
    let fidelity = calculator.calculate_pair_fidelity(&measurements);
    assert!(fidelity > 0.95, "Perfect correlation should give high fidelity, got {}", fidelity);
}

#[test]
fn test_fidelity_calculation_no_correlation() {
    let calculator = FidelityCalculator::new(0.8);
    
    // No correlation: random measurements
    let measurements = vec![
        (MeasurementOutcome::Zero, MeasurementOutcome::One),
        (MeasurementOutcome::One, MeasurementOutcome::Zero),
        (MeasurementOutcome::Zero, MeasurementOutcome::Zero),
        (MeasurementOutcome::One, MeasurementOutcome::One),
    ].repeat(25);
    
    let fidelity = calculator.calculate_pair_fidelity(&measurements);
    assert!(fidelity < 0.6, "No correlation should give low fidelity, got {}", fidelity);
}

#[test]
fn test_is_entangled_threshold() {
    let calculator = FidelityCalculator::new(0.8);
    
    assert!(calculator.is_entangled(0.9));
    assert!(calculator.is_entangled(0.8));
    assert!(!calculator.is_entangled(0.79));
    assert!(!calculator.is_entangled(0.5));
}

#[test]
fn test_empty_measurements_fidelity() {
    let calculator = FidelityCalculator::new(0.8);
    let measurements = vec![];
    let fidelity = calculator.calculate_pair_fidelity(&measurements);
    assert_eq!(fidelity, 0.0);
}

#[test]
fn test_measurement_outcome_conversions() {
    assert_eq!(MeasurementOutcome::Zero.to_i32(), 0);
    assert_eq!(MeasurementOutcome::One.to_i32(), 1);
    
    assert_eq!(MeasurementOutcome::Zero.to_f64(), -1.0);
    assert_eq!(MeasurementOutcome::One.to_f64(), 1.0);
}
