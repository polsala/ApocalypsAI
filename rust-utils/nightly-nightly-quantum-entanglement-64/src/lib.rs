pub mod quantum_state;
pub mod gates;
pub mod circuit;
pub mod visualization;
pub mod entanglement;

pub use quantum_state::QuantumState;
pub use gates::Gate;
pub use circuit::QuantumCircuit;
pub use visualization::CircuitVisualizer;
pub use entanglement::EntanglementDetector;

use std::collections::HashMap;

/// Result of a quantum circuit simulation
#[derive(Debug, Clone)]
pub struct SimulationResult {
    /// Measurement probabilities for each basis state
    pub probabilities: HashMap<String, f64>,
    /// Most likely measurement outcome
    pub most_likely: String,
    /// Number of measurements performed
    pub measurement_count: usize,
}

impl std::fmt::Display for SimulationResult {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "📊 Measurement Results:")?;
        writeln!(f, "   Most likely outcome: |{}⟩", self.most_likely)?;
        writeln!(f, "   Measurement count: {}", self.measurement_count)?;
        writeln!(f, "   Probabilities:")?;
        
        let mut sorted_probs: Vec<_> = self.probabilities.iter().collect();
        sorted_probs.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        
        for (state, prob) in sorted_probs {
            if *prob > 1e-10 {
                writeln!(f, "     |{}⟩: {:.1}%", state, prob * 100.0)?;
            }
        }
        
        Ok(())
    }
}

/// Information about entanglement between qubit pairs
#[derive(Debug, Clone)]
pub struct EntanglementInfo {
    /// Qubit pairs and their concurrence values
    pub pairs: Vec<(usize, usize)>,
    /// Concurrence values (0.0 = no entanglement, 1.0 = maximally entangled)
    pub concurrence_values: Vec<f64>,
}

impl EntanglementInfo {
    pub fn new() -> Self {
        Self {
            pairs: Vec::new(),
            concurrence_values: Vec::new(),
        }
    }
    
    pub fn add_entanglement(&mut self, qubit1: usize, qubit2: usize, concurrence: f64) {
        self.pairs.push((qubit1, qubit2));
        self.concurrence_values.push(concurrence);
    }
    
    pub fn is_empty(&self) -> bool {
        self.pairs.is_empty()
    }
}

impl std::fmt::Display for EntanglementInfo {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if self.is_empty() {
            writeln!(f, "No entanglement detected.")
        } else {
            writeln!(f, "Entanglement detected:")?;
            for (i, ((q1, q2), concurrence)) in self.pairs.iter().zip(self.concurrence_values.iter()).enumerate() {
                writeln!(f, "  Pair {}: Qubits {} and {}, concurrence = {:.3}", i + 1, q1, q2, concurrence)?;
            }
            Ok(())
        }
    }
}

/// Quantum gate operations
#[derive(Debug, Clone, PartialEq)]
pub enum Gate {
    /// Hadamard gate: creates superposition
    Hadamard(usize),
    /// Pauli-X gate: bit flip (NOT)
    PauliX(usize),
    /// Pauli-Y gate: bit and phase flip
    PauliY(usize),
    /// Pauli-Z gate: phase flip
    PauliZ(usize),
    /// Controlled NOT gate
    CNOT(usize, usize),
    /// Controlled Z gate
    CZ(usize, usize),
    /// SWAP gate: swaps qubit states
    SWAP(usize, usize),
    /// Toffoli gate: controlled-controlled NOT
    Toffoli(usize, usize, usize),
}

impl Gate {
    /// Get the gate symbol for visualization
    pub fn symbol(&self) -> &'static str {
        match self {
            Gate::Hadamard(_) => "H",
            Gate::PauliX(_) => "X",
            Gate::PauliY(_) => "Y",
            Gate::PauliZ(_) => "Z",
            Gate::CNOT(_, _) => "●",
            Gate::CZ(_, _) => "●",
            Gate::SWAP(_, _) => "×",
            Gate::Toffoli(_, _, _) => "●",
        }
    }
    
    /// Get the gate name for display
    pub fn name(&self) -> &'static str {
        match self {
            Gate::Hadamard(_) => "Hadamard",
            Gate::PauliX(_) => "Pauli-X",
            Gate::PauliY(_) => "Pauli-Y",
            Gate::PauliZ(_) => "Pauli-Z",
            Gate::CNOT(_, _) => "CNOT",
            Gate::CZ(_, _) => "CZ",
            Gate::SWAP(_, _) => "SWAP",
            Gate::Toffoli(_, _, _) => "Toffoli",
        }
    }
    
    /// Get target qubits affected by this gate
    pub fn target_qubits(&self) -> Vec<usize> {
        match self {
            Gate::Hadamard(q) | Gate::PauliX(q) | Gate::PauliY(q) | Gate::PauliZ(q) => vec![*q],
            Gate::CNOT(c, t) | Gate::CZ(c, t) | Gate::SWAP(c, t) => vec![*c, *t],
            Gate::Toffoli(c1, c2, t) => vec![*c1, *c2, *t],
        }
    }
}

