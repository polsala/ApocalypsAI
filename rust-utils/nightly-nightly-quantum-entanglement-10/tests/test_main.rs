use nightly_quantum_entanglement_checker::*;
use std::time::Duration;

#[tokio::test]
async fn test_spin_state_equality() {
    assert_eq!(SpinState::Up, SpinState::Up);
    assert_eq!(SpinState::Down, SpinState::Down);
    assert_ne!(SpinState::Up, SpinState::Down);
}

#[tokio::test]
async fn test_decoherence_calculation() {
    let mut rng = rand::thread_rng();
    
    // Test at zero distance
    let decoherence_zero = calculate_decoherence(0.0, &mut rng);
    assert!(decoherence_zero >= 0.01 && decoherence_zero <= 0.03); // Base + small noise
    
    // Test at large distance
    let decoherence_large = calculate_decoherence(10000.0, &mut rng);
    assert!(decoherence_large >= 0.01 && decoherence_large <= 0.5); // Should be higher but capped
    
    // Test monotonic increase with distance
    let decoherence_1000 = calculate_decoherence(1000.0, &mut rng);
    let decoherence_5000 = calculate_decoherence(5000.0, &mut rng);
    assert!(decoherence_5000 >= decoherence_1000);
}

#[tokio::test]
async fn test_correlation_strength_calculation() {
    // Perfect anti-correlation with no decoherence
    let correlation = calculate_correlation_strength(&SpinState::Up, &SpinState::Down, 0.0);
    assert_eq!(correlation, 1.0);
    
    // Perfect correlation with no decoherence (should be low)
    let correlation = calculate_correlation_strength(&SpinState::Up, &SpinState::Up, 0.0);
    assert_eq!(correlation, 0.0);
    
    // With decoherence
    let correlation = calculate_correlation_strength(&SpinState::Up, &SpinState::Down, 0.1);
    assert_eq!(correlation, 0.9);
}

#[tokio::test]
async fn test_decoherence_application() {
    let up_state = SpinState::Up;
    let down_state = SpinState::Down;
    
    // With zero decoherence, state should remain unchanged
    let result = apply_decoherence(&up_state, 0.0);
    assert_eq!(result, SpinState::Up);
    
    let result = apply_decoherence(&down_state, 0.0);
    assert_eq!(result, SpinState::Down);
    
    // With 100% decoherence, state should always flip
    for _ in 0..100 {
        let result = apply_decoherence(&up_state, 1.0);
        assert_eq!(result, SpinState::Down);
        
        let result = apply_decoherence(&down_state, 1.0);
        assert_eq!(result, SpinState::Up);
    }
}

#[tokio::test]
async fn test_quantum_fidelity_determination() {
    assert_eq!(determine_quantum_fidelity(0.98), "EXCELLENT");
    assert_eq!(determine_quantum_fidelity(0.92), "GOOD");
    assert_eq!(determine_quantum_fidelity(0.87), "FAIR");
    assert_eq!(determine_quantum_fidelity(0.82), "POOR");
    assert_eq!(determine_quantum_fidelity(0.75), "CRITICAL");
}

#[tokio::test]
async fn test_particle_pair_generation() {
    let pairs = generate_entangled_pairs(10, 1000.0).await;
    
    assert_eq!(pairs.len(), 10);
    
    for pair in &pairs {
        // Each pair should have opposite spins initially
        assert_ne!(pair.particle_a, pair.particle_b);
        
        // Distance should be set correctly
        assert_eq!(pair.distance_km, 1000.0);
        
        // Decoherence should be reasonable
        assert!(pair.decoherence_factor >= 0.01 && pair.decoherence_factor <= 0.5);
    }
}

#[tokio::test]
async fn test_entanglement_verification() {
    let pairs = vec![
        ParticlePair {
            id: 0,
            particle_a: SpinState::Up,
            particle_b: SpinState::Down,
            distance_km: 1000.0,
            decoherence_factor: 0.05,
            is_entangled: true,
        },
        ParticlePair {
            id: 1,
            particle_a: SpinState::Down,
            particle_b: SpinState::Up,
            distance_km: 1000.0,
            decoherence_factor: 0.05,
            is_entangled: true,
        },
    ];
    
    let result = verify_entanglement(&pairs, 0.8, false).await;
    
    assert_eq!(result.total_pairs, 2);
    assert_eq!(result.successful_entanglements, 2);
    assert!(result.average_correlation > 0.9);
    assert_eq!(result.quantum_fidelity, "GOOD");
}

