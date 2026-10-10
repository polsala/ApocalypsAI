#[cfg(test)]
mod tests {
    use battery_life_estimator::estimate_hours;

    #[test]
    fn test_normal() {
        let hours = estimate_hours(5000.0, 250.0);
        assert!((hours - 20.0).abs() < 1e-6);
    }

    #[test]
    fn test_zero_consumption() {
        let hours = estimate_hours(5000.0, 0.0);
        assert!(hours.is_infinite());
    }
}