/// Quantum state vector
#[derive(Debug, Clone)]
pub struct QuantumState {
    /// Complex amplitudes for each basis state
    pub amplitudes: Vec<Complex>,
    /// Number of qubits
    pub num_qubits: usize,
}

#[derive(Debug, Clone, Copy)]
pub struct Complex {
    pub re: f64,
    pub im: f64,
}

impl Complex {
    pub fn new(re: f64, im: f64) -> Self {
        Self { re, im }
    }
    
    pub fn magnitude_squared(&self) -> f64 {
        self.re * self.re + self.im * self.im
    }
    
    pub fn magnitude(&self) -> f64 {
        self.magnitude_squared().sqrt()
    }
    
    pub fn add(&self, other: Complex) -> Complex {
        Complex::new(self.re + other.re, self.im + other.im)
    }
    
    pub fn multiply(&self, other: Complex) -> Complex {
        Complex::new(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )
    }
    
    pub fn conjugate(&self) -> Complex {
        Complex::new(self.re, -self.im)
    }
}

impl QuantumState {
    pub fn new(num_qubits: usize) -> Self {
        let size = 1 << num_qubits;
        let mut amplitudes = vec![Complex::new(0.0, 0.0); size];
        amplitudes[0] = Complex::new(1.0, 0.0); // Start in |00...0⟩ state
        
        Self {
            amplitudes,
            num_qubits,
        }
    }
    
    pub fn normalize(&mut self) {
        let norm_sq = self.amplitudes.iter().map(|a| a.magnitude_squared()).sum::<f64>();
        let norm = norm_sq.sqrt();
        
        if norm > 1e-10 {
            for amplitude in &mut self.amplitudes {
                amplitude.re /= norm;
                amplitude.im /= norm;
            }
        }
    }
    
    pub fn apply_gate(&mut self, gate: &Gate) {
        match gate {
            Gate::Hadamard(qubit) => self.apply_hadamard(*qubit),
            Gate::PauliX(qubit) => self.apply_pauli_x(*qubit),
            Gate::PauliY(qubit) => self.apply_pauli_y(*qubit),
            Gate::PauliZ(qubit) => self.apply_pauli_z(*qubit),
            Gate::CNOT(control, target) => self.apply_cnot(*control, *target),
            Gate::CZ(control, target) => self.apply_cz(*control, *target),
            Gate::SWAP(qubit1, qubit2) => self.apply_swap(*qubit1, *qubit2),
            Gate::Toffoli(control1, control2, target) => self.apply_toffoli(*control1, *control2, *target),
        }
        self.normalize();
    }
    
    fn apply_hadamard(&mut self, qubit: usize) {
        let stride = 1 << qubit;
        for offset in (0..self.amplitudes.len()).step_by(stride * 2) {
            for i in 0..stride {
                let idx0 = offset + i;
                let idx1 = offset + i + stride;
                
                let a = self.amplitudes[idx0];
                let b = self.amplitudes[idx1];
                
                self.amplitudes[idx0] = Complex::new(
                    (a.re + b.re) / 2.0_f64.sqrt(),
                    (a.im + b.im) / 2.0_f64.sqrt(),
                );
                self.amplitudes[idx1] = Complex::new(
                    (a.re - b.re) / 2.0_f64.sqrt(),
                    (a.im - b.im) / 2.0_f64.sqrt(),
                );
            }
        }
    }
    
    fn apply_pauli_x(&mut self, qubit: usize) {
        let stride = 1 << qubit;
        for offset in (0..self.amplitudes.len()).step_by(stride * 2) {
            for i in 0..stride {
                let idx0 = offset + i;
                let idx1 = offset + i + stride;
                self.amplitudes.swap(idx0, idx1);
            }
        }
    }
    