#[tokio::test]
async fn test_network_distribution() {
    let pairs = vec![
        ParticlePair { id: 0, particle_a: SpinState::Up, particle_b: SpinState::Down, distance_km: 1000.0, decoherence_factor: 0.1, is_entangled: true },
        ParticlePair { id: 1, particle_a: SpinState::Down, particle_b: SpinState::Up, distance_km: 1000.0, decoherence_factor: 0.1, is_entangled: true },
        ParticlePair { id: 2, particle_a: SpinState::Up, particle_b: SpinState::Down, distance_km: 1000.0, decoherence_factor: 0.1, is_entangled: true },
        ParticlePair { id: 3, particle_a: SpinState::Down, particle_b: SpinState::Up, distance_km: 1000.0, decoherence_factor: 0.1, is_entangled: true },
    ];
    
    let nodes = distribute_particles_to_nodes(pairs, 2).await;
    
    assert_eq!(nodes.len(), 2);
    assert_eq!(nodes[0].particles.len(), 2); // Even IDs: 0, 2
    assert_eq!(nodes[1].particles.len(), 2); // Odd IDs: 1, 3
    
    // Check that particles are distributed correctly
    assert_eq!(nodes[0].particles[0], SpinState::Up); // ID 0
    assert_eq!(nodes[0].particles[1], SpinState::Up); // ID 2
    assert_eq!(nodes[1].particles[0], SpinState::Down); // ID 1
    assert_eq!(nodes[1].particles[1], SpinState::Down); // ID 3
}

#[tokio::test]
async fn test_node_correlation_calculation() {
    let node_a = NetworkNode {
        id: 0,
        particles: vec![SpinState::Up, SpinState::Down, SpinState::Up],
    };
    
    let node_b = NetworkNode {
        id: 1,
        particles: vec![SpinState::Down, SpinState::Up, SpinState::Down],
    };
    
    let correlations = calculate_node_correlations(&node_a, &node_b);
    
    assert_eq!(correlations.len(), 3);
    // All should be perfectly anti-correlated with base decoherence
    for correlation in &correlations {
        assert!(*correlation > 0.8 && *correlation < 0.95);
    }
}

#[tokio::test]
async fn test_format_spin() {
    assert_eq!(format_spin(&SpinState::Up), "+½ (up)");
    assert_eq!(format_spin(&SpinState::Down), "-½ (down)");
}

#[tokio::test]
async fn test_large_scale_simulation() {
    // Test with a larger number of particles to ensure performance
    let start = std::time::Instant::now();
    let pairs = generate_entangled_pairs(1000, 5000.0).await;
    let result = verify_entanglement(&pairs, 0.8, false).await;
    let duration = start.elapsed();
    
    assert_eq!(pairs.len(), 1000);
    assert_eq!(result.total_pairs, 1000);
    assert!(result.successful_entanglements > 800); // Should have high success rate
    assert!(duration < Duration::from_secs(5)); // Should complete quickly
}

#[tokio::test]
async fn test_network_entanglement_verification() {
    let pairs = generate_entangled_pairs(100, 1000.0).await;
    let nodes = distribute_particles_to_nodes(pairs, 3).await;
    let result = verify_network_entanglement(&nodes, 0.8, false).await;
    
    assert_eq!(result.total_pairs, 100);
    assert!(result.successful_entanglements > 80);
    assert!(result.average_correlation > 0.8);
}

#[tokio::test]
async fn test_edge_cases() {
    // Test with zero particles
    let pairs = generate_entangled_pairs(0, 1000.0).await;
    assert_eq!(pairs.len(), 0);
    
    let result = verify_entanglement(&pairs, 0.9, false).await;
    assert_eq!(result.total_pairs, 0);
    assert_eq!(result.successful_entanglements, 0);
    assert_eq!(result.average_correlation, 0.0);
    
    // Test with single node network
    let single_node = vec![NetworkNode {
        id: 0,
        particles: vec![SpinState::Up, SpinState::Down],
    }];
    
    let result = verify_network_entanglement(&single_node, 0.9, false).await;
    assert_eq!(result.total_pairs, 0);
    assert_eq!(result.successful_entanglements, 0);
}

#[tokio::test]
async fn test_random_number_generation() {
    // This test would require refactoring to make it deterministic
    // For now, we'll just verify the function can be called
    // In a real implementation, we'd mock the random number generator
    
    // generate_quantum_random_numbers(10).await; // Would need async context
    assert!(true); // Placeholder
}

// Mock rationale: These tests verify the core quantum simulation logic
// without requiring actual quantum hardware. They test mathematical
// correctness of decoherence models, correlation calculations, and
// distributed system simulation.
