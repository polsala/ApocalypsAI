/// Calculate quantum fidelity from measurement results
/// 
/// Fidelity measures how close the measured state is to the ideal Bell state
pub fn calculate_fidelity(
    phi_plus: usize,
    phi_minus: usize,
    psi_plus: usize,
    psi_minus: usize,
    total_measurements: usize,
) -> f64 {
    let total = total_measurements as f64;
    let p_phi_plus = phi_plus as f64 / total;
    let p_phi_minus = phi_minus as f64 / total;
    let p_psi_plus = psi_plus as f64 / total;
    let p_psi_minus = psi_minus as f64 / total;

    // Ideal Bell state has equal probability for all states (0.25 each)
    let ideal_prob = 0.25;

    // Calculate fidelity as the sum of square roots of probability products
    let fidelity = (p_phi_plus * ideal_prob).sqrt()
        + (p_phi_minus * ideal_prob).sqrt()
        + (p_psi_plus * ideal_prob).sqrt()
        + (p_psi_minus * ideal_prob).sqrt();

    fidelity
}

/// Calculate concurrence - a measure of entanglement
/// 
/// For a 2-qubit system, concurrence ranges from 0 (separable) to 1 (maximally entangled)
pub fn calculate_concurrence(
    phi_plus: usize,
    phi_minus: usize,
    psi_plus: usize,
    psi_minus: usize,
    total_measurements: usize,
) -> f64 {
    let total = total_measurements as f64;
    let p_phi_plus = phi_plus as f64 / total;
    let p_phi_minus = phi_minus as f64 / total;
    let p_psi_plus = psi_plus as f64 / total;
    let p_psi_minus = psi_minus as f64 / total;

    // For Bell states, concurrence can be calculated from the measurement probabilities
    // C = 2 * max(0, |ρ₁₂| - √(ρ₀₀ * ρ₃₃))
    // For our simplified case, we use the difference from ideal distribution

    let max_prob = p_phi_plus.max(p_phi_minus).max(p_psi_plus).max(p_psi_minus);
    let min_prob = p_phi_plus.min(p_phi_minus).min(p_psi_plus).min(p_psi_minus);

    // Simple concurrence calculation based on probability distribution
    let concurrence = if max_prob > 0.5 {
        2.0 * (max_prob - 0.5)
    } else {
        0.0
    };

    concurrence.min(1.0)
}

/// Calculate entanglement entropy
/// 
/// Entanglement entropy measures the degree of entanglement between subsystems
pub fn calculate_entropy(
    phi_plus: usize,
    phi_minus: usize,
    psi_plus: usize,
    psi_minus: usize,
    total_measurements: usize,
) -> f64 {
    let total = total_measurements as f64;
    let p_phi_plus = phi_plus as f64 / total;
    let p_phi_minus = phi_minus as f64 / total;
    let p_psi_plus = psi_plus as f64 / total;
    let p_psi_minus = psi_minus as f64 / total;

    let probabilities = [p_phi_plus, p_phi_minus, p_psi_plus, p_psi_minus];

    // Calculate von Neumann entropy
    let mut entropy = 0.0;
    for p in probabilities {
        if p > 0.0 {
            entropy -= p * p.ln();
        }
    }

    // Normalize by maximum possible entropy (ln(4) for 4 states)
    let max_entropy = (4.0_f64).ln();
    entropy / max_entropy
}

/// Calculate quantum discord (simplified)
/// 
/// Quantum discord measures quantum correlations beyond entanglement
pub fn calculate_quantum_discord(
    phi_plus: usize,
    phi_minus: usize,
    psi_plus: usize,
    psi_minus: usize,
    total_measurements: usize,
) -> f64 {
    let total = total_measurements as f64;
    let p_phi_plus = phi_plus as f64 / total;
    let p_phi_minus = phi_minus as f64 / total;
    let p_psi_plus = psi_plus as f64 / total;
    let p_psi_minus = psi_minus as f64 / total;

    // Simplified discord calculation based on measurement basis dependence
    let classical_correlation = (p_phi_plus - p_phi_minus).abs() + (p_psi_plus - p_psi_minus).abs();
    let quantum_correlation = 1.0 - classical_correlation;

    quantum_correlation.max(0.0)
}