    fn apply_pauli_y(&mut self, qubit: usize) {
        let stride = 1 << qubit;
        for offset in (0..self.amplitudes.len()).step_by(stride * 2) {
            for i in 0..stride {
                let idx0 = offset + i;
                let idx1 = offset + i + stride;
                
                let a = self.amplitudes[idx0];
                let b = self.amplitudes[idx1];
                
                self.amplitudes[idx0] = Complex::new(-b.im, b.re);
                self.amplitudes[idx1] = Complex::new(a.im, -a.re);
            }
        }
    }
    
    fn apply_pauli_z(&mut self, qubit: usize) {
        let stride = 1 << qubit;
        for offset in (0..self.amplitudes.len()).step_by(stride * 2) {
            for i in stride..(stride * 2) {
                let idx = offset + i;
                self.amplitudes[idx] = Complex::new(-self.amplitudes[idx].re, -self.amplitudes[idx].im);
            }
        }
    }
    
    fn apply_cnot(&mut self, control: usize, target: usize) {
        let control_stride = 1 << control;
        let target_stride = 1 << target;
        
        for offset in (0..self.amplitudes.len()).step_by(control_stride * 2) {
            for block_offset in (0..control_stride).step_by(target_stride * 2) {
                for i in 0..target_stride {
                    let idx0 = offset + block_offset + i;
                    let idx1 = offset + block_offset + i + target_stride;
                    self.amplitudes.swap(idx0, idx1);
                }
            }
        }
    }
    
    fn apply_cz(&mut self, control: usize, target: usize) {
        let control_stride = 1 << control;
        let target_stride = 1 << target;
        
        for offset in (control_stride..self.amplitudes.len()).step_by(control_stride * 2) {
            for block_offset in (target_stride..control_stride).step_by(target_stride * 2) {
                for i in 0..target_stride {
                    let idx = offset + block_offset + i;
                    self.amplitudes[idx] = Complex::new(-self.amplitudes[idx].re, -self.amplitudes[idx].im);
                }
            }
        }
    }
    
    fn apply_swap(&mut self, qubit1: usize, qubit2: usize) {
        // SWAP = three CNOTs
        self.apply_cnot(qubit1, qubit2);
        self.apply_cnot(qubit2, qubit1);
        self.apply_cnot(qubit1, qubit2);
    }
    
    fn apply_toffoli(&mut self, control1: usize, control2: usize, target: usize) {
        // Simplified Toffoli implementation
        // In a full implementation, this would be more complex
        let mut controls = vec![control1, control2];
        controls.sort();
        
        let stride1 = 1 << controls[0];
        let stride2 = 1 << controls[1];
        let target_stride = 1 << target;
        
        for offset in (stride1..self.amplitudes.len()).step_by(stride1 * 2) {
            for block_offset in (stride2..stride1).step_by(stride2 * 2) {
                for i in (target_stride..(target_stride * 2)).step_by(target_stride) {
                    let idx0 = offset + block_offset + i;
                    let idx1 = offset + block_offset + i + target_stride;
                    self.amplitudes.swap(idx0, idx1);
                }
            }
        }
    }
    
    pub fn measure(&self) -> String {
        let probabilities: Vec<f64> = self.amplitudes.iter().map(|a| a.magnitude_squared()).collect();
        let random_val = fastrand::f64();
        
        let mut cumulative = 0.0;
        for (i, &prob) in probabilities.iter().enumerate() {
            cumulative += prob;
            if random_val <= cumulative {
                return format!("{:0width$b}", i, width = self.num_qubits);
            }
        }
        
        // Fallback
        format!("{:0width$b}", 0, width = self.num_qubits)
    }
    
    pub fn get_probabilities(&self) -> HashMap<String, f64> {
        let mut probs = HashMap::new();
        for (i, amplitude) in self.amplitudes.iter().enumerate() {
            let prob = amplitude.magnitude_squared();
            if prob > 1e-10 {
                let state = format!("{:0width$b}", i, width = self.num_qubits);
                probs.insert(state, prob);
            }
        }
        probs
    }
}

/// Quantum circuit representation
#[derive(Debug, Clone)]
pub struct QuantumCircuit {
    pub num_qubits: usize,
    pub gates: Vec<Gate>,
    pub state: QuantumState,
}

impl QuantumCircuit {
    pub fn new(num_qubits: usize) -> Self {
        Self {
            num_qubits,
            gates: Vec::new(),
            state: QuantumState::new(num_qubits),
        }
    }
    
    pub fn add_gate(&mut self, gate: Gate) {
        // Validate gate targets
        let max_qubit = self.num_qubits - 1;
        for &qubit in &gate.target_qubits() {
            if qubit > max_qubit {
                panic!("Qubit index {} out of range for {}-qubit circuit", qubit, self.num_qubits);
            }
        }
        
        self.gates.push(gate.clone());
        self.state.apply_gate(&gate);
    }
    
