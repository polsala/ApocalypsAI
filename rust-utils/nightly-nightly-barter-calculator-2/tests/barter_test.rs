#[cfg(test)]
mod tests {
    use nightly_barter_calculator::calculate_exchange;

    #[test]
    fn test_basic_ratio() {
        let rate = calculate_exchange(3.0, 5.0);
        // Expected 5 / 3 ≈ 1.6666667
        assert!((rate - 1.6666667).abs() < 1e-6);
    }

    #[test]
    fn test_equal_values() {
        let rate = calculate_exchange(10.0, 10.0);
        assert!((rate - 1.0).abs() < 1e-9);
    }

    #[test]
    fn test_fractional_values() {
        let rate = calculate_exchange(2.5, 7.5);
        assert!((rate - 3.0).abs() < 1e-9);
    }
}