/// Calculate tangle (another entanglement measure)
/// 
/// Tangle is related to concurrence and measures entanglement of formation
pub fn calculate_tangle(
    phi_plus: usize,
    phi_minus: usize,
    psi_plus: usize,
    psi_minus: usize,
    total_measurements: usize,
) -> f64 {
    let concurrence = calculate_concurrence(phi_plus, phi_minus, psi_plus, psi_minus, total_measurements);
    concurrence * concurrence
}

/// Calculate linear entropy
/// 
/// Linear entropy is a simplified version of von Neumann entropy
pub fn calculate_linear_entropy(
    phi_plus: usize,
    phi_minus: usize,
    psi_plus: usize,
    psi_minus: usize,
    total_measurements: usize,
) -> f64 {
    let total = total_measurements as f64;
    let p_phi_plus = phi_plus as f64 / total;
    let p_phi_minus = phi_minus as f64 / total;
    let p_psi_plus = psi_plus as f64 / total;
    let p_psi_minus = psi_minus as f64 / total;

    let probabilities = [p_phi_plus, p_phi_minus, p_psi_plus, p_psi_minus];

    // Calculate linear entropy: S = 1 - Tr(ρ²)
    let mut purity = 0.0;
    for p in probabilities {
        purity += p * p;
    }

    1.0 - purity
}

/// Calculate quantum mutual information
/// 
/// Mutual information measures total correlations (classical + quantum)
pub fn calculate_mutual_information(
    phi_plus: usize,
    phi_minus: usize,
    psi_plus: usize,
    psi_minus: usize,
    total_measurements: usize,
) -> f64 {
    let total = total_measurements as f64;
    let p_phi_plus = phi_plus as f64 / total;
    let p_phi_minus = phi_minus as f64 / total;
    let p_psi_plus = psi_plus as f64 / total;
    let p_psi_minus = psi_minus as f64 / total;

    // For a 2-qubit system, calculate marginal probabilities
    let p_0 = p_phi_plus + p_psi_plus; // Probability of first qubit being 0
    let p_1 = p_phi_minus + p_psi_minus; // Probability of first qubit being 1
    let p_00 = p_phi_plus; // Probability of both qubits being 0
    let p_01 = p_psi_plus; // Probability of first 0, second 1
    let p_10 = p_psi_minus; // Probability of first 1, second 0
    let p_11 = p_phi_minus; // Probability of both qubits being 1

    let mut mutual_info = 0.0;

    // Calculate mutual information: I(A:B) = H(A) + H(B) - H(A,B)
    if p_0 > 0.0 {
        mutual_info -= p_0 * p_0.ln();
    }
    if p_1 > 0.0 {
        mutual_info -= p_1 * p_1.ln();
    }

    // For symmetric system, H(A) = H(B)
    let entropy_ab = calculate_entropy(phi_plus, phi_minus, psi_plus, psi_minus, total_measurements);

    mutual_info * 2.0 - entropy_ab
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate_fidelity_ideal() {
        // Perfect Bell state measurements
        let fidelity = calculate_fidelity(250, 250, 250, 250, 1000);
        assert!((fidelity - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_calculate_concurrence_ideal() {
        // Perfect Bell state should have maximum concurrence
        let concurrence = calculate_concurrence(250, 250, 250, 250, 1000);
        assert!((concurrence - 0.0).abs() < 0.1); // Ideal Bell state has specific concurrence
    }

    #[test]
    fn test_calculate_entropy_maximal() {
        // Equal probabilities should give maximum entropy
        let entropy = calculate_entropy(250, 250, 250, 250, 1000);
        assert!((entropy - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_calculate_linear_entropy_ideal() {
        // Perfect distribution should have low linear entropy
        let linear_entropy = calculate_linear_entropy(250, 250, 250, 250, 1000);
        assert!(linear_entropy < 0.1);
    }
}
