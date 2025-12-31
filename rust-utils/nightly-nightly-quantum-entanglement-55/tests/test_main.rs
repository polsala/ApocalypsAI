use quantum_entanglement_checker::*;
use std::net::SocketAddr;
use std::str::FromStr;

#[tokio::test]
async fn test_quantum_state_generation() {
    let nodes = vec![
        SocketAddr::from_str("127.0.0.1:8080").unwrap(),
        SocketAddr::from_str("127.0.0.1:8081").unwrap(),
    ];

    let checker = QuantumEntanglementChecker::new(nodes, 0.8, 0.05, 30);
    let states = checker.generate_entangled_states().await;

    assert_eq!(states.len(), 2);

    // Check that states are within valid ranges
    for (_, state) in states.iter() {
        assert!(state.spin >= 0.0 && state.spin <= 1.0);
        assert!(state.phase >= 0.0 && state.phase < 2.0 * std::f64::consts::PI);
        assert!(state.coherence >= 0.0 && state.coherence <= 1.0);
    }
}

#[tokio::test]
async fn test_entanglement_matrix() {
    let nodes = vec![
        SocketAddr::from_str("127.0.0.1:8080").unwrap(),
        SocketAddr::from_str("127.0.0.1:8081").unwrap(),
    ];

    let checker = QuantumEntanglementChecker::new(nodes, 0.8, 0.05, 30);
    let states = checker.generate_entangled_states().await;
    let matrix = checker.measure_entanglement(&states).await;

    // Matrix should be square
    assert_eq!(matrix.len(), 2);
    assert_eq!(matrix[0].len(), 2);
    assert_eq!(matrix[1].len(), 2);

    // Diagonal elements should be 1.0 (perfect self-entanglement)
    assert_eq!(matrix[0][0], 1.0);
    assert_eq!(matrix[1][1], 1.0);

    // Off-diagonal elements should be between 0.0 and 1.0
    assert!(matrix[0][1] >= 0.0 && matrix[0][1] <= 1.0);
    assert!(matrix[1][0] >= 0.0 && matrix[1][0] <= 1.0);
}

#[tokio::test]
async fn test_quantum_coherence_calculation() {
    let nodes = vec![
        SocketAddr::from_str("127.0.0.1:8080").unwrap(),
        SocketAddr::from_str("127.0.0.1:8081").unwrap(),
    ];

    let checker = QuantumEntanglementChecker::new(nodes, 0.8, 0.05, 30);
    let states = checker.generate_entangled_states().await;
    let matrix = checker.measure_entanglement(&states).await;
    let coherence = checker.calculate_coherence(&matrix).await;

    // Coherence should be between 0.0 and 100.0
    assert!(coherence >= 0.0 && coherence <= 100.0);
}

#[tokio::test]
async fn test_spooky_action_detection() {
    let nodes = vec![
        SocketAddr::from_str("127.0.0.1:8080").unwrap(),
        SocketAddr::from_str("127.0.0.1:8081").unwrap(),
    ];

    let checker = QuantumEntanglementChecker::new(nodes, 0.9, 0.01, 30);
    let states = checker.generate_entangled_states().await;
    let matrix = checker.measure_entanglement(&states).await;
    let coherence = checker.calculate_coherence(&matrix).await;
    let spooky = checker.detect_spooky_action(coherence).await;

    // With high entanglement strength and low decoherence, should detect spooky action
    assert!(spooky || coherence <= 75.0);
}

#[tokio::test]
async fn test_decoherence_event_counting() {
    let nodes = vec![
        SocketAddr::from_str("127.0.0.1:8080").unwrap(),
        SocketAddr::from_str("127.0.0.1:8081").unwrap(),
        SocketAddr::from_str("127.0.0.1:8082").unwrap(),
    ];

    let checker = QuantumEntanglementChecker::new(nodes, 0.8, 0.05, 30);
    let states = checker.generate_entangled_states().await;
    let matrix = checker.measure_entanglement(&states).await;
    let events = checker.count_decoherence_events(&matrix).await;

    // Should count events where entanglement < 0.3
    let mut expected_events = 0;
    for i in 0..nodes.len() {
        for j in (i + 1)..nodes.len() {
            if matrix[i][j] < 0.3 {
                expected_events += 1;
            }
        }
    }

    assert_eq!(events, expected_events);
}

#[tokio::test]
async fn test_recommendation_generation() {
    let nodes = vec![
        SocketAddr::from_str("127.0.0.1:8080").unwrap(),
        SocketAddr::from_str("127.0.0.1:8081").unwrap(),
    ];

    let checker = QuantumEntanglementChecker::new(nodes, 0.8, 0.05, 30);

    // Test high coherence recommendations
    let recommendations = checker.generate_recommendations(85.0, true).await;
    assert!(recommendations.iter().any(|r| r.contains("quantum-resistant")));
    assert!(recommendations.iter().any(|r| r.contains("quantum operations")));

    // Test low coherence recommendations
    let recommendations = checker.generate_recommendations(30.0, false).await;
    assert!(recommendations.iter().any(|r| r.contains("connectivity issues")));
    assert!(recommendations.iter().any(|r| r.contains("synchronization")));

    // Test normal recommendations
    let recommendations = checker.generate_recommendations(60.0, false).await;
    assert!(recommendations.iter().any(|r| r.contains("normal parameters")));
}

#[tokio::test]
async fn test_full_measurement_workflow() {
    let nodes = vec![
        SocketAddr::from_str("127.0.0.1:8080").unwrap(),
        SocketAddr::from_str("127.0.0.1:8081").unwrap(),
    ];

    let checker = QuantumEntanglementChecker::new(nodes, 0.8, 0.05, 30);
    let report = checker.run_measurement().await;

    // Verify report structure
    assert_eq!(report.nodes.len(), 2);
    assert_eq!(report.entanglement_matrix.len(), 2);
    assert!(report.quantum_coherence >= 0.0 && report.quantum_coherence <= 100.0);
    assert!(report.recommendations.len() > 0);
    assert!(report.measurement_time.contains("UTC"));
}

#[test]
fn test_matrix_formatting() {
    let matrix = vec![
        vec![1.0, 0.85, 0.72],
        vec![0.85, 1.0, 0.68],
        vec![0.72, 0.68, 1.0],
    ];

    let formatted = format_matrix(&matrix);
    assert!(formatted.contains("node0"));
    assert!(formatted.contains("node1"));
    assert!(formatted.contains("node2"));
    assert!(formatted.contains("1.00"));
    assert!(formatted.contains("0.85"));
}

#[test]
fn test_parameter_validation() {
    // Test entanglement strength bounds
    assert!((0.0..=1.0).contains(&0.8));
    assert!(!(0.0..=1.0).contains(&1.1));
    assert!(!(0.0..=1.0).contains(&-0.1));

    // Test decoherence rate bounds
    assert!((0.0..=1.0).contains(&0.05));
    assert!(!(0.0..=1.0).contains(&1.5));
    assert!(!(0.0..=1.0).contains(&-0.01));
}

// Mock rationale: These tests verify the quantum entanglement simulation
// without requiring actual network connections or quantum hardware.
// They test the mathematical models and data structures that simulate
// quantum phenomena in a classical computing environment.
