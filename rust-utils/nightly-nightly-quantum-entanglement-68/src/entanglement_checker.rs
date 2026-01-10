use crate::quantum_simulator::QuantumSimulator;

/// Result of an entanglement check
#[derive(Debug, Clone)]
pub struct EntanglementResult {
    pub is_entangled: bool,
    pub entanglement_score: f64,
    pub bell_state_fidelity: f64,
    pub decoherence_level: f64,
}

/// Checks quantum entanglement between states
pub struct EntanglementChecker {
    simulator: QuantumSimulator,
}

impl EntanglementChecker {
    pub fn new() -> Self {
        Self {
            simulator: QuantumSimulator::new(),
        }
    }

    /// Check if two quantum states are entangled
    pub fn check_entanglement(&mut self, state_a: &[f64], state_b: &[f64]) -> EntanglementResult {
        if state_a.len() != state_b.len() {
            return EntanglementResult {
                is_entangled: false,
                entanglement_score: 0.0,
                bell_state_fidelity: 0.0,
                decoherence_level: 1.0,
            };
        }

        // Calculate entanglement metrics
        let fidelity = self.simulator.calculate_fidelity(state_a, state_b);
        let bell_fidelity = self.simulator.calculate_bell_fidelity(state_a, state_b);
        
        // Calculate decoherence level
        let decoherence = self.calculate_decoherence(state_a, state_b);
        
        // Determine entanglement score
        let entanglement_score = self.calculate_entanglement_score(state_a, state_b, fidelity, bell_fidelity);
        
        // Determine if states are entangled
        let is_entangled = entanglement_score > 0.5 && bell_fidelity > 0.3 && decoherence < 0.7;

        EntanglementResult {
            is_entangled,
            entanglement_score,
            bell_state_fidelity: bell_fidelity,
            decoherence_level: decoherence,
        }
    }

    /// Calculate decoherence level between two states
    fn calculate_decoherence(&self, state_a: &[f64], state_b: &[f64]) -> f64 {
        let variance_a: f64 = state_a.iter().map(|x| x.powi(2)).sum();
        let variance_b: f64 = state_b.iter().map(|x| x.powi(2)).sum();
        
        let avg_variance = (variance_a + variance_b) / 2.0;
        
        // Normalize to 0-1 range
        avg_variance.min(1.0)
    }

    /// Calculate entanglement score
    fn calculate_entanglement_score(&self, state_a: &[f64], state_b: &[f64], fidelity: f64, bell_fidelity: f64) -> f64 {
        // Calculate state correlation
        let correlation: f64 = state_a.iter()
            .zip(state_b.iter())
            .map(|(a, b)| (a * b).abs())
            .sum() / state_a.len() as f64;
        
        // Weighted combination of metrics
        let score = (fidelity * 0.4) + (bell_fidelity * 0.4) + (correlation * 0.2);
        
        score.min(1.0).max(0.0)
    }
}
