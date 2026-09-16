#[cfg(test)]
mod tests {
    use battery_hope_estimator::estimate_hours;

    #[test]
    fn test_basic_estimate() {
        let hours = estimate_hours(4000.0, 500.0, 0.9);
        // (4000 * 0.9) / 500 = 7.2
        assert!((hours - 7.2).abs() < 1e-6);
    }

    #[test]
    fn test_zero_draw() {
        let hours = estimate_hours(4000.0, 0.0, 0.9);
        assert_eq!(hours, 0.0);
    }

    #[test]
    fn test_low_efficiency() {
        let hours = estimate_hours(4000.0, 500.0, 0.5);
        // (4000 * 0.5) / 500 = 4.0
        assert!((hours - 4.0).abs() < 1e-6);
    }
}
