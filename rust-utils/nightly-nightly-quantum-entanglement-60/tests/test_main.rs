use nightly_quantum_entanglement_simulator::*;
use rand::SeedableRng;
use rand::rngs::StdRng;

#[test]
fn test_entangled_pair_generation() {
    let mut simulator = QuantumSimulator::new(10, 1000);
    
    // Use a fixed seed for deterministic tests
    simulator.rng = StdRng::seed_from_u64(42);
    
    let pair = simulator.generate_entangled_pair(1);
    
    // Basic validation
    assert_eq!(pair.id, 1);
    assert!(pair.distance_km == 1000);
    assert!(pair.alice_measurement.angle >= 0.0 && pair.alice_measurement.angle < 360.0);
    assert!(pair.bob_measurement.angle >= 0.0 && pair.bob_measurement.angle < 360.0);
}

#[test]
fn test_spin_values() {
    let spin_up = Spin::Up;
    let spin_down = Spin::Down;
    
    assert!(spin_up != spin_down);
    
    // Test that Up and Down are distinct
    match spin_up {
        Spin::Up => assert!(true),
        Spin::Down => assert!(false, "Spin::Up should not equal Spin::Down"),
    }
    
    match spin_down {
        Spin::Up => assert!(false, "Spin::Down should not equal Spin::Up"),
        Spin::Down => assert!(true),
    }
}

#[test]
fn test_bell_correlation_calculation() {
    let simulator = QuantumSimulator::new(100, 1000);
    
    // Create test pairs with known correlations
    let test_pairs = vec![
        ParticlePair {
            id: 1,
            alice_measurement: Measurement { angle: 0.0, result: Spin::Up },
            bob_measurement: Measurement { angle: 0.0, result: Spin::Down },
            distance_km: 1000,
            correlated: true,
        },
        ParticlePair {
            id: 2,
            alice_measurement: Measurement { angle: 90.0, result: Spin::Down },
            bob_measurement: Measurement { angle: 90.0, result: Spin::Up },
            distance_km: 1000,
            correlated: true,
        },
    ];
    
    let correlation = simulator.calculate_bell_correlation(&test_pairs);
    
    // With perfect anti-correlation, we should get a high Bell correlation
    assert!(correlation > 0.0);
    assert!(correlation <= 4.0); // CHSH value should be <= 4
}

#[test]
fn test_simulation_results_structure() {
    let mut simulator = QuantumSimulator::new(5, 500);
    
    // Use a fixed seed for deterministic tests
    simulator.rng = StdRng::seed_from_u64(123);
    
    let results = simulator.run();
    
    // Validate results structure
    assert_eq!(results.pairs.len(), 5);
    assert!(results.bell_correlation >= 0.0);
    assert_eq!(results.classical_limit, 2.0);
    assert!(results.violation_percentage >= 0.0);
    
    // Check that all pairs have the correct distance
    for pair in &results.pairs {
        assert_eq!(pair.distance_km, 500);
    }
}

#[test]
fn test_json_serialization() {
    let test_results = SimulationResults {
        pairs: vec![
            ParticlePair {
                id: 1,
                alice_measurement: Measurement { angle: 45.0, result: Spin::Up },
                bob_measurement: Measurement { angle: 45.0, result: Spin::Down },
                distance_km: 1000,
                correlated: true,
            }
        ],
        bell_correlation: 2.5,
        classical_limit: 2.0,
        quantum_violation: true,
        violation_percentage: 25.0,
    };
    
    // Test serialization
    let json = serde_json::to_string(&test_results).expect("Failed to serialize to JSON");
    assert!(json.contains("pairs"));
    assert!(json.contains("bell_correlation"));
    assert!(json.contains("quantum_violation"));
    
    // Test deserialization
    let deserialized: SimulationResults = serde_json::from_str(&json).expect("Failed to deserialize from JSON");
    assert_eq!(deserialized.pairs.len(), 1);
    assert_eq!(deserialized.bell_correlation, 2.5);
    assert_eq!(deserialized.quantum_violation, true);
}

#[test]
fn test_large_simulation() {
    let mut simulator = QuantumSimulator::new(10000, 10000);
    
    // Use a fixed seed for deterministic tests
    simulator.rng = StdRng::seed_from_u64(999);
    
    let results = simulator.run();
    
    // Validate large simulation
    assert_eq!(results.pairs.len(), 10000);
    assert!(results.bell_correlation >= 0.0);
    assert!(results.bell_correlation <= 4.0);
    
    // Check that distances are consistent
    for pair in &results.pairs {
        assert_eq!(pair.distance_km, 10000);
    }
}
