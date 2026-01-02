use nightly_quantum_entanglement_checker::quantum_checker::*;
use tokio::time::{sleep, Duration};

#[tokio::test]
async fn test_full_quantum_workflow() {
    // Test the complete quantum entanglement workflow
    let mut nodes = vec![
        QuantumNode::new("Integration-Alpha".to_string()),
        QuantumNode::new("Integration-Beta".to_string()),
        QuantumNode::new("Integration-Gamma".to_string()),
    ];
    
    // Spin up all processors
    for node in nodes.iter_mut() {
        node.spin_up_processors().await;
    }
    
    // Verify all nodes have different initial states (before entanglement)
    let alpha_state = nodes[0].quantum_state;
    let beta_state = nodes[1].quantum_state;
    let gamma_state = nodes[2].quantum_state;
    
    // After spin-up, states should be different (unless by random chance)
    // We'll just verify they're in valid range
    assert!(alpha_state >= 0.0 && alpha_state <= 1.0);
    assert!(beta_state >= 0.0 && beta_state <= 1.0);
    assert!(gamma_state >= 0.0 && gamma_state <= 1.0);
    
    // Establish entanglement
    let entanglement_success = establish_entanglement(&mut nodes).await;
    assert!(entanglement_success);
    
    // After entanglement, all states should be the same
    assert_eq!(nodes[0].quantum_state, nodes[1].quantum_state);
    assert_eq!(nodes[1].quantum_state, nodes[2].quantum_state);
    assert!(nodes.iter().all(|n| n.is_entangled));
    
    // Verify entanglement
    let verification_success = verify_entanglement(&nodes).await;
    assert!(verification_success);
}

#[tokio::test]
async fn test_quantum_measurement_probabilities() {
    // Test that quantum measurements have the expected probabilistic behavior
    let node = QuantumNode::new("Probability-Test".to_string());
    node.spin_up_processors().await;
    
    let mut successes = 0;
    let total_measurements = 100;
    
    for _ in 0..total_measurements {
        if node.measure_state().await {
            successes += 1;
        }
    }
    
    // With 90% success rate, we should get roughly 90 successes out of 100
    // Allow some variance due to randomness
    let success_rate = successes as f64 / total_measurements as f64;
    assert!(success_rate > 0.7, "Success rate too low: {}", success_rate);
    assert!(success_rate < 1.0, "Success rate too high: {}", success_rate);
}

#[tokio::test]
async fn test_quantum_entanglement_timing() {
    // Test that entanglement operations complete in reasonable time
    let start = std::time::Instant::now();
    
    let mut nodes = vec![
        QuantumNode::new("Timing-Alpha".to_string()),
        QuantumNode::new("Timing-Beta".to_string()),
    ];
    
    nodes[0].spin_up_processors().await;
    nodes[1].spin_up_processors().await;
    
    let entanglement_success = establish_entanglement(&mut nodes).await;
    let verification_success = verify_entanglement(&nodes).await;
    
    let duration = start.elapsed();
    
    assert!(entanglement_success);
    assert!(verification_success);
    // Should complete much faster than real-time (since we use mocked delays)
    assert!(duration < std::time::Duration::from_secs(5));
}
