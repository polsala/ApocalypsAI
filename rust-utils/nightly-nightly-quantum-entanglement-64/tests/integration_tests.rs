use nightly_quantum_entanglement_simulator::*;
use std::collections::HashMap;

#[test]
fn test_bell_state_creation() {
    let mut circuit = QuantumCircuit::new(2);
    circuit.add_gate(Gate::Hadamard(0));
    circuit.add_gate(Gate::CNOT(0, 1));
    
    let result = circuit.simulate();
    
    // Bell state should have equal probabilities for |00⟩ and |11⟩
    assert!(result.probabilities.contains_key("00"));
    assert!(result.probabilities.contains_key("11"));
    assert!(!result.probabilities.contains_key("01"));
    assert!(!result.probabilities.contains_key("10"));
    
    let p00 = result.probabilities.get("00").unwrap();
    let p11 = result.probabilities.get("11").unwrap();
    assert!((p00 - 0.5).abs() < 1e-10);
    assert!((p11 - 0.5).abs() < 1e-10);
}

#[test]
fn test_bell_state_entanglement() {
    let mut circuit = QuantumCircuit::new(2);
    circuit.add_gate(Gate::Hadamard(0));
    circuit.add_gate(Gate::CNOT(0, 1));
    
    let entanglements = circuit.detect_entanglement();
    assert_eq!(entanglements.len(), 1);
    assert_eq!(entanglements[0].0, (0, 1));
    assert!(entanglements[0].1 > 0.9); // High concurrence for Bell state
}

#[test]
fn test_single_qubit_gates() {
    let mut circuit = QuantumCircuit::new(1);
    circuit.add_gate(Gate::Hadamard(0));
    
    let result = circuit.simulate();
    
    assert!(result.probabilities.contains_key("0"));
    assert!(result.probabilities.contains_key("1"));
    
    let p0 = result.probabilities.get("0").unwrap();
    let p1 = result.probabilities.get("1").unwrap();
    assert!((p0 - 0.5).abs() < 1e-10);
    assert!((p1 - 0.5).abs() < 1e-10);
}

#[test]
fn test_pauli_x_gate() {
    let mut circuit = QuantumCircuit::new(1);
    circuit.add_gate(Gate::PauliX(0));
    
    let result = circuit.simulate();
    
    assert!(result.probabilities.contains_key("1"));
    assert!(!result.probabilities.contains_key("0"));
    
    let p1 = result.probabilities.get("1").unwrap();
    assert!((p1 - 1.0).abs() < 1e-10);
}

#[test]
fn test_ghz_state() {
    let mut circuit = QuantumCircuit::new(3);
    circuit.add_gate(Gate::Hadamard(0));
    circuit.add_gate(Gate::CNOT(0, 1));
    circuit.add_gate(Gate::CNOT(1, 2));
    
    let result = circuit.simulate();
    
    // GHZ state should have equal probabilities for |000⟩ and |111⟩
    assert!(result.probabilities.contains_key("000"));
    assert!(result.probabilities.contains_key("111"));
    assert!(!result.probabilities.contains_key("001"));
    assert!(!result.probabilities.contains_key("010"));
    assert!(!result.probabilities.contains_key("011"));
    assert!(!result.probabilities.contains_key("100"));
    assert!(!result.probabilities.contains_key("101"));
    assert!(!result.probabilities.contains_key("110"));
    
    let p000 = result.probabilities.get("000").unwrap();
    let p111 = result.probabilities.get("111").unwrap();
    assert!((p000 - 0.5).abs() < 1e-10);
    assert!((p111 - 0.5).abs() < 1e-10);
}

