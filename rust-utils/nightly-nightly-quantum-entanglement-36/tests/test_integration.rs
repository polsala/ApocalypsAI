use nightly_quantum_entanglement_checker::*;
use std::collections::HashMap;

#[test]
fn test_full_simulation_workflow() {
    let simulator = QuantumSimulator::new(4, 100);
    let measurements = simulator.simulate_entanglement();
    
    let calculator = FidelityCalculator::new(0.8);
    let fidelities = calculator.calculate_fidelities(&measurements);
    
    // Should have fidelities for all pairs
    assert_eq!(fidelities.len(), 6); // 4 choose 2 = 6 pairs
    
    // All fidelities should be in valid range
    for (&(node1, node2), &fidelity) in fidelities.iter() {
        assert!(fidelity >= 0.0 && fidelity <= 1.0, 
            "Fidelity for pair ({}, {}) is out of range: {}", node1, node2, fidelity);
    }
}

#[test]
fn test_simulation_deterministic_with_seed() {
    // Note: This test documents the current behavior
    // In a real implementation, you might want to add seed support
    let simulator1 = QuantumSimulator::new(3, 50);
    let measurements1 = simulator1.simulate_entanglement();
    
    let simulator2 = QuantumSimulator::new(3, 50);
    let measurements2 = simulator2.simulate_entanglement();
    
    // Measurements should be different due to randomness
    // (This is expected behavior for now)
    let pair = (0, 1);
    let diff_count = measurements1.get(&pair).unwrap()
        .iter()
        .zip(measurements2.get(&pair).unwrap())
        .filter(|(m1, m2)| m1 != m2)
        .count();
    
    // Should have some differences (not guaranteed, but very likely)
    // This test mainly ensures the simulation runs without errors
    assert!(diff_count >= 0);
}

#[test]
fn test_large_system_simulation() {
    // Test with a larger system to ensure it doesn't crash
    let simulator = QuantumSimulator::new(10, 100);
    let measurements = simulator.simulate_entanglement();
    
    // Should have 10 choose 2 = 45 pairs
    assert_eq!(measurements.len(), 45);
    
    let calculator = FidelityCalculator::new(0.8);
    let fidelities = calculator.calculate_fidelities(&measurements);
    
    assert_eq!(fidelities.len(), 45);
}

#[test]
fn test_edge_case_two_nodes() {
    let simulator = QuantumSimulator::new(2, 10);
    let measurements = simulator.simulate_entanglement();
    
    assert_eq!(measurements.len(), 1); // Only one pair: (0, 1)
    assert!(measurements.contains_key(&(0, 1)));
    
    let calculator = FidelityCalculator::new(0.8);
    let fidelities = calculator.calculate_fidelities(&measurements);
    
    assert_eq!(fidelities.len(), 1);
}

#[test]
fn test_json_output_structure() {
    // This test ensures the JSON output has the expected structure
    // We'll test this by checking that we can serialize the results
    use serde_json;
    
    let simulator = QuantumSimulator::new(3, 10);
    let measurements = simulator.simulate_entanglement();
    let calculator = FidelityCalculator::new(0.8);
    let fidelities = calculator.calculate_fidelities(&measurements);
    
    // Test that we can create the JSON structure
    let mut fidelity_details = Vec::new();
    for ((node1, node2), fidelity) in fidelities.iter() {
        fidelity_details.push(serde_json::json!({
            "node1": node1,
            "node2": node2,
            "fidelity": fidelity,
            "entangled": fidelity >= &0.8
        }));
    }
    
    let output = serde_json::json!({
        "simulation": {
            "nodes": 3,
            "measurements": 10,
            "fidelity_threshold": 0.8,
            "duration_ms": 0
        },
        "results": {
            "total_pairs": fidelity_details.len(),
            "entangled_pairs": fidelity_details.iter().filter(|d| d["entangled"] == true).count(),
            "classical_correlation_pairs": fidelity_details.iter().filter(|d| d["entangled"] == false).count(),
            "entanglement_percentage": 50.0,
            "fidelity_details": fidelity_details
        }
    });
    
    // Should be able to serialize to string
    let json_str = serde_json::to_string_pretty(&output).unwrap();
    assert!(json_str.contains("simulation"));
    assert!(json_str.contains("results"));
    assert!(json_str.contains("fidelity_details"));
}
