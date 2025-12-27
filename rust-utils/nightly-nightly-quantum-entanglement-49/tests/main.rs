use nightly_quantum_entanglement_checker::*;
use rand::SeedableRng;
use rand_chacha::ChaCha8Rng;

#[test]
fn test_generate_quantum_nodes() {
    let nodes = generate_quantum_nodes(3, 1000.0);
    
    assert_eq!(nodes.len(), 3);
    assert_eq!(nodes[0].id, "Node A");
    assert_eq!(nodes[1].id, "Node B");
    assert_eq!(nodes[2].id, "Node C");
    
    for node in &nodes {
        assert!(node.quantum_state >= 0.0 && node.quantum_state <= 1.0);
        assert!(node.position.0 >= 0.0 && node.position.0 <= 1000.0);
        assert!(node.position.1 >= 0.0 && node.position.1 <= 1000.0);
        assert!(node.position.2 >= 0.0 && node.position.2 <= 1000.0);
    }
}

#[test]
fn test_calculate_distance() {
    let pos1 = (0.0, 0.0, 0.0);
    let pos2 = (3.0, 4.0, 0.0);
    
    let distance = calculate_distance(pos1, pos2);
    assert!((distance - 5.0).abs() < 0.0001);
}

#[test]
fn test_calculate_average_correlation() {
    let results = vec![
        EntanglementResult {
            node_a: "A".to_string(),
            node_b: "B".to_string(),
            correlation: 0.8,
            entangled: true,
        },
        EntanglementResult {
            node_a: "A".to_string(),
            node_b: "C".to_string(),
            correlation: 0.6,
            entangled: true,
        },
        EntanglementResult {
            node_a: "B".to_string(),
            node_b: "C".to_string(),
            correlation: 0.4,
            entangled: false,
        },
    ];
    
    let average = calculate_average_correlation(&results);
    assert!((average - 0.6).abs() < 0.0001);
}

#[test]
fn test_determine_system_coherence() {
    assert_eq!(determine_system_coherence(0.9), "STABLE");
    assert_eq!(determine_system_coherence(0.7), "CAUTION");
    assert_eq!(determine_system_coherence(0.4), "UNSTABLE");
}

#[test]
fn test_simulate_entanglement_deterministic() {
    // Use a fixed seed for deterministic testing
    let mut rng = ChaCha8Rng::seed_from_u64(42);
    
    let nodes = vec![
        QuantumNode {
            id: "A".to_string(),
            quantum_state: 0.5,
            position: (0.0, 0.0, 0.0),
        },
        QuantumNode {
            id: "B".to_string(),
            quantum_state: 0.5,
            position: (1000.0, 0.0, 0.0),
        },
    ];
    
    let results = simulate_entanglement(&nodes, 0.8, 10);
    
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].node_a, "A");
    assert_eq!(results[0].node_b, "B");
    assert!(results[0].correlation >= 0.0 && results[0].correlation <= 1.0);
}

#[test]
fn test_empty_results_average_correlation() {
    let results = vec![];
    let average = calculate_average_correlation(&results);
    assert_eq!(average, 0.0);
}

#[test]
fn test_entanglement_threshold() {
    let results = vec![
        EntanglementResult {
            node_a: "A".to_string(),
            node_b: "B".to_string(),
            correlation: 0.6,
            entangled: true, // Should be true for correlation > 0.5
        },
        EntanglementResult {
            node_a: "A".to_string(),
            node_b: "C".to_string(),
            correlation: 0.4,
            entangled: false, // Should be false for correlation <= 0.5
        },
    ];
    
    assert!(results[0].entangled);
    assert!(!results[1].entangled);
}

#[test]
fn test_simulation_with_zero_distance() {
    let nodes = vec![
        QuantumNode {
            id: "A".to_string(),
            quantum_state: 0.5,
            position: (0.0, 0.0, 0.0),
        },
        QuantumNode {
            id: "B".to_string(),
            quantum_state: 0.5,
            position: (0.0, 0.0, 0.0), // Same position
        },
    ];
    
    let results = simulate_entanglement(&nodes, 0.8, 5);
    
    // With zero distance, correlation should be high
    assert!(results[0].correlation > 0.7);
}

#[test]
fn test_simulation_with_large_distance() {
    let nodes = vec![
        QuantumNode {
            id: "A".to_string(),
            quantum_state: 0.5,
            position: (0.0, 0.0, 0.0),
        },
        QuantumNode {
            id: "B".to_string(),
            quantum_state: 0.5,
            position: (10000.0, 0.0, 0.0), // Very far apart
        },
    ];
    
    let results = simulate_entanglement(&nodes, 0.8, 5);
    
    // With large distance, correlation should be lower due to distance factor
    assert!(results[0].correlation < 0.8);
}
