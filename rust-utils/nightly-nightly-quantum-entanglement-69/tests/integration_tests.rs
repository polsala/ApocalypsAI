use nightly_quantum_entanglement_simulator::{QuantumSimulator, QuantumState};

#[test]
fn test_entanglement_simulation() {
    let mut simulator = QuantumSimulator::new(2);
    let result = simulator.simulate_entanglement();
    
    // Should have exactly 2 particles
    assert_eq!(result.particles.len(), 2);
    
    // Particles should be entangled (opposite states)
    let state1 = &result.particles[0].state;
    let state2 = &result.particles[1].state;
    
    match (state1, state2) {
        (QuantumState::Up, QuantumState::Down) => {},
        (QuantumState::Down, QuantumState::Up) => {},
        _ => panic!("Particles should be in opposite states for entanglement"),
    }
    
    // Entanglement strength should be high
    assert!(result.entanglement_strength > 90.0);
    
    // Should have explanation
    assert!(!result.explanation.is_empty());
}

#[test]
fn test_quantum_measurement() {
    let mut simulator = QuantumSimulator::new(1);
    let measurement = simulator.measure_particle();
    
    // Should have a definite state after measurement
    match measurement.state {
        QuantumState::Up | QuantumState::Down => {},
        QuantumState::Superposition => panic!("Measurement should collapse superposition"),
    }
    
    // Probability should be reasonable
    assert!(measurement.probability >= 0.0 && measurement.probability <= 1.0);
    
    // Should have a fun fact
    assert!(!measurement.fun_fact.is_empty());
}

#[test]
fn test_particle_coherence() {
    let mut simulator = QuantumSimulator::new(2);
    let result = simulator.simulate_entanglement();
    
    // Coherence should be high for fresh entanglement
    for particle in &result.particles {
        assert!(particle.coherence > 0.7);
        assert!(particle.coherence <= 1.0);
    }
}

#[test]
fn test_simulation_determinism() {
    // While the simulation is random, the structure should be consistent
    let mut simulator1 = QuantumSimulator::new(2);
    let mut simulator2 = QuantumSimulator::new(2);
    
    let result1 = simulator1.simulate_entanglement();
    let result2 = simulator2.simulate_entanglement();
    
    // Both should have 2 particles
    assert_eq!(result1.particles.len(), 2);
    assert_eq!(result2.particles.len(), 2);
    
    // Both should have explanations
    assert!(!result1.explanation.is_empty());
    assert!(!result2.explanation.is_empty());
    
    // Both should have high entanglement strength
    assert!(result1.entanglement_strength > 90.0);
    assert!(result2.entanglement_strength > 90.0);
}
