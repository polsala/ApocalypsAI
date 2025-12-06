use nightly_quantum_quip_generator::*;

#[test]
fn integration_test_with_various_seeds() {
    let seeds = [0, 1, 42, 999, 12345, 987654];
    
    for seed in seeds {
        let quip = generate_quip(seed);
        assert!(QUANTUM_JOKES.contains(&quip), "Seed {}: Generated quip not in joke list: {}", seed, quip);
        assert!(!quip.is_empty(), "Seed {}: Generated quip is empty", seed);
    }
}

#[test]
fn integration_test_deterministic_behavior() {
    let test_seeds = [42, 123, 999];
    
    for seed in test_seeds {
        let quip1 = generate_quip(seed);
        let quip2 = generate_quip(seed);
        let quip3 = generate_quip(seed);
        
        assert_eq!(quip1, quip2, "First and second generation differ for seed {}", seed);
        assert_eq!(quip2, quip3, "Second and third generation differ for seed {}", seed);
    }
}

#[test]
fn integration_test_main_function_behavior() {
    // Test that the program runs without panicking
    // This is more of a smoke test
    let args = vec!["quantum-quip-generator", "--seed", "42"];
    
    // We can't easily test the main function's output without capturing stdout,
    // but we can at least ensure it doesn't panic with valid arguments
    // In a real integration test, you might use a test harness or mock the output
    
    // For now, we'll test the core logic that main() uses
    let seed = get_seed(Some(42));
    assert_eq!(seed, 42);
    
    let quip = generate_quip(seed);
    assert!(QUANTUM_JOKES.contains(&quip));
}

#[test]
fn integration_test_edge_case_seeds() {
    // Test with edge case seeds
    let edge_seeds = [0, 1, u64::MAX, u64::MIN];
    
    for seed in edge_seeds {
        let quip = generate_quip(seed);
        assert!(QUANTUM_JOKES.contains(&quip), "Edge seed {}: Generated quip not in joke list: {}", seed, quip);
        assert!(!quip.is_empty(), "Edge seed {}: Generated quip is empty", seed);
    }
}

#[test]
fn integration_test_joke_variety() {
    // Generate jokes with many different seeds to ensure variety
    let mut generated_jokes = std::collections::HashSet::new();
    
    for seed in 0..100 {
        let quip = generate_quip(seed);
        generated_jokes.insert(quip);
    }
    
    // With 10 jokes and 100 different seeds, we should get some variety
    // Even if we don't get all jokes, we should get multiple different ones
    assert!(generated_jokes.len() >= 2, "Expected at least 2 different jokes, got {}: {:?}", generated_jokes.len(), generated_jokes);
    assert!(generated_jokes.len() <= QUANTUM_JOKES.len(), "Generated more unique jokes than exist in the list!");
}