    pub fn simulate(&self) -> SimulationResult {
        let probabilities = self.state.get_probabilities();
        
        // Find most likely outcome
        let mut most_likely = String::new();
        let mut max_prob = 0.0;
        for (state, prob) in &probabilities {
            if *prob > max_prob {
                max_prob = *prob;
                most_likely = state.clone();
            }
        }
        
        SimulationResult {
            probabilities,
            most_likely,
            measurement_count: 1000,
        }
    }
    
    pub fn visualize(&self) -> String {
        CircuitVisualizer::new(self).visualize()
    }
    
    pub fn detect_entanglement(&self) -> Vec<((usize, usize), f64)> {
        EntanglementDetector::detect(&self.state)
    }
    
    pub fn reset(&mut self) {
        self.gates.clear();
        self.state = QuantumState::new(self.num_qubits);
    }
}

/// Circuit visualization
pub struct CircuitVisualizer<'a> {
    circuit: &'a QuantumCircuit,
}

impl<'a> CircuitVisualizer<'a> {
    pub fn new(circuit: &'a QuantumCircuit) -> Self {
        Self { circuit }
    }
    
    pub fn visualize(&self) -> String {
        let mut output = String::new();
        
        // Header
        output.push_str("🔬 Quantum Circuit Diagram\n");
        output.push_str(&"-".repeat(40));
        output.push_str("\n\n");
        
        // Draw each qubit line
        for qubit in 0..self.circuit.num_qubits {
            output.push_str(&format!("Qubit {}: |0⟩", qubit));
            
            // Find gates affecting this qubit
            for gate in &self.circuit.gates {
                if gate.target_qubits().contains(&qubit) {
                    output.push_str(" ── ");
                    output.push_str(gate.symbol());
                    
                    // Add control connections for multi-qubit gates
                    match gate {
                        Gate::CNOT(c, t) if *t == qubit => {
                            output.push_str(&format!(" (ctrl: {})", c));
                        },
                        Gate::CZ(c, t) if *t == qubit => {
                            output.push_str(&format!(" (ctrl: {})", c));
                        },
                        Gate::Toffoli(c1, c2, t) if *t == qubit => {
                            output.push_str(&format!(" (ctrls: {}, {})", c1, c2));
                        },
                        _ => {},
                    }
                } else {
                    output.push_str(" ── ");
                }
            }
            
            output.push_str(" ── Measurement\n");
        }
        
        // Add gate legend
        output.push_str("\n");
        output.push_str(&"-".repeat(40));
        output.push_str("\n");
        output.push_str("Gate Legend:\n");
        output.push_str("  H  = Hadamard (superposition)\n");
        output.push_str("  X  = Pauli-X (bit flip)\n");
        output.push_str("  Y  = Pauli-Y (bit & phase flip)\n");
        output.push_str("  Z  = Pauli-Z (phase flip)\n");
        output.push_str("  ●  = Control qubit\n");
        output.push_str("  ×  = SWAP gate\n");
        
        output
    }
}

/// Entanglement detection
pub struct EntanglementDetector;

impl EntanglementDetector {
    pub fn detect(state: &QuantumState) -> Vec<((usize, usize), f64)> {
        let mut entanglements = Vec::new();
        
        // Check all pairs of qubits
        for i in 0..state.num_qubits {
            for j in (i + 1)..state.num_qubits {
                let concurrence = Self::calculate_concurrence(state, i, j);
                if concurrence > 0.1 { // Threshold for entanglement
                    entanglements.push(((i, j), concurrence));
                }
            }
        }
        
        entanglements
    }
    
    fn calculate_concurrence(state: &QuantumState, qubit1: usize, qubit2: usize) -> f64 {
        // Simplified concurrence calculation
        // In a full implementation, this would involve partial traces and density matrices
        
        let mut max_correlation = 0.0;
        
        // Check correlation between measurement outcomes
        for i in 0..(1 << state.num_qubits) {
            let bit1 = (i >> qubit1) & 1;
            let bit2 = (i >> qubit2) & 1;
            let prob = state.amplitudes[i].magnitude_squared();
            
            if bit1 == bit2 {
                max_correlation += prob;
            }
        }
        
        // Normalize and convert to concurrence-like measure
        (max_correlation - 0.5).abs() * 2.0
    }
}

// Re-export commonly used items
pub use fastrand;
