use nightly_quantum_entanglement_simulator::*;
use quantum_state::QuantumState;

#[test]
fn test_bell_state_creation() {
    let mut circuit = circuit::QuantumCircuit::new();
    
    // Create Bell state: H(0), CNOT(0,1)
    circuit.apply_gate(circuit::QuantumGate::SingleQubit {
        qubit: 0,
        gate: quantum_state::QubitGate::Hadamard,
    });
    
    circuit.apply_gate(circuit::QuantumGate::TwoQubit {
        control: 0,
        target: 1,
        gate: quantum_state::TwoQubitGate::CNOT,
    });
    
    let state = circuit.get_state();
    
    // Bell state should have equal probability of |00⟩ and |11⟩
    let prob_00 = state.get_probability(0); // |00⟩
    let prob_11 = state.get_probability(3); // |11⟩
    
    assert!((prob_00 - 0.5).abs() < 1e-10);
    assert!((prob_11 - 0.5).abs() < 1e-10);
    
    // Other states should have zero probability
    assert!(state.get_probability(1).abs() < 1e-10); // |01⟩
    assert!(state.get_probability(2).abs() < 1e-10); // |10⟩
}

#[test]
fn test_single_qubit_gates() {
    let mut circuit = circuit::QuantumCircuit::new();
    
    // Start with |0⟩
    let state = circuit.get_state();
    assert!((state.get_probability(0) - 1.0).abs() < 1e-10);
    
    // Apply Hadamard gate
    circuit.apply_gate(circuit::QuantumGate::SingleQubit {
        qubit: 0,
        gate: quantum_state::QubitGate::Hadamard,
    });
    
    let state = circuit.get_state();
    assert!((state.get_probability(0) - 0.5).abs() < 1e-10);
    assert!((state.get_probability(1) - 0.5).abs() < 1e-10);
    
    // Apply Pauli-X gate (should flip to |1⟩)
    circuit.apply_gate(circuit::QuantumGate::SingleQubit {
        qubit: 0,
        gate: quantum_state::QubitGate::PauliX,
    });
    
    let state = circuit.get_state();
    assert!(state.get_probability(0).abs() < 1e-10);
    assert!((state.get_probability(1) - 1.0).abs() < 1e-10);
}

#[test]
fn test_entanglement_detection() {
    let mut circuit = circuit::QuantumCircuit::new();
    
    // Create entangled state
    circuit.apply_gate(circuit::QuantumGate::SingleQubit {
        qubit: 0,
        gate: quantum_state::QubitGate::Hadamard,
    });
    
    circuit.apply_gate(circuit::QuantumGate::TwoQubit {
        control: 0,
        target: 1,
        gate: quantum_state::TwoQubitGate::CNOT,
    });
    
    let state = circuit.get_state();
    let visualizer = visualization::QuantumVisualizer::new();
    
    // Should detect entanglement between qubits 0 and 1
    let entangled_pairs = visualizer.detect_entanglement(state, 2);
    assert!(entangled_pairs.contains(&(0, 1)));
}
