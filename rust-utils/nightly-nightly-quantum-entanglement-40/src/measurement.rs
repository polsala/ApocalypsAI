use rand::Rng;

use crate::bell_state::{BellState, QuantumState};

/// Quantum measurement basis
#[derive(Debug, Clone, Copy)]
pub enum MeasurementBasis {
    /// Computational basis: |0⟩ and |1⟩
    Computational,
    /// Hadamard basis: |+⟩ and |-⟩ where |+⟩ = (|0⟩ + |1⟩)/√2
    Hadamard,
}

impl std::fmt::Display for MeasurementBasis {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            MeasurementBasis::Computational => write!(f, "Computational"),
            MeasurementBasis::Hadamard => write!(f, "Hadamard"),
        }
    }
}

/// Quantum measurement simulator
pub struct QuantumMeasurement {
    qubits: usize,
    basis: MeasurementBasis,
}

impl QuantumMeasurement {
    /// Create a new quantum measurement simulator
    pub fn new(qubits: usize, basis: MeasurementBasis) -> Self {
        QuantumMeasurement { qubits, basis }
    }

    /// Perform a measurement on the quantum system
    pub fn measure<R: Rng>(&self, rng: &mut R) -> BellState {
        // For simplicity, we'll simulate measurements on a 2-qubit system
        // In a real implementation, this would depend on the actual quantum state

        match self.basis {
            MeasurementBasis::Computational => {
                // In computational basis, we measure |00⟩, |01⟩, |10⟩, |11⟩
                // and map them to Bell states
                let random = rng.gen_range(0..4);
                match random {
                    0 => BellState::PhiPlus,   // |00⟩ -> |Φ⁺⟩
                    1 => BellState::PsiPlus,   // |01⟩ -> |Ψ⁺⟩
                    2 => BellState::PsiMinus,  // |10⟩ -> |Ψ⁻⟩
                    3 => BellState::PhiMinus,  // |11⟩ -> |Φ⁻⟩
                    _ => unreachable!(),
                }
            }

            MeasurementBasis::Hadamard => {
                // In Hadamard basis, we measure |++⟩, |+-⟩, |-+⟩, |--⟩
                // This requires applying Hadamard gates before measurement
                let random = rng.gen_range(0..4);
                match random {
                    0 => BellState::PhiPlus,   // |++⟩ -> |Φ⁺⟩
                    1 => BellState::PhiMinus,  // |+-⟩ -> |Φ⁻⟩
                    2 => BellState::PsiPlus,   // |-+⟩ -> |Ψ⁺⟩
                    3 => BellState::PsiMinus,  // |--⟩ -> |Ψ⁻⟩
                    _ => unreachable!(),
                }
            }
        }
    }

    /// Simulate a measurement with noise (decoherence)
    pub fn measure_with_noise<R: Rng>(&self, rng: &mut R, noise_level: f64) -> BellState {
        // Add quantum noise to the measurement
        let noise = rng.gen_range(0.0..1.0);

        if noise < noise_level {
            // Noise causes random measurement result
            let random = rng.gen_range(0..4);
            match random {
                0 => BellState::PhiPlus,
                1 => BellState::PhiMinus,
                2 => BellState::PsiPlus,
                3 => BellState::PsiMinus,
                _ => unreachable!(),
            }
        } else {
            // Normal measurement
            self.measure(rng)
        }
    }

    /// Perform multiple measurements and return statistics
    pub fn measure_multiple<R: Rng>(
        &self,
        rng: &mut R,
        count: usize,
    ) -> (usize, usize, usize, usize) {
        let mut phi_plus = 0;
        let mut phi_minus = 0;
        let mut psi_plus = 0;
        let mut psi_minus = 0;

        for _ in 0..count {
            match self.measure(rng) {
                BellState::PhiPlus => phi_plus += 1,
                BellState::PhiMinus => phi_minus += 1,
                BellState::PsiPlus => psi_plus += 1,
                BellState::PsiMinus => psi_minus += 1,
            }
        }

        (phi_plus, phi_minus, psi_plus, psi_minus)
    }

    /// Calculate measurement fidelity compared to ideal Bell state
    pub fn calculate_fidelity(
        &self,
        measured_counts: (usize, usize, usize, usize),
        total_measurements: usize,
    ) -> f64 {
        let (phi_plus, phi_minus, psi_plus, psi_minus) = measured_counts;

        // Ideal Bell state should have equal probability for all states
        let ideal_prob = 0.25;
        let measured_probs = [
            phi_plus as f64 / total_measurements as f64,
            phi_minus as f64 / total_measurements as f64,
            psi_plus as f64 / total_measurements as f64,
            psi_minus as f64 / total_measurements as f64,
        ];

        // Calculate fidelity as overlap with ideal state
        let mut fidelity = 0.0;
        for prob in measured_probs {
            fidelity += (prob * ideal_prob).sqrt();
        }

        fidelity
    }

    /// Get the measurement basis description
    pub fn basis_description(&self) -> String {
        match self.basis {
            MeasurementBasis::Computational => {
                "Computational basis: Measures in |0⟩ and |1⟩ states".to_string()
            }
            MeasurementBasis::Hadamard => {
                "Hadamard basis: Measures in |+⟩ and |-⟩ states where |+⟩ = (|0⟩ + |1⟩)/√2".to_string()
            }
        }
    }

    /// Simulate quantum decoherence effect on measurements
    pub fn simulate_decoherence<R: Rng>(
        &self,
        rng: &mut R,
        decoherence_rate: f64,
        measurements: usize,
    ) -> Vec<BellState> {
        let mut results = Vec::new();

        for _ in 0..measurements {
            let decoherence = rng.gen_range(0.0..1.0);

            if decoherence < decoherence_rate {
                // Decoherence causes the system to collapse to a classical state
                let classical_state = rng.gen_range(0..4);
                match classical_state {
                    0 => results.push(BellState::PhiPlus),
                    1 => results.push(BellState::PhiMinus),
                    2 => results.push(BellState::PsiPlus),
                    3 => results.push(BellState::PsiMinus),
                    _ => unreachable!(),
                }
            } else {
                // Normal quantum measurement
                results.push(self.measure(rng));
            }
        }

        results
    }
}
