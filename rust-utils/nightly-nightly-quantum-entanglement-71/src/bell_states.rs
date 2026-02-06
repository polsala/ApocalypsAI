use rand::prelude::*;

/// Represents the four Bell states
#[derive(Debug, Clone)]
pub enum BellState {
    PhiPlus,   // |Φ+⟩ = (|00⟩ + |11⟩)/√2
    PhiMinus,  // |Φ-⟩ = (|00⟩ - |11⟩)/√2
    PsiPlus,   // |Ψ+⟩ = (|01⟩ + |10⟩)/√2
    PsiMinus,  // |Ψ-⟩ = (|01⟩ - |10⟩)/√2
}

impl BellState {
    /// Create BellState from string
    pub fn from_string(state: &str) -> Self {
        match state.to_lowercase().as_str() {
            "phi-plus" | "phi+" | "φ+" => BellState::PhiPlus,
            "phi-minus" | "phi-" | "φ-" => BellState::PhiMinus,
            "psi-plus" | "psi+" | "ψ+" => BellState::PsiPlus,
            "psi-minus" | "psi-" | "ψ-" => BellState::PsiMinus,
            _ => BellState::PhiPlus, // Default
        }
    }
    
    /// Get the name of the Bell state
    pub fn name(&self) -> &'static str {
        match self {
            BellState::PhiPlus => "|Φ+⟩ = (|00⟩ + |11⟩)/√2",
            BellState::PhiMinus => "|Φ-⟩ = (|00⟩ - |11⟩)/√2",
            BellState::PsiPlus => "|Ψ+⟩ = (|01⟩ + |10⟩)/√2",
            BellState::PsiMinus => "|Ψ-⟩ = (|01⟩ - |10⟩)/√2",
        }
    }
    
    /// Generate measurement outcomes for the Bell state
    pub fn measure(&self, measurements: usize, precision: usize) -> Vec<(bool, bool)> {
        let mut rng = thread_rng();
        let mut results = Vec::with_capacity(measurements);
        
        for _ in 0..measurements {
            let (bit1, bit2) = match self {
                BellState::PhiPlus => {
                    // 50% |00⟩, 50% |11⟩
                    if rng.gen_bool(0.5) {
                        (false, false) // |00⟩
                    } else {
                        (true, true)   // |11⟩
                    }
                },
                BellState::PhiMinus => {
                    // 50% |00⟩, 50% |11⟩ with phase
                    if rng.gen_bool(0.5) {
                        (false, false) // |00⟩
                    } else {
                        (true, true)   // |11⟩
                    }
                },
                BellState::PsiPlus => {
                    // 50% |01⟩, 50% |10⟩
                    if rng.gen_bool(0.5) {
                        (false, true)  // |01⟩
                    } else {
                        (true, false)  // |10⟩
                    }
                },
                BellState::PsiMinus => {
                    // 50% |01⟩, 50% |10⟩ with phase
                    if rng.gen_bool(0.5) {
                        (false, true)  // |01⟩
                    } else {
                        (true, false)  // |10⟩
                    }
                },
            };
            results.push((bit1, bit2));
        }
        
        results
    }
    
    /// Calculate theoretical correlation for Bell state
    pub fn theoretical_correlation(&self) -> f64 {
        match self {
            BellState::PhiPlus | BellState::PhiMinus => 1.0,  // Perfect correlation
            BellState::PsiPlus | BellState::PsiMinus => -1.0, // Perfect anti-correlation
        }
    }
    
    /// Calculate theoretical CHSH value
    pub fn theoretical_chsh(&self) -> f64 {
        2.0 * f64::sqrt(2.0) // Maximum quantum violation
    }
}

/// Calculate correlation coefficient from measurement results
pub fn calculate_correlation(results: &[(bool, bool)]) -> f64 {
    let n = results.len();
    if n == 0 { return 0.0; }
    
    let mut sum = 0.0;
    for &(a, b) in results {
        let val_a = if a { 1.0 } else { -1.0 };
        let val_b = if b { 1.0 } else { -1.0 };
        sum += val_a * val_b;
    }
    
    sum / n as f64
}

/// Calculate CHSH inequality value
pub fn calculate_chsh(results: &[(bool, bool)]) -> f64 {
    // CHSH test with measurement angles:
    // Alice: 0°, 90°
    // Bob: 45°, 135°
    
    let n = results.len();
    if n == 0 { return 0.0; }
    
    let mut e_ab = 0.0;
    let mut e_ab_prime = 0.0;
    let mut e_a_prime_b = 0.0;
    let mut e_a_prime_b_prime = 0.0;
    
    let mut rng = thread_rng();
    
    for &(a, b) in results {
        // Randomly choose measurement settings
        let alice_setting = rng.gen_range(0..2);
        let bob_setting = rng.gen_range(0..2);
        
        let val_a = if a { 1.0 } else { -1.0 };
        let val_b = if b { 1.0 } else { -1.0 };
        
        match (alice_setting, bob_setting) {
            (0, 0) => e_ab += val_a * val_b,
            (0, 1) => e_ab_prime += val_a * val_b,
            (1, 0) => e_a_prime_b += val_a * val_b,
            (1, 1) => e_a_prime_b_prime += val_a * val_b,
            _ => {},
        }
    }
    
    let n_float = n as f64;
    let s = (e_ab / n_float).abs() + (e_ab_prime / n_float).abs() + 
            (e_a_prime_b / n_float).abs() + (e_a_prime_b_prime / n_float).abs();
    
    s
}

/// Calculate fidelity with ideal Bell state
pub fn calculate_fidelity(results: &[(bool, bool)], bell_state: &BellState) -> f64 {
    let n = results.len();
    if n == 0 { return 0.0; }
    
    let mut matches = 0;
    for &(a, b) in results {
        let expected = match bell_state {
            BellState::PhiPlus => a == b,
            BellState::PhiMinus => a == b,
            BellState::PsiPlus => a != b,
            BellState::PsiMinus => a != b,
        };
        if expected {
            matches += 1;
        }
    }
    
    matches as f64 / n as f64
}
