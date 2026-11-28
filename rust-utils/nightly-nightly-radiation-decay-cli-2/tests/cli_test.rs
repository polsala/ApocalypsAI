#[cfg(test)]
mod tests {
    use radiation_decay_cli::calculate_decay;

    #[test]
    fn test_basic_decay() {
        // One half‑life should halve the dose
        let remaining = calculate_decay(100.0, 10.0, 10.0);
        assert!((remaining - 50.0).abs() < 1e-6);
    }

    #[test]
    fn test_multiple_half_lives() {
        // Three half‑lives: 80 -> 40 -> 20 -> 10
        let remaining = calculate_decay(80.0, 5.0, 15.0);
        assert!((remaining - 10.0).abs() < 1e-6);
    }

    #[test]
    fn test_zero_half_life() {
        // Guard against division‑by‑zero; should return 0.0
        let remaining = calculate_decay(50.0, 0.0, 5.0);
        assert_eq!(remaining, 0.0);
    }
}
