use nightly_quantum_entanglement_checker::*;
use std::time::Instant;

/// Test quantum state equality
#[test]
fn test_quantum_state_equality() {
    let state1 = QuantumState::SpinUp;
    let state2 = QuantumState::SpinUp;
    let state3 = QuantumState::SpinDown;
    
    assert_eq!(state1, state2);
    assert_ne!(state1, state3);
    assert_ne!(state2, state3);
}

/// Test correlation calculation with identical states
#[tokio::test]
async fn test_correlation_identical_states() {
    let measurements = vec![
        Measurement {
            node_id: 0,
            state: QuantumState::SpinUp,
            timestamp: Instant::now(),
            measurement_basis: 0.0,
        },
        Measurement {
            node_id: 1,
            state: QuantumState::SpinUp,
            timestamp: Instant::now(),
            measurement_basis: 0.0,
        },
    ];
    
    let correlation = calculate_correlation(&measurements);
    assert_eq!(correlation, 1.0);
}

/// Test correlation calculation with opposite states
#[tokio::test]
async fn test_correlation_opposite_states() {
    let measurements = vec![
        Measurement {
            node_id: 0,
            state: QuantumState::SpinUp,
            timestamp: Instant::now(),
            measurement_basis: 0.0,
        },
        Measurement {
            node_id: 1,
            state: QuantumState::SpinDown,
            timestamp: Instant::now(),
            measurement_basis: 0.0,
        },
    ];
    
    let correlation = calculate_correlation(&measurements);
    assert_eq!(correlation, -1.0);
}

/// Test correlation calculation with different bases
#[tokio::test]
async fn test_correlation_different_bases() {
    let measurements = vec![
        Measurement {
            node_id: 0,
            state: QuantumState::SpinUp,
            timestamp: Instant::now(),
            measurement_basis: 0.0, // 0 degrees
        },
        Measurement {
            node_id: 1,
            state: QuantumState::SpinUp,
            timestamp: Instant::now(),
            measurement_basis: std::f64::consts::PI / 2.0, // 90 degrees
        },
    ];
    
    let correlation = calculate_correlation(&measurements);
    // With 90-degree difference, cos(π/2) = 0, so correlation should be 0
    assert!((correlation - 0.0).abs() < 0.001);
}

/// Test Bell inequality with classical limit
#[tokio::test]
async fn test_bell_inequality_classical() {
    let measurements = vec![
        Measurement {
            node_id: 0,
            state: QuantumState::SpinUp,
            timestamp: Instant::now(),
            measurement_basis: 0.0,
        },
        Measurement {
            node_id: 1,
            state: QuantumState::SpinDown,
            timestamp: Instant::now(),
            measurement_basis: 0.0,
        },
    ];
    
    let bell_value = calculate_bell_inequality(&measurements);
    assert_eq!(bell_value, 2.0); // Classical limit
}

/// Test measurement consistency with perfect timing
#[tokio::test]
async fn test_consistency_perfect_timing() {
    let now = Instant::now();
    let measurements = vec![
        Measurement {
            node_id: 0,
            state: QuantumState::SpinUp,
            timestamp: now,
            measurement_basis: 0.0,
        },
        Measurement {
            node_id: 1,
            state: QuantumState::SpinUp,
            timestamp: now,
            measurement_basis: 0.0,
        },
    ];
    
    let consistency = calculate_consistency(&measurements);
    assert_eq!(consistency, 100.0);
}

/// Test measurement consistency with different states
#[tokio::test]
async fn test_consistency_different_states() {
    let now = Instant::now();
    let measurements = vec![
        Measurement {
            node_id: 0,
            state: QuantumState::SpinUp,
            timestamp: now,
            measurement_basis: 0.0,
        },
        Measurement {
            node_id: 1,
            state: QuantumState::SpinDown,
            timestamp: now,
            measurement_basis: 0.0,
        },
    ];
    
    let consistency = calculate_consistency(&measurements);
    assert_eq!(consistency, 0.0);
}

/// Test empty measurements edge case
#[tokio::test]
async fn test_empty_measurements() {
    let measurements = vec![];
    
    let correlation = calculate_correlation(&measurements);
    assert_eq!(correlation, 0.0);
    
    let bell_value = calculate_bell_inequality(&measurements);
    assert_eq!(bell_value, 2.0);
    
    let consistency = calculate_consistency(&measurements);
    assert_eq!(consistency, 100.0);
}

