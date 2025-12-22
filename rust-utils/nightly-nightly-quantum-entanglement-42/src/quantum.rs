use rand::prelude::*;

#[derive(Debug, Clone, Copy)]
pub enum MeasurementBasis {
    Z,  // Computational basis
    X,  // Hadamard basis
}

impl MeasurementBasis {
    pub fn random(rng: &mut ThreadRng) -> Self {
        match rng.gen_range(0..2) {
            0 => MeasurementBasis::Z,
            _ => MeasurementBasis::X,
        }
    }
}

#[derive(Debug, Clone)]
pub struct QuantumState {
    alpha: f64,  // Amplitude of |0>
    beta: f64,   // Amplitude of |1>
}

impl QuantumState {
    pub fn new(alpha: f64, beta: f64) -> Self {
        let norm = (alpha.powi(2) + beta.powi(2)).sqrt();
        QuantumState {
            alpha: alpha / norm,
            beta: beta / norm,
        }
    }
    
    pub fn random(rng: &mut ThreadRng) -> Self {
        // Generate random complex amplitudes
        let theta: f64 = rng.gen_range(0.0..std::f64::consts::PI);
        let phi: f64 = rng.gen_range(0.0..2.0 * std::f64::consts::PI);
        
        let alpha = (theta / 2.0).cos();
        let beta = (theta / 2.0).sin() * (phi * std::f64::consts::I).exp();
        
        QuantumState::new(alpha, beta.re())
    }
    
    pub fn entangled_copy(&self) -> Self {
        // Create entangled copy (simplified for demonstration)
        QuantumState::new(self.beta, self.alpha)
    }
    
    pub fn measure(&self, basis: &MeasurementBasis) -> bool {
        let probability = match basis {
            MeasurementBasis::Z => self.alpha.powi(2),
            MeasurementBasis::X => {
                // Transform to X basis
                let plus_prob = ((self.alpha + self.beta) / 2.0_f64.sqrt()).powi(2);
                plus_prob
            }
        };
        
        let mut rng = thread_rng();
        rng.gen::<f64>() < probability
    }
    
    pub fn fidelity(&self, other: &QuantumState) -> f64 {
        // Calculate fidelity between two quantum states
        let overlap = self.alpha * other.alpha + self.beta * other.beta;
        overlap.abs()
    }
    
    pub fn apply_hadamard(&mut self) {
        // Apply Hadamard gate
        let new_alpha = (self.alpha + self.beta) / 2.0_f64.sqrt();
        let new_beta = (self.alpha - self.beta) / 2.0_f64.sqrt();
        
        self.alpha = new_alpha;
        self.beta = new_beta;
    }
    
    pub fn apply_pauli_x(&mut self) {
        // Apply Pauli-X gate (bit flip)
        let temp = self.alpha;
        self.alpha = self.beta;
        self.beta = temp;
    }
    
    pub fn apply_pauli_z(&mut self) {
        // Apply Pauli-Z gate (phase flip)
        self.beta = -self.beta;
    }
}

impl Default for QuantumState {
    fn default() -> Self {
        QuantumState::new(1.0, 0.0)  // |0> state
    }
}
