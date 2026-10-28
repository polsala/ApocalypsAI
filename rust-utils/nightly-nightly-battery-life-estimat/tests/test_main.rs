#[cfg(test)]
mod tests {
    use battery_life_estimator::estimate_hours;

    #[test]
    fn test_basic_estimate() {
        // 2500 mAh capacity, 500 mA draw, 0.9 efficiency → 4.5 h
        let hours = estimate_hours(2500.0, 500.0, 0.9);
        assert!((hours - 4.5).abs() < 1e-6);
    }

    #[test]
    fn test_zero_draw() {
        // Zero draw should yield infinite runtime
        let hours = estimate_hours(2500.0, 0.0, 0.9);
        assert!(hours.is_infinite());
    }
}
