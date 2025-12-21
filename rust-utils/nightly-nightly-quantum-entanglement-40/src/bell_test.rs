use rand::Rng;

/// Perform a Bell inequality test using the CHSH inequality
/// 
/// The CHSH inequality states that for any local hidden variable theory:
/// |E(a,b) - E(a,b') + E(a',b) + E(a',b')| ≤ 2
/// 
/// Where E represents correlation measurements at different angles
pub fn bell_inequality_test(
    angle_a: f64,
    angle_b: f64,
    angle_a_prime: f64,
    angle_b_prime: f64,
    trials: usize,
) -> String {
    let mut rng = rand::thread_rng();

    // Convert angles from degrees to radians
    let angle_a_rad = angle_a.to_radians();
    let angle_b_rad = angle_b.to_radians();
    let angle_a_prime_rad = angle_a_prime.to_radians();
    let angle_b_prime_rad = angle_b_prime.to_radians();

    // Perform measurements for each angle combination
    let e_ab = measure_correlation(&mut rng, angle_a_rad, angle_b_rad, trials);
    let e_ab_prime = measure_correlation(&mut rng, angle_a_rad, angle_b_prime_rad, trials);
    let e_a_prime_b = measure_correlation(&mut rng, angle_a_prime_rad, angle_b_rad, trials);
    let e_a_prime_b_prime = measure_correlation(&mut rng, angle_a_prime_rad, angle_b_prime_rad, trials);

    // Calculate S-value for CHSH inequality
    let s_value = (e_ab - e_ab_prime + e_a_prime_b + e_a_prime_b_prime).abs();
    let classical_limit = 2.0;
    let violation_percentage = ((s_value - classical_limit) / classical_limit) * 100.0;

    let mut result = String::new();
    result.push_str("=== Bell Inequality Test Results ===\n\n");
    result.push_str(&format!("Measurement Angles:\n"));
    result.push_str(&format!("  Alice (a): {:.1}°\n", angle_a));
    result.push_str(&format!("  Bob (b): {:.1}°\n", angle_b));
    result.push_str(&format!("  Alice (a'): {:.1}°\n", angle_a_prime));
    result.push_str(&format!("  Bob (b'): {:.1}°\n\n", angle_b_prime));

    result.push_str(&format!("Correlation Measurements:\n"));
    result.push_str(&format!("  E(a,b): {:.3}\n", e_ab));
    result.push_str(&format!("  E(a,b'): {:.3}\n", e_ab_prime));
    result.push_str(&format!("  E(a',b): {:.3}\n", e_a_prime_b));
    result.push_str(&format!("  E(a',b'): {:.3}\n\n", e_a_prime_b_prime));

    result.push_str(&format!("CHSH Inequality Test:\n"));
    result.push_str(&format!("  S-value: {:.3}\n", s_value));
    result.push_str(&format!("  Classical Limit: {:.1}\n", classical_limit));
    result.push_str(&format!("  Violation: {:.1}% above classical limit\n\n", violation_percentage));

    if s_value > classical_limit {
        result.push_str(&format!("Result: ✅ QUANTUM ENTANGLEMENT CONFIRMED\n"));
        result.push_str(&format!("The measured correlations violate the Bell inequality,\n"));
        result.push_str(&format!("indicating quantum entanglement is present.\n"));
    } else {
        result.push_str(&format!("Result: ❌ NO QUANTUM ENTANGLEMENT DETECTED\n"));
        result.push_str(&format!("The correlations are consistent with classical physics.\n"));
    }

    result
}

/// Measure correlation between two measurement angles
fn measure_correlation<R: Rng>(rng: &mut R, angle_a: f64, angle_b: f64, trials: usize) -> f64 {
    let mut correlation = 0.0;

    for _ in 0..trials {
        // Generate random hidden variable (lambda)
        let lambda = rng.gen_range(0.0..2.0 * std::f64::consts::PI);

        // Calculate measurement outcomes based on angles
        let outcome_a = measure_outcome(lambda, angle_a);
        let outcome_b = measure_outcome(lambda, angle_b);

        // Correlation is the product of outcomes
        correlation += outcome_a * outcome_b;
    }

    correlation / trials as f64
}

/// Calculate measurement outcome for a given angle and hidden variable
fn measure_outcome(lambda: f64, angle: f64) -> f64 {
    // In quantum mechanics, the probability of getting +1 or -1 depends on
    // the angle difference between the measurement direction and the hidden variable
    let angle_diff = angle - lambda;
    let prob_plus = ((2.0 * angle_diff).cos() + 1.0) / 2.0;

    let random = rand::random::<f64>();

    if random < prob_plus {
        1.0
    } else {
        -1.0
    }
}

/// Calculate the theoretical quantum mechanical prediction for correlation
pub fn theoretical_correlation(angle_diff: f64) -> f64 {
    // For entangled particles, the correlation should be -cos(2 * angle_difference)
    -(2.0 * angle_diff.to_radians()).cos()
}

/// Calculate the maximum possible S-value for given angles
pub fn maximum_s_value(
    angle_a: f64,
    angle_b: f64,
    angle_a_prime: f64,
    angle_b_prime: f64,
) -> f64 {
    let angle_a_rad = angle_a.to_radians();
    let angle_b_rad = angle_b.to_radians();
    let angle_a_prime_rad = angle_a_prime.to_radians();
    let angle_b_prime_rad = angle_b_prime.to_radians();

    let term1 = theoretical_correlation((angle_a_rad - angle_b_rad).to_degrees());
    let term2 = theoretical_correlation((angle_a_rad - angle_b_prime_rad).to_degrees());
    let term3 = theoretical_correlation((angle_a_prime_rad - angle_b_rad).to_degrees());
    let term4 = theoretical_correlation((angle_a_prime_rad - angle_b_prime_rad).to_degrees());

    (term1 - term2 + term3 + term4).abs()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_theoretical_correlation() {
        // For 0 degree difference, correlation should be -1 (perfect anti-correlation)
        assert!((theoretical_correlation(0.0) - (-1.0)).abs() < 1e-10);

        // For 90 degree difference, correlation should be 0 (no correlation)
        assert!((theoretical_correlation(90.0) - 0.0).abs() < 1e-10);

        // For 45 degree difference, correlation should be 0
        assert!((theoretical_correlation(45.0) - 0.0).abs() < 1e-10);
    }

    #[test]
    fn test_maximum_s_value() {
        // Standard CHSH angles: 0°, 45°, 22.5°, 67.5°
        let s_max = maximum_s_value(0.0, 45.0, 22.5, 67.5);
        // Should be close to 2√2 ≈ 2.828
        assert!((s_max - 2.828).abs() < 0.1);
    }
}
