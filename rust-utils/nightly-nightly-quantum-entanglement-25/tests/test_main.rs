use nightly_quantum_entanglement_checker::*;
use std::time::Duration;

#[tokio::test]
async fn test_quantum_state_symbols() {
    assert_eq!(QuantumState::Zero.to_symbol(), "|0⟩");
    assert_eq!(QuantumState::One.to_symbol(), "|1⟩");
    assert_eq!(QuantumState::Plus.to_symbol(), "|+⟩");
    assert_eq!(QuantumState::Minus.to_symbol(), "|-⟩");
}

#[tokio::test]
async fn test_quantum_node_creation() {
    let node = QuantumNode::new(0).await;
    assert_eq!(node.id, 0);
    assert_eq!(node.state, QuantumState::Zero);
    assert!(node.entangled_with.is_empty());
}

#[tokio::test]
async fn test_quantum_node_entanglement() {
    let mut node = QuantumNode::new(1).await;
    node.entangle_with(2).await;
    assert_eq!(node.entangled_with, vec![2]);
}

#[tokio::test]
async fn test_quantum_measurement_consistency() {
    let node = QuantumNode::new(2).await; // Should be Plus state
    let measurement1 = node.get_measurement();
    let measurement2 = node.get_measurement();
    
    // Measurements should be consistent for the same node
    assert!((measurement1 - measurement2).abs() < 0.1);
}

#[tokio::test]
async fn test_quantum_network_creation() {
    let nodes = create_quantum_network(3, false).await;
    
    assert_eq!(nodes.len(), 3);
    
    // Check that each node has the correct state based on its ID
    assert_eq!(nodes[0].state, QuantumState::Zero);
    assert_eq!(nodes[1].state, QuantumState::One);
    assert_eq!(nodes[2].state, QuantumState::Plus);
    
    // Check entanglement topology (ring)
    assert_eq!(nodes[0].entangled_with, vec![1]);
    assert_eq!(nodes[1].entangled_with, vec![2]);
    assert_eq!(nodes[2].entangled_with, vec![0]);
}

#[tokio::test]
async fn test_quantum_entanglement_verification_success() {
    let nodes = create_quantum_network(4, false).await;
    let result = verify_entanglement(&nodes, false).await;
    assert!(result, "Entanglement verification should succeed for properly entangled nodes");
}

#[tokio::test]
async fn test_quantum_entanglement_verification_failure() {
    // Create nodes with inconsistent states to force verification failure
    let mut nodes = Vec::new();
    
    // Manually create nodes with very different measurements
    nodes.push(QuantumNode {
        id: 0,
        state: QuantumState::Zero,
        entangled_with: vec![1],
    });
    
    nodes.push(QuantumNode {
        id: 1,
        state: QuantumState::One,
        entangled_with: vec![0],
    });
    
    // This should fail due to high variance between |0⟩ and |1⟩ states
    let result = verify_entanglement(&nodes, false).await;
    assert!(!result, "Entanglement verification should fail for inconsistent states");
}

#[tokio::test]
async fn test_large_quantum_network() {
    let nodes = create_quantum_network(10, false).await;
    assert_eq!(nodes.len(), 10);
    
    // Verify all nodes are properly entangled
    for node in &nodes {
        assert_eq!(node.entangled_with.len(), 1, "Each node should be entangled with exactly one other node");
    }
    
    let result = verify_entanglement(&nodes, false).await;
    assert!(result, "Large quantum network should maintain entanglement");
}

#[tokio::test]
async fn test_quantum_state_distribution() {
    let nodes = create_quantum_network(8, false).await;
    
    // Count distribution of quantum states
    let mut state_counts = HashMap::new();
    for node in &nodes {
        *state_counts.entry(&node.state).or_insert(0) += 1;
    }
    
    // With 8 nodes and 4 state types, we should have roughly equal distribution
    assert_eq!(state_counts.len(), 4, "All four quantum states should be present");
    for count in state_counts.values() {
        assert!(*count >= 1, "Each quantum state should appear at least once");
    }
}

#[tokio::test]
async fn test_entanglement_timing() {
    let start = std::time::Instant::now();
    let _nodes = create_quantum_network(5, false).await;
    let duration = start.elapsed();
    
    // Network creation should be reasonably fast (less than 1 second)
    assert!(duration < Duration::from_secs(1), "Quantum network creation should be fast");
}

#[tokio::test]
async fn test_concurrent_node_creation() {
    // Test that nodes can be created concurrently without issues
    let mut handles = Vec::new();
    for i in 0..5 {
        handles.push(tokio::spawn(async move {
            QuantumNode::new(i).await
        }));
    }
    
    let mut nodes = Vec::new();
    for handle in handles {
        nodes.push(handle.await.unwrap());
    }
    
    assert_eq!(nodes.len(), 5);
    
    // Verify each node has unique ID and proper state
    for (i, node) in nodes.iter().enumerate() {
        assert_eq!(node.id, i);
        assert_eq!(node.state, match i % 4 {
            0 => QuantumState::Zero,
            1 => QuantumState::One,
            2 => QuantumState::Plus,
            _ => QuantumState::Minus,
        });
    }
}
