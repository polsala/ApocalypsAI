use crate::bell_states::{BellState, calculate_correlation, calculate_chsh, calculate_fidelity};
use crate::VerificationResults;
use rand::prelude::*;

/// Verify quantum entanglement using Bell state measurements
pub fn verify_entanglement(
    qubits: usize,
    measurements: usize,
    bell_state_str: &str,
    precision: usize,
) -> VerificationResults {
    // For simplicity, we focus on 2-qubit entanglement
    if qubits != 2 {
        eprintln!("⚠️  Warning: Only 2-qubit entanglement verification is currently supported");
    }
    
    let bell_state = BellState::from_string(bell_state_str);
    
    // Generate measurement results
    let results = bell_state.measure(measurements, precision);
    
    // Calculate metrics
    let correlation = calculate_correlation(&results);
    let chsh_value = calculate_chsh(&results);
    let fidelity = calculate_fidelity(&results, &bell_state);
    
    // Determine if entangled
    // Classical correlation limit: |correlation| ≤ 1
    // Quantum correlation: can approach ±1 with high fidelity
    let is_entangled = fidelity > 0.8 && correlation.abs() > 0.5;
    
    // CHSH violation check
    // Classical limit: |S| ≤ 2
    // Quantum limit: |S| ≤ 2√2 ≈ 2.828
    let chsh_violation = chsh_value > 2.0;
    
    VerificationResults {
        correlation,
        chsh_value,
        chsh_violation,
        fidelity,
        is_entangled,
    }
}

/// Simulate quantum decoherence effects
pub fn apply_decoherence(results: &mut Vec<(bool, bool)>, decoherence_rate: f64) {
    let mut rng = thread_rng();
    
    for (a, b) in results.iter_mut() {
        // Apply bit flip with probability based on decoherence rate
        if rng.gen_bool(decoherence_rate) {
            *a = !*a;
        }
        if rng.gen_bool(decoherence_rate) {
            *b = !*b;
        }
    }
}

/// Simulate measurement noise
pub fn add_measurement_noise(results: &mut Vec<(bool, bool)>, noise_level: f64) {
    let mut rng = thread_rng();
    
    for (a, b) in results.iter_mut() {
        // Add random measurement errors
        if rng.gen_bool(noise_level) {
            *a = !*a;
        }
        if rng.gen_bool(noise_level) {
            *b = !*b;
        }
    }
}

/// Generate statistical summary of measurements
pub fn generate_statistics(results: &[(bool, bool)]) -> HashMap<String, f64> {
    let n = results.len() as f64;
    
    let mut stats = HashMap::new();
    
    // Count outcomes
    let mut count_00 = 0;
    let mut count_01 = 0;
    let mut count_10 = 0;
    let mut count_11 = 0;
    
    for &(a, b) in results {
        match (a, b) {
            (false, false) => count_00 += 1,
            (false, true) => count_01 += 1,
            (true, false) => count_10 += 1,
            (true, true) => count_11 += 1,
        }
    }
    
    stats.insert("P(00)".to_string(), count_00 as f64 / n);
    stats.insert("P(01)".to_string(), count_01 as f64 / n);
    stats.insert("P(10)".to_string(), count_10 as f64 / n);
    stats.insert("P(11)".to_string(), count_11 as f64 / n);
    stats.insert("Correlation".to_string(), calculate_correlation(results));
    stats.insert("CHSH Value".to_string(), calculate_chsh(results));
    stats.insert("Entropy".to_string(), calculate_entropy(results));
    
    stats
}

/// Calculate von Neumann entropy of the measurement distribution
fn calculate_entropy(results: &[(bool, bool)]) -> f64 {
    let n = results.len() as f64;
    
    let mut counts = [0.0; 4];
    for &(a, b) in results {
        let idx = (a as usize) * 2 + (b as usize);
        counts[idx] += 1.0;
    }
    
    let mut entropy = 0.0;
    for &count in &counts {
        if count > 0.0 {
            let p = count / n;
            entropy -= p * p.ln();
        }
    }
    
    entropy
}
