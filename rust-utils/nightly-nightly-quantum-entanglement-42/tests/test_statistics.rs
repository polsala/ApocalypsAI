use nightly_quantum_entanglement_checker::statistics::Statistics;

#[test]
fn test_mean_calculation() {
    let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    let mean = Statistics::mean(&values);
    assert_eq!(mean, 3.0);
}

#[test]
fn test_mean_empty() {
    let values = vec![];
    let mean = Statistics::mean(&values);
    assert_eq!(mean, 0.0);
}

#[test]
fn test_variance_calculation() {
    let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    let variance = Statistics::variance(&values);
    let expected = 2.0; // ((1-3)² + (2-3)² + (3-3)² + (4-3)² + (5-3)²) / 5
    assert!((variance - expected).abs() < 1e-10);
}

#[test]
fn test_standard_deviation() {
    let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    let std_dev = Statistics::standard_deviation(&values);
    let variance = Statistics::variance(&values);
    assert!((std_dev - variance.sqrt()).abs() < 1e-10);
}

#[test]
fn test_correlation_calculation() {
    let x = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    let y = vec![2.0, 4.0, 6.0, 8.0, 10.0]; // Perfect positive correlation
    let corr = Statistics::correlation(&x, &y);
    assert!((corr - 1.0).abs() < 1e-10);
}

#[test]
fn test_correlation_negative() {
    let x = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    let y = vec![10.0, 8.0, 6.0, 4.0, 2.0]; // Perfect negative correlation
    let corr = Statistics::correlation(&x, &y);
    assert!((corr + 1.0).abs() < 1e-10);
}

#[test]
fn test_correlation_zero() {
    let x = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    let y = vec![5.0, 5.0, 5.0, 5.0, 5.0]; // No correlation
    let corr = Statistics::correlation(&x, &y);
    assert!((corr - 0.0).abs() < 1e-10);
}

#[test]
fn test_confidence_interval() {
    let values = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    let (lower, upper) = Statistics::confidence_interval(&values, 0.95);
    
    let mean = Statistics::mean(&values);
    assert!(lower <= mean);
    assert!(upper >= mean);
}

#[test]
fn test_chi_square_test() {
    let observed = vec![10.0, 20.0, 30.0, 40.0];
    let expected = vec![25.0, 25.0, 25.0, 25.0];
    let chi_square = Statistics::chi_square_test(&observed, &expected);
    
    assert!(chi_square > 0.0);
}

#[test]
fn test_entropy_calculation() {
    let probabilities = vec![0.5, 0.5];
    let entropy = Statistics::entropy(&probabilities);
    
    // Entropy of fair coin flip
    let expected = -(0.5 * (0.5_f64.ln()) + 0.5 * (0.5_f64.ln()));
    assert!((entropy - expected).abs() < 1e-10);
}

#[test]
fn test_mutual_information() {
    use std::collections::HashMap;
    
    let mut joint_probs = HashMap::new();
    joint_probs.insert((0, 0), 0.25);
    joint_probs.insert((0, 1), 0.25);
    joint_probs.insert((1, 0), 0.25);
    joint_probs.insert((1, 1), 0.25);
    
    let mi = Statistics::mutual_information(&joint_probs);
    
    // Independent variables should have zero mutual information
    assert!((mi - 0.0).abs() < 1e-10);
}

#[test]
fn test_mutual_information_dependent() {
    use std::collections::HashMap;
    
    let mut joint_probs = HashMap::new();
    joint_probs.insert((0, 0), 0.5);
    joint_probs.insert((1, 1), 0.5);
    // Other combinations have zero probability
    
    let mi = Statistics::mutual_information(&joint_probs);
    
    // Perfectly correlated variables should have high mutual information
    assert!(mi > 0.0);
}
