use std::collections::HashMap;
use std::fmt;

#[derive(Debug, Clone)]
pub struct QuantumState {
    pub amplitudes: Vec<Complex>,
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

    pub fn magnitude(&self) -> f64 {
        (self.re * self.re + self.im * self.im).sqrt()
    }

    pub fn magnitude_squared(&self) -> f64 {
        self.re * self.re + self.im * self.im
    }

    pub fn conjugate(&self) -> Self {
        Self::new(self.re, -self.im)
    }

    pub fn normalize(&mut self) {
        let mag = self.magnitude();
        if mag > 0.0 {
            self.re /= mag;
            self.im /= mag;
        }
    }
}

impl std::ops::Add for Complex {
    type Output = Self;

    fn add(self, other: Self) -> Self {
        Self::new(self.re + other.re, self.im + other.im)
    }
}

impl std::ops::Sub for Complex {
    type Output = Self;

    fn sub(self, other: Self) -> Self {
        Self::new(self.re - other.re, self.im - other.im)
    }
}

impl std::ops::Mul for Complex {
    type Output = Self;

    fn mul(self, other: Self) -> Self {
        Self::new(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )
    }
}

impl std::ops::Mul<f64> for Complex {
    type Output = Self;

    fn mul(self, scalar: f64) -> Self {
        Self::new(self.re * scalar, self.im * scalar)
    }
}

impl QuantumState {
    pub fn new(num_qubits: usize) -> Self {
        let size = 1 << num_qubits;
        let mut amplitudes = vec![Complex::new(0.0, 0.0); size];
        amplitudes[0] = Complex::new(1.0, 0.0); // |000...0⟩ state
        Self { amplitudes, num_qubits }
    }

    pub fn normalize(&mut self) {
        let norm_sq: f64 = self.amplitudes.iter().map(|a| a.magnitude_squared()).sum();
        if norm_sq > 0.0 {
            let norm = norm_sq.sqrt();
            for amp in &mut self.amplitudes {
                amp.re /= norm;
                amp.im /= norm;
            }
        }
    }

    pub fn probability(&self, index: usize) -> f64 {
        if index < self.amplitudes.len() {
            self.amplitudes[index].magnitude_squared()
        } else {
            0.0
        }
    }

    pub fn get_measurement_probabilities(&self) -> Vec<f64> {
        self.amplitudes.iter().map(|a| a.magnitude_squared()).collect()
    }

    pub fn is_entangled(&self) -> bool {
        // Simple entanglement detection: check if state can be written as tensor product
        if self.num_qubits < 2 {
            return false;
        }

        // For simplicity, we'll use a heuristic: if there are non-zero amplitudes
        // in states that aren't all-zero or all-one, and the state isn't a simple product
        let non_zero_states: Vec<usize> = self.amplitudes
            .iter()
            .enumerate()
            .filter(|(_, amp)| amp.magnitude_squared() > 1e-10)
            .map(|(i, _)| i)
            .collect();

        if non_zero_states.len() <= 2 {
            return false;
        }

        // Check if it's a product state by examining the pattern
        // This is a simplified check for common entangled states
        let mut has_mixed_pattern = false;
        for &state in &non_zero_states {
            let binary = format!("{:0width$b}", state, width = self.num_qubits);
            if binary.contains('0') && binary.contains('1') {
                has_mixed_pattern = true;
                break;
            }
        }

        has_mixed_pattern
    }

    pub fn get_entangled_qubits(&self) -> Vec<(usize, usize)> {
        let mut entangled_pairs = Vec::new();
        
        if self.num_qubits < 2 {
            return entangled_pairs;
        }

        // Simple heuristic: check if measuring one qubit affects another
        for i in 0..self.num_qubits {
            for j in (i + 1)..self.num_qubits {
                if self.qubits_correlated(i, j) {
                    entangled_pairs.push((i, j));
                }
            }
        }

        entangled_pairs
    }

    fn qubits_correlated(&self, qubit1: usize, qubit2: usize) -> bool {
        // Simplified correlation check
        let mut correlations = HashMap::new();
        
        for (state_idx, amp) in self.amplitudes.iter().enumerate() {
            if amp.magnitude_squared() > 1e-10 {
                let binary = format!("{:0width$b}", state_idx, width = self.num_qubits);
                let bit1 = binary.chars().nth(qubit1).unwrap() as u8 - b'0';
                let bit2 = binary.chars().nth(qubit2).unwrap() as u8 - b'0';
                
                let key = (bit1, bit2);
                *correlations.entry(key).or_insert(0.0) += amp.magnitude_squared();
            }
        }

        // If we have both (0,1) and (1,0) correlations, qubits are likely entangled
        correlations.contains_key(&(0, 1)) && correlations.contains_key(&(1, 0))
    }
}

#[derive(Debug, Clone)]
pub enum Gate {
    Hadamard(usize),
    PauliX(usize),
    PauliY(usize),
    PauliZ(usize),
    CNOT(usize, usize),
    CZ(usize, usize),
    SWAP(usize, usize),
}

