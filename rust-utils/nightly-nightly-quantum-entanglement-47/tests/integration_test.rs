use nightly_quantum_entanglement_simulator::quantum_simulator::*;

#[test]
fn test_simulator_creation() {
    let simulator = QuantumSimulator::new();
    assert_eq!(simulator.get_pairs().len(), 0);
    assert_eq!(simulator.get_observation_count(), 0);
    assert_eq!(simulator.get_teleportation_count(), 0);
}

#[test]
fn test_generate_entangled_pair() {
    let mut simulator = QuantumSimulator::new();
    let pair = simulator.generate_entangled_pair();
    
    // Check that particles have opposite states
    assert_ne!(pair.particle_a.spin, pair.particle_b.spin);
    assert_ne!(pair.particle_a.polarization, pair.particle_b.polarization);
    assert_ne!(pair.particle_a.color, pair.particle_b.color);
    assert_ne!(pair.particle_a.position, pair.particle_b.position);
    
    // Check entanglement strength is valid
    assert!(pair.entanglement_strength >= 0.8 && pair.entanglement_strength <= 1.0);
    
    // Check that pair was added to simulator
    assert_eq!(simulator.get_pairs().len(), 1);
    assert_eq!(simulator.get_results().pairs_generated, 1);
}

#[test]
fn test_observe_particle() {
    let mut simulator = QuantumSimulator::new();
    let pair = simulator.generate_entangled_pair();
    
    // Observe particle A
    let observation = simulator.observe_particle(0, true).unwrap();
    
    assert_eq!(observation.pair_id, 1);
    assert_eq!(observation.observed_particle, 1); // First particle ID
    assert!(observation.spooky_action);
    
    // Check that particles are marked as observed
    let pairs = simulator.get_pairs();
    assert!(pairs[0].particle_a.is_observed);
    assert!(pairs[0].particle_b.is_observed);
    
    // Check that observation was recorded
    assert_eq!(simulator.get_observation_count(), 1);
}

#[test]
fn test_quantum_teleportation_success() {
    let mut simulator = QuantumSimulator::new();
    let pair1 = simulator.generate_entangled_pair();
    let pair2 = simulator.generate_entangled_pair();
    
    // Teleport from first particle of pair1 to first particle of pair2
    let teleportation = simulator.quantum_teleportation(1, 3).unwrap();
    
    assert_eq!(teleportation.source_particle, 1);
    assert_eq!(teleportation.target_particle, 3);
    assert!(teleportation.fidelity >= 0.8 && teleportation.fidelity <= 1.0);
    
    // Check that teleportation was recorded
    assert_eq!(simulator.get_teleportation_count(), 1);
}

#[test]
fn test_quantum_teleportation_failure() {
    let mut simulator = QuantumSimulator::new();
    let pair1 = simulator.generate_entangled_pair();
    let pair2 = simulator.generate_entangled_pair();
    
    // Try to teleport from non-existent particle
    let result = simulator.quantum_teleportation(999, 3);
    assert!(result.is_none());
    
    // Try to teleport to non-existent particle
    let result = simulator.quantum_teleportation(1, 999);
    assert!(result.is_none());
}

#[test]
fn test_multiple_pairs_generation() {
    let mut simulator = QuantumSimulator::new();
    
    for _ in 0..10 {
        simulator.generate_entangled_pair();
    }
    
    assert_eq!(simulator.get_pairs().len(), 10);
    assert_eq!(simulator.get_results().pairs_generated, 10);
    
    // Check all pairs have valid entanglement strength
    for pair in simulator.get_pairs() {
        assert!(pair.entanglement_strength >= 0.8 && pair.entanglement_strength <= 1.0);
    }
}

#[test]
fn test_observation_idempotency() {
    let mut simulator = QuantumSimulator::new();
    simulator.generate_entangled_pair();
    
    // First observation should succeed
    let observation1 = simulator.observe_particle(0, true).unwrap();
    assert!(observation1.spooky_action);
    
    // Second observation of same pair should return None
    let observation2 = simulator.observe_particle(0, true);
    assert!(observation2.is_none());
    
    // But we should still have only one observation recorded
    assert_eq!(simulator.get_observation_count(), 1);
}

#[test]
fn test_average_entanglement_strength() {
    let mut simulator = QuantumSimulator::new();
    
    // Generate pairs with known entanglement strengths
    for _ in 0..5 {
        let pair = simulator.generate_entangled_pair();
        // We can't directly set the strength, but we can verify the calculation
    }
    
    let avg_strength = simulator.get_average_entanglement_strength();
    assert!(avg_strength >= 0.8 && avg_strength <= 1.0);
    
    // Test with empty simulator
    let empty_simulator = QuantumSimulator::new();
    assert_eq!(empty_simulator.get_average_entanglement_strength(), 0.0);
}

#[test]
fn test_simulation_result_structure() {
    let mut simulator = QuantumSimulator::new();
    simulator.generate_entangled_pair();
    simulator.observe_particle(0, true);
    simulator.quantum_teleportation(1, 3);
    
    let results = simulator.get_results();
    
    assert_eq!(results.pairs_generated, 1);
    assert_eq!(results.observations.len(), 1);
    assert_eq!(results.teleportations.len(), 1);
    assert!(!results.timestamp.is_empty());
}
