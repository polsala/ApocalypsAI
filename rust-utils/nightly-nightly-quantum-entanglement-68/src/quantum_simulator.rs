use rand::Rng;
use std::f64::consts::PI;

/// Simulates quantum states and operations
pub struct QuantumSimulator {
    rng: rand::rngs::ThreadRng,
}

impl QuantumSimulator {
    pub fn new() -> Self {
        Self {
            rng: rand::thread_rng(),
        }
    }

    /// Generate a quantum state with the specified number of qubits
    pub fn generate_quantum_state(&mut self, qubit_count: usize) -> Vec<f64> {
        let mut state = Vec::with_capacity(qubit_count);
        
        for _ in 0..qubit_count {
            // Generate complex probability amplitudes
            let amplitude = self.rng.gen_range(-1.0..=1.0);
            state.push(amplitude);
        }
        
        // Normalize the state vector
        self.normalize_state(&mut state);
        state
    }

    /// Apply a quantum gate operation to a state
    pub fn apply_quantum_gate(&mut self, state: &mut Vec<f64>) {
        // Simulate applying a Hadamard-like gate
        for amplitude in state.iter_mut() {
            // Random phase rotation
            let phase = self.rng.gen_range(0.0..2.0 * PI);
            *amplitude *= phase.cos();
        }
        
        // Re-normalize
        self.normalize_state(state);
    }

    /// Introduce quantum decoherence to a state
    pub fn introduce_decoherence(&mut self, state: &mut Vec<f64>, decoherence_rate: f64) {
        for amplitude in state.iter_mut() {
            // Apply decoherence effect
            *amplitude *= 1.0 - (self.rng.gen_range(0.0..decoherence_rate));
        }
        
        // Re-normalize
        self.normalize_state(state);
    }

    /// Calculate quantum fidelity between two states
    pub fn calculate_fidelity(&self, state_a: &[f64], state_b: &[f64]) -> f64 {
        if state_a.len() != state_b.len() {
            return 0.0;
        }
        
        let dot_product: f64 = state_a.iter()
            .zip(state_b.iter())
            .map(|(a, b)| a * b)
            .sum();
        
        dot_product.abs()
    }

    /// Calculate Bell state fidelity
    pub fn calculate_bell_fidelity(&self, state_a: &[f64], state_b: &[f64]) -> f64 {
        if state_a.len() != state_b.len() {
            return 0.0;
        }
        
        // Simplified Bell state check
        let correlation: f64 = state_a.iter()
            .zip(state_b.iter())
            .map(|(a, b)| (a * b).abs())
            .sum();
        
        correlation / state_a.len() as f64
    }

    /// Normalize a quantum state vector
    fn normalize_state(&self, state: &mut Vec<f64>) {
        let norm: f64 = state.iter().map(|x| x.powi(2)).sum::<f64>().sqrt();
        if norm > 0.0 {
            for amplitude in state.iter_mut() {
                *amplitude /= norm;
            }
        }
    }
}
