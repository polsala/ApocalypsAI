use std::collections::HashMap;
use num_complex::Complex;
use rand::Rng;

use crate::quantum_state::{QuantumState, QubitGate, TwoQubitGate};

#[derive(Debug, Clone)]
pub enum QuantumGate {
    SingleQubit { qubit: usize, gate: QubitGate },
    TwoQubit { control: usize, target: usize, gate: TwoQubitGate },
}

pub struct QuantumCircuit {
    state: QuantumState,
    num_qubits: usize,
}

impl QuantumCircuit {
    pub fn new() -> Self {
        Self {
            state: QuantumState::new(1), // Start with 1 qubit
            num_qubits: 1,
        }
    }
    
    pub fn get_num_qubits(&self) -> usize {
        self.num_qubits
    }
    
    pub fn get_state(&self) -> &QuantumState {
        &self.state
    }
    
    pub fn apply_gate(&mut self, gate: QuantumGate) {
        match gate {
            QuantumGate::SingleQubit { qubit, gate } => {
                self.ensure_qubit_capacity(qubit);
                self.state.apply_single_qubit_gate(qubit, gate);
            },
            QuantumGate::TwoQubit { control, target, gate } => {
                self.ensure_qubit_capacity(control.max(target));
                self.state.apply_two_qubit_gate(control, target, gate);
            },
        }
    }
    
    pub fn measure(&mut self, qubit: usize) -> bool {
        if qubit >= self.num_qubits {
            panic!("Qubit {} does not exist (max: {})", qubit, self.num_qubits - 1);
        }
        
        let result = self.state.measure(qubit);
        
        // After measurement, the state collapses
        // For simplicity, we'll keep the full state but note that it's now in a definite state
        result
    }
    
    fn ensure_qubit_capacity(&mut self, qubit_index: usize) {
        if qubit_index >= self.num_qubits {
            let new_num_qubits = qubit_index + 1;
            self.state = self.state.expand_to_qubits(new_num_qubits);
            self.num_qubits = new_num_qubits;
        }
    }
}

impl Default for QuantumCircuit {
    fn default() -> Self {
        Self::new()
    }
}