#[test]
fn test_entanglement_detection() {
    // Test separable state (no entanglement)
    let mut circuit = QuantumCircuit::new(2);
    circuit.add_gate(Gate::Hadamard(0));
    circuit.add_gate(Gate::Hadamard(1));
    
    let entanglements = circuit.detect_entanglement();
    assert!(entanglements.is_empty());
    
    // Test entangled state
    let mut circuit = QuantumCircuit::new(2);
    circuit.add_gate(Gate::Hadamard(0));
    circuit.add_gate(Gate::CNOT(0, 1));
    
    let entanglements = circuit.detect_entanglement();
    assert!(!entanglements.is_empty());
    assert!(entanglements[0].1 > 0.5); // Should have high concurrence
}

#[test]
fn test_circuit_visualization() {
    let mut circuit = QuantumCircuit::new(2);
    circuit.add_gate(Gate::Hadamard(0));
    circuit.add_gate(Gate::CNOT(0, 1));
    
    let visualization = circuit.visualize();
    
    // Check that visualization contains expected elements
    assert!(visualization.contains("Qubit 0:"));
    assert!(visualization.contains("Qubit 1:"));
    assert!(visualization.contains("H"));
    assert!(visualization.contains("●"));
    assert!(visualization.contains("Measurement"));
}

#[test]
fn test_complex_arithmetic() {
    let c1 = Complex::new(1.0, 2.0);
    let c2 = Complex::new(3.0, 4.0);
    
    let sum = c1.add(c2);
    assert!((sum.re - 4.0).abs() < 1e-10);
    assert!((sum.im - 6.0).abs() < 1e-10);
    
    let product = c1.multiply(c2);
    assert!((product.re - (-5.0)).abs() < 1e-10); // (1*3 - 2*4) = -5
    assert!((product.im - 10.0).abs() < 1e-10);  // (1*4 + 2*3) = 10
    
    let conjugate = c1.conjugate();
    assert!((conjugate.re - 1.0).abs() < 1e-10);
    assert!((conjugate.im - (-2.0)).abs() < 1e-10);
}

#[test]
fn test_state_normalization() {
    let mut state = QuantumState::new(1);
    state.amplitudes[0] = Complex::new(1.0, 0.0);
    state.amplitudes[1] = Complex::new(1.0, 0.0);
    
    state.normalize();
    
    let norm_sq = state.amplitudes.iter().map(|a| a.magnitude_squared()).sum::<f64>();
    assert!((norm_sq - 1.0).abs() < 1e-10);
}

#[test]
fn test_measurement_probabilities() {
    let mut state = QuantumState::new(2);
    state.amplitudes[0] = Complex::new(1.0, 0.0); // |00⟩
    state.amplitudes[1] = Complex::new(0.0, 0.0);
    state.amplitudes[2] = Complex::new(0.0, 0.0);
    state.amplitudes[3] = Complex::new(0.0, 0.0);
    
    let probs = state.get_probabilities();
    assert_eq!(probs.len(), 1);
    assert!(probs.contains_key("00"));
    assert!((probs.get("00").unwrap() - 1.0).abs() < 1e-10);
}

#[test]
fn test_gate_target_validation() {
    let mut circuit = QuantumCircuit::new(2);
    
    // Valid gates should work
    circuit.add_gate(Gate::Hadamard(0));
    circuit.add_gate(Gate::CNOT(0, 1));
    
    // Invalid gate should panic
    let result = std::panic::catch_unwind(|| {
        circuit.add_gate(Gate::Hadamard(2)); // Qubit 2 doesn't exist in 2-qubit circuit
    });
    assert!(result.is_err());
}

#[test]
fn test_circuit_reset() {
    let mut circuit = QuantumCircuit::new(2);
    circuit.add_gate(Gate::Hadamard(0));
    circuit.add_gate(Gate::CNOT(0, 1));
    
    assert_eq!(circuit.gates.len(), 2);
    
    circuit.reset();
    
    assert_eq!(circuit.gates.len(), 0);
    assert_eq!(circuit.state.amplitudes[0].re, 1.0);
    assert_eq!(circuit.state.amplitudes[1].re, 0.0);
}
