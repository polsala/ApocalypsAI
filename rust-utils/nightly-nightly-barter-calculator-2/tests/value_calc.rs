#[cfg(test)]
mod tests {
    // Mock rationale: test compute_value and ratio calculation deterministically.
    use nightly_barter_calculator::compute_value;

    #[test]
    fn test_compute_value() {
        assert_eq!(compute_value(5, 4), 20);
        assert_eq!(compute_value(1, 10), 10);
    }

    #[test]
    fn test_ratio_precision() {
        let v1 = compute_value(7, 5); // 35
        let v2 = compute_value(3, 8); // 24
        let ratio = (v1 as f64) / (v2 as f64);
        // Expected ratio ≈ 1.458333..., we assert within a tiny epsilon.
        assert!((ratio - 1.4583333333).abs() < 1e-9);
    }
}
