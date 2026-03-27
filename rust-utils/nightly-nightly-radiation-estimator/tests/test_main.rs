#[cfg(test)]
mod tests {
    use nightly_radiation_estimator::compute_dose;

    #[test]
    fn test_basic() {
        let dose = compute_dose(2.0, 5);
        assert!((dose - 10.0).abs() < 1e-6);
    }

    #[test]
    fn test_zero_hours() {
        let dose = compute_dose(0.0, 10);
        assert_eq!(dose, 0.0);
    }

    #[test]
    fn test_fractional() {
        let dose = compute_dose(1.5, 3);
        assert!((dose - 4.5).abs() < 1e-6);
    }

    #[test]
    fn test_negative_hours() {
        let dose = compute_dose(-5.0, 4);
        assert_eq!(dose, 0.0);
    }
}