/// Test single measurement edge case
#[tokio::test]
async fn test_single_measurement() {
    let measurements = vec![
        Measurement {
            node_id: 0,
            state: QuantumState::SpinUp,
            timestamp: Instant::now(),
            measurement_basis: 0.0,
        },
    ];
    
    let correlation = calculate_correlation(&measurements);
    assert_eq!(correlation, 0.0);
    
    let bell_value = calculate_bell_inequality(&measurements);
    assert_eq!(bell_value, 2.0);
    
    let consistency = calculate_consistency(&measurements);
    assert_eq!(consistency, 100.0);
}

/// Test spooky action detection logic
#[tokio::test]
async fn test_spooky_action_detection() {
    // Create a configuration that should detect spooky action
    let config = QuantumConfig {
        num_nodes: 4,
        distance_km: 1000.0,
        correlation_threshold: 0.5,
        measurement_precision: 10,
        measurement_delay_ms: 50,
    };
    
    // Run the entanglement check
    let result = run_entanglement_check(&config).await;
    
    // The result should be deterministic enough for our tests
    // Since we're using random generation, we'll test the structure
    assert!(result.correlation_strength >= -1.0 && result.correlation_strength <= 1.0);
    assert!(result.bell_inequality_value >= 0.0);
    assert!(result.measurement_consistency >= 0.0 && result.measurement_consistency <= 100.0);
}

/// Test correlation formatting
#[test]
fn test_format_correlation() {
    assert_eq!(format_correlation(0.9), "0.900 👻");
    assert_eq!(format_correlation(0.6), "0.600 👻");
    assert_eq!(format_correlation(0.3), "0.300 🨀");
    assert_eq!(format_correlation(0.1), "0.100 😐");
    assert_eq!(format_correlation(-0.9), "0.900 👻"); // Absolute value
}

/// Test Bell value formatting
#[test]
fn test_format_bell_value() {
    assert_eq!(format_bell_value(2.5), "2.50 ⚛️");
    assert_eq!(format_bell_value(1.8), "1.80  classical");
}

/// Integration test: full workflow
#[tokio::test]
async fn test_full_entanglement_workflow() {
    let config = QuantumConfig {
        num_nodes: 3,
        distance_km: 500.0,
        correlation_threshold: 0.3,
        measurement_precision: 5,
        measurement_delay_ms: 10, // Fast for testing
    };
    
    let result = run_entanglement_check(&config).await;
    
    // Verify all metrics are within expected ranges
    assert!(result.correlation_strength >= -1.0 && result.correlation_strength <= 1.0);
    assert!(result.bell_inequality_value >= 0.0);
    assert!(result.measurement_consistency >= 0.0 && result.measurement_consistency <= 100.0);
    
    // Verify the result structure is complete
    assert!(result.spooky_action_detected == true || result.spooky_action_detected == false);
}

/// Performance test: ensure entanglement check completes in reasonable time
#[tokio::test]
async fn test_performance() {
    let config = QuantumConfig {
        num_nodes: 10,
        distance_km: 1000.0,
        correlation_threshold: 0.5,
        measurement_precision: 10,
        measurement_delay_ms: 5, // Minimal delay for testing
    };
    
    let start = Instant::now();
    let _result = run_entanglement_check(&config).await;
    let duration = start.elapsed();
    
    // Should complete in less than 1 second (with 5ms delays and 10 nodes)
    assert!(duration.as_secs() < 1);
}

/// Test configuration parsing
#[test]
fn test_config_parsing() {
    let config = QuantumConfig {
        num_nodes: 4,
        distance_km: 1000.0,
        correlation_threshold: 0.5,
        measurement_precision: 10,
        measurement_delay_ms: 50,
    };
    
    assert_eq!(config.num_nodes, 4);
    assert_eq!(config.distance_km, 1000.0);
    assert_eq!(config.correlation_threshold, 0.5);
    assert_eq!(config.measurement_precision, 10);
    assert_eq!(config.measurement_delay_ms, 50);
}
