#[cfg(test)]
mod tests {
    use battery_life_estimator::compute_estimated_hours;

    #[test]
    fn typical_case() {
        let hours = compute_estimated_hours(3000.0, 500.0, 0.9);
        assert!((hours - 5.4).abs() < 1e-6);
    }

    #[test]
    fn zero_draw() {
        let hours = compute_estimated_hours(3000.0, 0.0, 0.9);
        assert!(hours.is_infinite());
    }

    #[test]
    fn custom_efficiency() {
        let hours = compute_estimated_hours(2000.0, 400.0, 0.8);
        assert!((hours - 4.0).abs() < 1e-6);
    }
}
