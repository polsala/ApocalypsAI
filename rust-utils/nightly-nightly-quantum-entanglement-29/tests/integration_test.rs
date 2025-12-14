use nightly_quantum_entanglement_checker::*;

#[test]
fn test_full_entanglement_workflow() {
    // Test the complete entanglement verification workflow
    let config = Config {
        nodes: 4,
        trials: 100,
        seed: 42,
        visualize: false,
    };
    
    let mut simulator = QuantumSimulator::new(config.seed);
    let mut bell_test = BellTest::new();
    
    // Generate entangled states
    let entangled_states = simulator.generate_entangled_states(config.nodes, config.trials);
    assert_eq!(entangled_states.len(), config.trials);
    
    // Test Bell inequality
    let chsh_result = bell_test.test_chsh_inequality(&entangled_states);
    
    // Verify quantum violation
    assert!(chsh_result.s_value > 2.0, "Expected quantum violation, got S = {}", chsh_result.s_value);
    assert!(chsh_result.s_value <= 2.828 + 1e-10, "S exceeds quantum limit");
}

#[test]
fn test_deterministic_results() {
    // Test that same configuration produces identical results
    let config1 = Config {
        nodes: 3,
        trials: 50,
        seed: 123,
        visualize: false,
    };
    
    let config2 = Config {
        nodes: 3,
        trials: 50,
        seed: 123,
        visualize: false,
    };
    
    let mut simulator1 = QuantumSimulator::new(config1.seed);
    let mut simulator2 = QuantumSimulator::new(config2.seed);
    
    let states1 = simulator1.generate_entangled_states(config1.nodes, config1.trials);
    let states2 = simulator2.generate_entangled_states(config2.nodes, config2.trials);
    
    assert_eq!(states1, states2);
}

#[test]
fn test_performance_scaling() {
    // Test that the tool scales reasonably with input size
    use std::time::Instant;
    
    let mut simulator = QuantumSimulator::new(42);
    
    // Small scale test
    let start = Instant::now();
    let _states_small = simulator.generate_entangled_states(2, 100);
    let time_small = start.elapsed();
    
    // Large scale test
    let start = Instant::now();
    let _states_large = simulator.generate_entangled_states(8, 10000);
    let time_large = start.elapsed();
    
    // Large test should take longer but be reasonable
    assert!(time_large > time_small);
    assert!(time_large.as_secs() < 5, "Large scale test should complete quickly");
}

#[test]
fn test_classical_vs_quantum() {
    let mut bell_test = BellTest::new();
    
    // Classical data (should not violate CHSH)
    let classical_states = vec![
        (1.0, 0.0, 1.0, 0.0),
        (-1.0, 0.0, -1.0, 0.0),
        (1.0, PI/2.0, 1.0, PI/2.0),
        (-1.0, PI/2.0, -1.0, PI/2.0),
    ];
    
    let classical_result = bell_test.test_chsh_inequality(&classical_states);
    assert!(classical_result.s_value <= 2.0 + 1e-10, 
           "Classical data should not violate CHSH: S = {}", classical_result.s_value);
    
    // Quantum data (should violate CHSH)
    let quantum_states = vec![
        (1.0, 0.0, -1.0, 0.0),
        (-1.0, 0.0, 1.0, 0.0),
        (1.0, PI/4.0, -1.0, PI/4.0),
        (-1.0, PI/4.0, 1.0, PI/4.0),
    ];
    
    let quantum_result = bell_test.test_chsh_inequality(&quantum_states);
    assert!(quantum_result.s_value > 2.0, 
           "Quantum data should violate CHSH: S = {}", quantum_result.s_value);
}
