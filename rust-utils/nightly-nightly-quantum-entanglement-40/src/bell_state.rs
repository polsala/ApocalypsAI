use rand::Rng;

/// Represents the four canonical Bell states
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum BellState {
    /// |Φ⁺⟩ = (|00⟩ + |11⟩)/√2 - Both qubits correlated in same state
    PhiPlus,
    /// |Φ⁻⟩ = (|00⟩ - |11⟩)/√2 - Both qubits anti-correlated in same state
    PhiMinus,
    /// |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2 - Qubits correlated in opposite states
    PsiPlus,
    /// |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2 - Qubits anti-correlated in opposite states
    PsiMinus,
}

impl BellState {
    /// Get the string representation of the Bell state
    pub fn to_string(&self) -> &'static str {
        match self {
            BellState::PhiPlus => "|Φ⁺⟩ (Phi Plus)",
            BellState::PhiMinus => "|Φ⁻⟩ (Phi Minus)",
            BellState::PsiPlus => "|Ψ⁺⟩ (Psi Plus)",
            BellState::PsiMinus => "|Ψ⁻⟩ (Psi Minus)",
        }
    }

    /// Get the mathematical notation
    pub fn notation(&self) -> &'static str {
        match self {
            BellState::PhiPlus => "|Φ⁺⟩ = (|00⟩ + |11⟩)/√2",
            BellState::PhiMinus => "|Φ⁻⟩ = (|00⟩ - |11⟩)/√2",
            BellState::PsiPlus => "|Ψ⁺⟩ = (|01⟩ + |10⟩)/√2",
            BellState::PsiMinus => "|Ψ⁻⟩ = (|01⟩ - |10⟩)/√2",
        }
    }

    /// Calculate the theoretical probability of measuring this state
    /// In an ideal entangled system, all states should have equal probability
    pub fn theoretical_probability() -> f64 {
        0.25 // 1/4 for each of the 4 Bell states
    }
}

/// Quantum state representation for simulation
#[derive(Debug, Clone, Copy)]
pub struct QuantumState {
    pub amplitude_00: Complex,
    pub amplitude_01: Complex,
    pub amplitude_10: Complex,
    pub amplitude_11: Complex,
}

#[derive(Debug, Clone, Copy)]
pub struct Complex {
    pub real: f64,
    pub imag: f64,
}

impl Complex {
    pub fn new(real: f64, imag: f64) -> Self {
        Complex { real, imag }
    }

    pub fn magnitude_squared(&self) -> f64 {
        self.real * self.real + self.imag * self.imag
    }

    pub fn normalize(&mut self, norm: f64) {
        self.real /= norm;
        self.imag /= norm;
    }
}

impl QuantumState {
    /// Create a Bell state |Φ⁺⟩
    pub fn phi_plus() -> Self {
        let amp = Complex::new(1.0 / 2.0_f64.sqrt(), 0.0);
        QuantumState {
            amplitude_00: amp,
            amplitude_01: Complex::new(0.0, 0.0),
            amplitude_10: Complex::new(0.0, 0.0),
            amplitude_11: amp,
        }
    }

    /// Create a Bell state |Φ⁻⟩
    pub fn phi_minus() -> Self {
        let amp = Complex::new(1.0 / 2.0_f64.sqrt(), 0.0);
        QuantumState {
            amplitude_00: amp,
            amplitude_01: Complex::new(0.0, 0.0),
            amplitude_10: Complex::new(0.0, 0.0),
            amplitude_11: Complex::new(-amp.real, -amp.imag),
        }
    }

    /// Create a Bell state |Ψ⁺⟩
    pub fn psi_plus() -> Self {
        let amp = Complex::new(1.0 / 2.0_f64.sqrt(), 0.0);
        QuantumState {
            amplitude_00: Complex::new(0.0, 0.0),
            amplitude_01: amp,
            amplitude_10: amp,
            amplitude_11: Complex::new(0.0, 0.0),
        }
    }

    /// Create a Bell state |Ψ⁻⟩
    pub fn psi_minus() -> Self {
        let amp = Complex::new(1.0 / 2.0_f64.sqrt(), 0.0);
        QuantumState {
            amplitude_00: Complex::new(0.0, 0.0),
            amplitude_01: amp,
            amplitude_10: Complex::new(-amp.real, -amp.imag),
            amplitude_11: Complex::new(0.0, 0.0),
        }
    }