impl fmt::Display for Gate {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Gate::Hadamard(q) => write!(f, "H({})", q),
            Gate::PauliX(q) => write!(f, "X({})", q),
            Gate::PauliY(q) => write!(f, "Y({})", q),
            Gate::PauliZ(q) => write!(f, "Z({})", q),
            Gate::CNOT(c, t) => write!(f, "CNOT({}, {})", c, t),
            Gate::CZ(c, t) => write!(f, "CZ({}, {})", c, t),
            Gate::SWAP(q1, q2) => write!(f, "SWAP({}, {})", q1, q2),
        }
    }
}

pub struct QuantumSimulator {
    state: QuantumState,
}

impl QuantumSimulator {
    pub fn new(num_qubits: usize) -> Self {
        Self {
            state: QuantumState::new(num_qubits),
        }
    }

    pub fn get_state(&self) -> QuantumState {
        self.state.clone()
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
        }
        self.state.normalize();
    }

    fn apply_hadamard(&mut self, qubit: usize) {
        let n = self.state.num_qubits;
        let size = 1 << n;
        let mut new_amplitudes = vec![Complex::new(0.0, 0.0); size];

        for i in 0..size {
            let bit = (i >> qubit) & 1;
            let mask = !(1 << qubit);
            let base = i & mask;

            let amp0 = self.state.amplitudes[base];
            let amp1 = self.state.amplitudes[base | (1 << qubit)];

            if bit == 0 {
                new_amplitudes[i] = amp0 + amp1;
            } else {
                new_amplitudes[i] = amp0 - amp1;
            }
        }

        for amp in &mut new_amplitudes {
            *amp = *amp * (1.0 / 2.0_f64.sqrt());
        }

        self.state.amplitudes = new_amplitudes;
    }

    fn apply_pauli_x(&mut self, qubit: usize) {
        let n = self.state.num_qubits;
        let size = 1 << n;
        let mask = 1 << qubit;

        for i in 0..size {
            if (i & mask) == 0 {
                let j = i | mask;
                self.state.amplitudes.swap(i, j);
            }
        }
    }

    fn apply_pauli_y(&mut self, qubit: usize) {
        let n = self.state.num_qubits;
        let size = 1 << n;
        let mask = 1 << qubit;

        for i in 0..size {
            let bit = (i >> qubit) & 1;
            if bit == 1 {
                let j = i ^ mask;
                let amp = self.state.amplitudes[i];
                self.state.amplitudes[i] = Complex::new(-amp.im, amp.re);
                self.state.amplitudes[j] = Complex::new(amp.im, -amp.re);
            }
        }
    }

    fn apply_pauli_z(&mut self, qubit: usize) {
        let n = self.state.num_qubits;
        let size = 1 << n;
        let mask = 1 << qubit;

        for i in 0..size {
            if (i & mask) != 0 {
                self.state.amplitudes[i] = Complex::new(-self.state.amplitudes[i].re, -self.state.amplitudes[i].im);
            }
        }
    }

    fn apply_cnot(&mut self, control: usize, target: usize) {
        let n = self.state.num_qubits;
        let size = 1 << n;
        let control_mask = 1 << control;
        let target_mask = 1 << target;

        for i in 0..size {
            if (i & control_mask) != 0 {
                let j = i ^ target_mask;
                self.state.amplitudes.swap(i, j);
            }
        }
    }

    fn apply_cz(&mut self, control: usize, target: usize) {
        let n = self.state.num_qubits;
        let size = 1 << n;
        let control_mask = 1 << control;
        let target_mask = 1 << target;

        for i in 0..size {
            if (i & control_mask) != 0 && (i & target_mask) != 0 {
                self.state.amplitudes[i] = Complex::new(-self.state.amplitudes[i].re, -self.state.amplitudes[i].im);
            }
        }
    }

    fn apply_swap(&mut self, qubit1: usize, qubit2: usize) {
        if qubit1 == qubit2 {
            return;
        }

        let n = self.state.num_qubits;
        let size = 1 << n;
        let mask1 = 1 << qubit1;
        let mask2 = 1 << qubit2;

        for i in 0..size {
            let bit1 = (i & mask1) != 0;
            let bit2 = (i & mask2) != 0;

            if bit1 != bit2 {
                let j = i ^ (mask1 | mask2);
                if i < j {
                    self.state.amplitudes.swap(i, j);
                }
            }
        }
    }

    pub fn measure(&self, trials: usize) -> HashMap<String, usize> {
        let mut results = HashMap::new();
        let probabilities = self.state.get_measurement_probabilities();
        let mut rng = Xorshift::new();

        for _ in 0..trials {
            let r = rng.next_f64();
            let mut cumulative_prob = 0.0;
            let mut outcome = 0;

            for (i, &prob) in probabilities.iter().enumerate() {
                cumulative_prob += prob;
                if r <= cumulative_prob {
                    outcome = i;
                    break;
                }
            }

            let outcome_str = format!("{:0width$b}", outcome, width = self.state.num_qubits);
            *results.entry(outcome_str).or_insert(0) += 1;
        }

        results
    }
}

// Simple pseudo-random number generator for deterministic results
struct Xorshift {
    state: u64,
}

impl Xorshift {
    fn new() -> Self {
        Self { state: 123456789 } // Fixed seed for deterministic results
    }

    fn next(&mut self) -> u64 {
        let mut x = self.state;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.state = x;
        x
    }

    fn next_f64(&mut self) -> f64 {
        (self.next() % 1000000) as f64 / 1000000.0
    }
}
