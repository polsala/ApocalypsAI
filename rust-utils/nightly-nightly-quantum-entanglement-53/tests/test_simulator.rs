use quantum_entanglement_simulator::*;
use std::sync::{Arc, Mutex};

#[test]
fn test_quantum_state_symbols() {
    assert_eq!(QuantumState::Up.to_symbol(), "↑");
    assert_eq!(QuantumState::Down.to_symbol(), "↓");
    assert_eq!(QuantumState::Superposition.to_symbol(), "?");
}

#[test]
fn test_entangled_pair_creation() {
    let pair = EntangledPair::new(1);
    
    // Initially both particles should be in superposition
    assert_eq!(*pair.particle_a.lock().unwrap(), QuantumState::Superposition);
    assert_eq!(*pair.particle_b.lock().unwrap(), QuantumState::Superposition);
    assert!(!*pair.is_measured.lock().unwrap());
}

#[test]
fn test_entangled_pair_measurement_strong() {
    let pair = EntangledPair::new(1);
    let (state_a, state_b) = pair.measure(1.0); // Perfect entanglement
    
    // With perfect entanglement, states should be opposite
    assert!(state_a != state_b);
    assert!(*pair.is_measured.lock().unwrap());
}

#[test]
fn test_entangled_pair_measurement_weak() {
    let pair = EntangledPair::new(1);
    let (state_a, state_b) = pair.measure(0.0); // No entanglement
    
    // With no entanglement, states could be same or different
    // Just verify measurement occurred
    assert!(*pair.is_measured.lock().unwrap());
}

#[test]
fn test_entangled_pair_display() {
    let pair = EntangledPair::new(1);
    let display = pair.display();
    
    assert!(display.contains("Particle Pair 1:"));
    assert!(display.contains("⟷"));
    assert!(display.contains("(Entangled)"));
    
    // After measurement
    pair.measure(1.0);
    let measured_display = pair.display();
    assert!(measured_display.contains("(Measured)"));
}

#[test]
fn test_simulator_creation() {
    let simulator = QuantumSimulator::new(3, 0.8, 0.5, 5);
    
    assert_eq!(simulator.pairs.len(), 3);
    assert_eq!(simulator.entanglement_strength, 0.8);
    assert_eq!(simulator.measurement_probability, 0.5);
    assert_eq!(simulator.duration, 5);
}

#[test]
fn test_entanglement_strength_clamping() {
    // Test that entanglement strength is properly clamped
    let simulator = QuantumSimulator::new(2, 1.5, 0.5, 5); // Above 1.0
    assert_eq!(simulator.entanglement_strength, 1.0);
    
    let simulator = QuantumSimulator::new(2, -0.5, 0.5, 5); // Below 0.0
    assert_eq!(simulator.entanglement_strength, 0.0);
}

#[test]
fn test_measurement_probability_clamping() {
    // Test that measurement probability is properly clamped
    let simulator = QuantumSimulator::new(2, 0.7, 1.2, 5); // Above 1.0
    assert_eq!(simulator.measurement_probability, 1.0);
    
    let simulator = QuantumSimulator::new(2, 0.7, -0.1, 5); // Below 0.0
    assert_eq!(simulator.measurement_probability, 0.0);
}

#[test]
fn test_minimum_particles() {
    // Test that at least 1 particle pair is created
    let simulator = QuantumSimulator::new(0, 0.7, 0.5, 5);
    assert_eq!(simulator.pairs.len(), 1);
    
    let simulator = QuantumSimulator::new(5, 0.7, 0.5, 5);
    assert_eq!(simulator.pairs.len(), 5);
}

// Mock rationale: These tests verify the core quantum mechanics simulation logic
// without requiring external dependencies or network calls. They test state
// transitions, entanglement behavior, and edge cases with deterministic inputs.