    /// Create a random entangled state
    pub fn random_entangled<R: Rng>(rng: &mut R) -> Self {
        // Generate random complex amplitudes
        let a = Complex::new(rng.gen_range(-1.0..1.0), rng.gen_range(-1.0..1.0));
        let b = Complex::new(rng.gen_range(-1.0..1.0), rng.gen_range(-1.0..1.0));
        let c = Complex::new(rng.gen_range(-1.0..1.0), rng.gen_range(-1.0..1.0));
        let d = Complex::new(rng.gen_range(-1.0..1.0), rng.gen_range(-1.0..1.0));

        // Normalize the state
        let norm = (a.magnitude_squared() + b.magnitude_squared() + c.magnitude_squared() + d.magnitude_squared()).sqrt();

        QuantumState {
            amplitude_00: Complex::new(a.real / norm, a.imag / norm),
            amplitude_01: Complex::new(b.real / norm, b.imag / norm),
            amplitude_10: Complex::new(c.real / norm, c.imag / norm),
            amplitude_11: Complex::new(d.real / norm, d.imag / norm),
        }
    }

    /// Calculate the probability of measuring each basis state
    pub fn measurement_probabilities(&self) -> (f64, f64, f64, f64) {
        let p_00 = self.amplitude_00.magnitude_squared();
        let p_01 = self.amplitude_01.magnitude_squared();
        let p_10 = self.amplitude_10.magnitude_squared();
        let p_11 = self.amplitude_11.magnitude_squared();

        (p_00, p_01, p_10, p_11)
    }

    /// Measure the quantum state and return the result
    pub fn measure<R: Rng>(&self, rng: &mut R) -> BellState {
        let (p_00, p_01, p_10, p_11) = self.measurement_probabilities();
        let random = rng.gen_range(0.0..1.0);

        if random < p_00 {
            BellState::PhiPlus
        } else if random < p_00 + p_01 {
            BellState::PsiPlus
        } else if random < p_00 + p_01 + p_10 {
            BellState::PsiMinus
        } else {
            BellState::PhiMinus
        }
    }

    /// Apply a Hadamard gate to the first qubit
    pub fn hadamard_first_qubit(&mut self) {
        // Hadamard gate matrix: H = 1/√2 * [[1, 1], [1, -1]]
        let h_factor = 1.0 / 2.0_f64.sqrt();

        let new_00 = Complex::new(
            h_factor * (self.amplitude_00.real + self.amplitude_10.real),
            h_factor * (self.amplitude_00.imag + self.amplitude_10.imag),
        );
        let new_01 = Complex::new(
            h_factor * (self.amplitude_01.real + self.amplitude_11.real),
            h_factor * (self.amplitude_01.imag + self.amplitude_11.imag),
        );
        let new_10 = Complex::new(
            h_factor * (self.amplitude_00.real - self.amplitude_10.real),
            h_factor * (self.amplitude_00.imag - self.amplitude_10.imag),
        );
        let new_11 = Complex::new(
            h_factor * (self.amplitude_01.real - self.amplitude_11.real),
            h_factor * (self.amplitude_01.imag - self.amplitude_11.imag),
        );

        self.amplitude_00 = new_00;
        self.amplitude_01 = new_01;
        self.amplitude_10 = new_10;
        self.amplitude_11 = new_11;
    }

    /// Apply a Hadamard gate to the second qubit
    pub fn hadamard_second_qubit(&mut self) {
        let h_factor = 1.0 / 2.0_f64.sqrt();

        let new_00 = Complex::new(
            h_factor * (self.amplitude_00.real + self.amplitude_01.real),
            h_factor * (self.amplitude_00.imag + self.amplitude_01.imag),
        );
        let new_01 = Complex::new(
            h_factor * (self.amplitude_00.real - self.amplitude_01.real),
            h_factor * (self.amplitude_00.imag - self.amplitude_01.imag),
        );
        let new_10 = Complex::new(
            h_factor * (self.amplitude_10.real + self.amplitude_11.real),
            h_factor * (self.amplitude_10.imag + self.amplitude_11.imag),
        );
        let new_11 = Complex::new(
            h_factor * (self.amplitude_10.real - self.amplitude_11.real),
            h_factor * (self.amplitude_10.imag - self.amplitude_11.imag),
        );

        self.amplitude_00 = new_00;
        self.amplitude_01 = new_01;
        self.amplitude_10 = new_10;
        self.amplitude_11 = new_11;
    }
}
