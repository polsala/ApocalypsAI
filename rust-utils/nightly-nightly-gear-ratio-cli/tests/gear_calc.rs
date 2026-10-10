#[cfg(test)]
mod tests {
    use nightly_gear_ratio_cli::compute_gear_inches;

    #[test]
    fn test_known_values() {
        // chainring 50, cog 12, wheel 700 mm → approx 84.30 gear inches
        let gi = compute_gear_inches(50, 12, 700);
        let expected = 84.30_f64;
        let diff = (gi - expected).abs();
        assert!(diff < 0.01, "gear inches {} not within tolerance", gi);
    }

    #[test]
    fn test_zero_cog() {
        // Guard against division‑by‑zero; should return 0.0
        let gi = compute_gear_inches(50, 0, 700);
        assert_eq!(gi, 0.0);
    }
}
