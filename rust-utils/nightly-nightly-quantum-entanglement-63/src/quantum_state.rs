use std::fmt;
use num_complex::Complex;
use rand::Rng;

#[derive(Debug, Clone, Copy)]
pub enum QubitGate {
    Hadamard,
    PauliX,
    PauliY,
    PauliZ,
    PhaseS,
    PhaseT,
}

#[derive(Debug, Clone, Copy)]
pub enum TwoQubitGate {
    CNOT,
}

#[derive(Debug, Clone)]
pub struct QuantumState {
    amplitudes: Vec<Complex<f64>>,
    num_qubits: usize,
}

impl QuantumState {
    pub fn new(num_qubits: usize) -> Self {
        let size = 1 << num_qubits;
        let mut amplitudes = vec![Complex::new(0.0, 0.0); size];
        amplitudes[0] = Complex::new(1.0, 0.0); // Start in |000...⟩ state
        
        Self {
            amplitudes,
            num_qubits,
        }
    }
    
    pub fn get_num_qubits(&self) -> usize {
        self.num_qubits
    }
    
    pub fn get_amplitude(&self, index: usize) -> Complex<f64> {
        self.amplitudes[index]
    }
    
    pub fn get_probability(&self, index: usize) -> f64 {
        self.amplitudes[index].norm_sqr()
    }
    
    pub fn measure(&self, qubit: usize) -> bool {
        if qubit >= self.num_qubits {
            panic!("Qubit {} does not exist", qubit);
        }
        
        let mut prob_0 = 0.0;
        let mut prob_1 = 0.0;
        
        for (i, amplitude) in self.amplitudes.iter().enumerate() {
            let prob = amplitude.norm_sqr();
            if (i >> qubit) & 1 == 0 {
                prob_0 += prob;
            } else {
                prob_1 += prob;
            }
        }
        
        let mut rng = rand::thread_rng();
        let roll = rng.gen::<f64>();
        
        roll > prob_0
    }
    
    pub fn apply_single_qubit_gate(&mut self, qubit: usize, gate: QubitGate) {
        let gate_matrix = match gate {
            QubitGate::Hadamard => self.hadamard_matrix(),
            QubitGate::PauliX => self.pauli_x_matrix(),
            QubitGate::PauliY => self.pauli_y_matrix(),
            QubitGate::PauliZ => self.pauli_z_matrix(),
            QubitGate::PhaseS => self.phase_s_matrix(),
            QubitGate::PhaseT => self.phase_t_matrix(),
        };
        
        self.apply_single_qubit_matrix(qubit, &gate_matrix);
    }
    
    pub fn apply_two_qubit_gate(&mut self, control: usize, target: usize, gate: TwoQubitGate) {
        match gate {
            TwoQubitGate::CNOT => self.apply_cnot(control, target),
        }
    }
    
    pub fn expand_to_qubits(&self, new_num_qubits: usize) -> Self {
        if new_num_qubits <= self.num_qubits {
            return self.clone();
        }
        
        let old_size = 1 << self.num_qubits;
        let new_size = 1 << new_num_qubits;
        let mut new_amplitudes = vec![Complex::new(0.0, 0.0); new_size];
        
        for i in 0..old_size {
            new_amplitudes[i] = self.amplitudes[i];
        }
        
        Self {
            amplitudes: new_amplitudes,
            num_qubits: new_num_qubits,
        }
    }
    
    fn apply_single_qubit_matrix(&mut self, qubit: usize, matrix: &[Complex<f64>; 4]) {
        let stride = 1 << qubit;
        let block_size = 1 << (qubit + 1);
        
        for block_start in (0..self.amplitudes.len()).step_by(block_size) {
            for i in 0..stride {
                let idx_0 = block_start + i;
                let idx_1 = block_start + i + stride;
                
                let old_0 = self.amplitudes[idx_0];
                let old_1 = self.amplitudes[idx_1];
                
                self.amplitudes[idx_0] = matrix[0] * old_0 + matrix[1] * old_1;
                self.amplitudes[idx_1] = matrix[2] * old_0 + matrix[3] * old_1;
            }
        }
    }
    
    fn apply_cnot(&mut self, control: usize, target: usize) {
        let control_bit = 1 << control;
        let target_bit = 1 << target;
        
        for i in 0..self.amplitudes.len() {
            if (i & control_bit) != 0 {
                let j = i ^ target_bit;
                self.amplitudes.swap(i, j);
            }
        }
    }
    
    fn hadamard_matrix(&self) -> [Complex<f64>; 4] {
        let sqrt2_inv = 1.0 / (2.0_f64).sqrt();
        [
            Complex::new(sqrt2_inv, 0.0),
            Complex::new(sqrt2_inv, 0.0),
            Complex::new(sqrt2_inv, 0.0),
            Complex::new(-sqrt2_inv, 0.0),
        ]
    }
    
    fn pauli_x_matrix(&self) -> [Complex<f64>; 4] {
        [
            Complex::new(0.0, 0.0),
            Complex::new(1.0, 0.0),
            Complex::new(1.0, 0.0),
            Complex::new(0.0, 0.0),
        ]
    }
    
    fn pauli_y_matrix(&self) -> [Complex<f64>; 4] {
        [
            Complex::new(0.0, 0.0),
            Complex::new(0.0, -1.0),
            Complex::new(0.0, 1.0),
            Complex::new(0.0, 0.0),
        ]
    }
    
    fn pauli_z_matrix(&self) -> [Complex<f64>; 4] {
        [
            Complex::new(1.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(-1.0, 0.0),
        ]
    }
    
    fn phase_s_matrix(&self) -> [Complex<f64>; 4] {
        [
            Complex::new(1.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 1.0),
        ]
    }
    
    fn phase_t_matrix(&self) -> [Complex<f64>; 4] {
        let pi_quarter = std::f64::consts::PI / 4.0;
        [
            Complex::new(1.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(pi_quarter.cos(), pi_quarter.sin()),
        ]
    }
}

impl fmt::Display for QuantumState {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "Quantum State ({} qubits):", self.num_qubits)?;
        
        for i in 0..self.amplitudes.len() {
            let amplitude = self.amplitudes[i];
            let prob = amplitude.norm_sqr();
            
            if prob > 1e-10 {
                let binary = format!("{:0width$b}", i, width = self.num_qubits);
                writeln!(f, "  |{}⟩: {:.6} + {:.6}i  (|α|² = {:.2})", 
                       binary, amplitude.re, amplitude.im, prob)?;
            }
        }
        
        Ok(())
    }
}

impl Default for QuantumState {
    fn default() -> Self {
        Self::new(1)
    }
}
