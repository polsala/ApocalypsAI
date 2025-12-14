use std::f64::consts::PI;

pub struct QuantumSimulator {
    seed: u64,
}

impl QuantumSimulator {
    pub fn new(seed: u64) -> Self {
        Self { seed }
    }
    
    pub fn generate_entangled_states(&mut self, nodes: usize, trials: usize) -> Vec<(f64, f64, f64, f64)> {
        let mut states = Vec::with_capacity(trials);
        
        for trial in 0..trials {
            // Generate entangled Bell state |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
            // Using deterministic pseudo-random generation
            let theta_a = self.random_angle(trial * nodes);
            let theta_b = self.random_angle(trial * nodes + 1);
            
            // Calculate correlated measurement outcomes
            // For entangled states, outcomes are perfectly anti-correlated
            let outcome_a = self.measure_spin(theta_a);
            let outcome_b = -outcome_a; // Perfect anti-correlation for |Ψ⁻⟩
            
            // Add small quantum noise
            let noise_a = self.random_noise(trial * nodes + 2);
            let noise_b = self.random_noise(trial * nodes + 3);
            
            states.push((
                outcome_a + noise_a,
                theta_a,
                outcome_b + noise_b,
                theta_b,
            ));
        }
        
        states
    }
    
    fn random_angle(&self, index: usize) -> f64 {
        // Generate deterministic pseudo-random angle [0, 2π]
        let x = self.hash_u64(self.seed.wrapping_add(index as u64)) as f64;
        (x / u64::MAX as f64) * 2.0 * PI
    }
    
    fn random_noise(&self, index: usize) -> f64 {
        // Generate small random noise [-0.1, 0.1]
        let x = self.hash_u64(self.seed.wrapping_add(index as u64)) as f64;
        ((x / u64::MAX as f64) - 0.5) * 0.2
    }
    
    fn measure_spin(&self, theta: f64) -> f64 {
        // Simulate spin measurement along direction theta
        // For entangled states, outcome depends on measurement angle
        let probability = (theta * 2.0).sin().abs();
        let random_val = self.hash_u64(self.seed.wrapping_add(theta as u64)) as f64 / u64::MAX as f64;
        
        if random_val < probability {
            1.0
        } else {
            -1.0
        }
    }
    
    fn hash_u64(&self, x: u64) -> u64 {
        // Simple but effective hash function for deterministic randomness
        let mut z = x.wrapping_mul(0x9e3779b97f4a7c15);
        z = (z ^ (z >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94d049bb133111eb);
        z ^ (z >> 31)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_deterministic_generation() {
        let mut sim1 = QuantumSimulator::new(123);
        let mut sim2 = QuantumSimulator::new(123);
        
        let states1 = sim1.generate_entangled_states(2, 10);
        let states2 = sim2.generate_entangled_states(2, 10);
        
        assert_eq!(states1, states2);
    }
    
    #[test]
    fn test_anti_correlation() {
        let mut sim = QuantumSimulator::new(42);
        let states = sim.generate_entangled_states(2, 100);
        
        // Check that outcomes are approximately anti-correlated
        for (outcome_a, _, outcome_b, _) in states {
            assert!((outcome_a + outcome_b).abs() < 0.3, 
                   "Outcomes should be anti-correlated: {} vs {}", outcome_a, outcome_b);
        }
    }
}
