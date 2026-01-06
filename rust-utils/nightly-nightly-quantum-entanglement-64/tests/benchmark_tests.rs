use nightly_quantum_entanglement_simulator::*;
use std::time::Instant;

#[test]
fn benchmark_bell_state_simulation() {
    let start = Instant::now();
    
    for _ in 0..1000 {
        let mut circuit = QuantumCircuit::new(2);
        circuit.add_gate(Gate::Hadamard(0));
        circuit.add_gate(Gate::CNOT(0, 1));
        let _result = circuit.simulate();
    }
    
    let duration = start.elapsed();
    println!("Bell state simulation (1000 iterations): {:?}", duration);
    
    // Should complete in reasonable time (less than 1 second for 1000 iterations)
    assert!(duration.as_secs() < 1);
}

#[test]
fn benchmark_ghz_state_simulation() {
    let start = Instant::now();
    
    for _ in 0..100 {
        let mut circuit = QuantumCircuit::new(4);
        circuit.add_gate(Gate::Hadamard(0));
        circuit.add_gate(Gate::CNOT(0, 1));
        circuit.add_gate(Gate::CNOT(1, 2));
        circuit.add_gate(Gate::CNOT(2, 3));
        let _result = circuit.simulate();
    }
    
    let duration = start.elapsed();
    println!("4-qubit GHZ state simulation (100 iterations): {:?}", duration);
    
    // Should complete in reasonable time
    assert!(duration.as_secs() < 5);
}

#[test]
fn benchmark_entanglement_detection() {
    let mut circuit = QuantumCircuit::new(3);
    circuit.add_gate(Gate::Hadamard(0));
    circuit.add_gate(Gate::CNOT(0, 1));
    circuit.add_gate(Gate::CNOT(1, 2));
    
    let start = Instant::now();
    
    for _ in 0..1000 {
        let _entanglements = circuit.detect_entanglement();
    }
    
    let duration = start.elapsed();
    println!("Entanglement detection (1000 iterations): {:?}", duration);
    
    // Should be fast
    assert!(duration.as_millis() < 1000);
}

#[test]
fn benchmark_large_circuit() {
    // Test with a larger circuit to see performance characteristics
    let start = Instant::now();
    
    let mut circuit = QuantumCircuit::new(5); // 32 amplitudes
    for _ in 0..10 {
        circuit.add_gate(Gate::Hadamard(0));
        circuit.add_gate(Gate::CNOT(0, 1));
        circuit.add_gate(Gate::CNOT(1, 2));
        circuit.add_gate(Gate::CNOT(2, 3));
        circuit.add_gate(Gate::CNOT(3, 4));
    }
    
    let _result = circuit.simulate();
    let duration = start.elapsed();
    
    println!("Large circuit simulation: {:?}", duration);
    
    // Should complete in reasonable time for demonstration purposes
    assert!(duration.as_secs() < 10);
}

#[test]
fn benchmark_random_circuit_generation() {
    let start = Instant::now();
    
    for _ in 0..100 {
        let mut rng = fastrand::Rng::new();
        let circuit = create_random_circuit(3, 5, &mut rng);
        let _result = circuit.simulate();
    }
    
    let duration = start.elapsed();
    println!("Random circuit generation and simulation (100 iterations): {:?}", duration);
    
    // Should be reasonably fast
    assert!(duration.as_secs() < 5);
}

// Helper function for benchmark tests
fn create_random_circuit(num_qubits: usize, depth: usize, rng: &mut fastrand::Rng) -> QuantumCircuit {
    let mut circuit = QuantumCircuit::new(num_qubits);
    
    for _ in 0..depth {
        let gate_type = rng.u32(..100);
        
        match gate_type {
            0..=30 => {
                let qubit = rng.usize(..num_qubits);
                let gate = match rng.u32(..4) {
                    0 => Gate::Hadamard(qubit),
                    1 => Gate::PauliX(qubit),
                    2 => Gate::PauliY(qubit),
                    _ => Gate::PauliZ(qubit),
                };
                circuit.add_gate(gate);
            },
            31..=70 => {
                if num_qubits >= 2 {
                    let control = rng.usize(..num_qubits);
                    let target = loop {
                        let t = rng.usize(..num_qubits);
                        if t != control { break t; }
                    };
                    let gate = match rng.u32(..3) {
                        0 => Gate::CNOT(control, target),
                        1 => Gate::CZ(control, target),
                        _ => Gate::SWAP(control, target),
                    };
                    circuit.add_gate(gate);
                }
            },
            71..=100 => {
                if num_qubits >= 3 {
                    let control1 = rng.usize(..num_qubits);
                    let control2 = loop {
                        let c = rng.usize(..num_qubits);
                        if c != control1 { break c; }
                    };
                    let target = loop {
                        let t = rng.usize(..num_qubits);
                        if t != control1 && t != control2 { break t; }
                    };
                    circuit.add_gate(Gate::Toffoli(control1, control2, target));
                }
            },
        }
    }
    
    circuit
}
