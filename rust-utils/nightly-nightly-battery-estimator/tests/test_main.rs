#[cfg(test)]
mod tests {
    use nightly_battery_estimator::{estimate_hours, apply_survival};

    #[test]
    fn test_estimate_normal() {
        let hours = estimate_hours(80.0, 4.0).unwrap();
        assert!((hours - 20.0).abs() < 1e-6);
    }

    #[test]
    fn test_estimate_zero_rate() {
        assert!(estimate_hours(50.0, 0.0).is_none());
    }

    #[test]
    fn test_survival_mode() {
        let rate = 4.0;
        let surv_rate = apply_survival(rate);
        let hours = estimate_hours(80.0, surv_rate).unwrap();
        // 4 * 1.25 = 5, 80 / 5 = 16
        assert!((hours - 16.0).abs() < 1e-6);
    }
}
