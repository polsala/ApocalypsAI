#[cfg(test)]
mod tests {
    use nightly_battery_estimator::{compute_estimated_hours, whimsical_message};

    #[test]
    fn test_compute_normal() {
        let hours = compute_estimated_hours(50.0, 10.0);
        assert!((hours - 5.0).abs() < 1e-6);
    }

    #[test]
    fn test_compute_zero_consumption() {
        let hours = compute_estimated_hours(50.0, 0.0);
        assert!(hours.is_infinite());
    }

    #[test]
    fn test_whimsical_messages() {
        assert_eq!(whimsical_message(12.0), "Plenty of juice left—keep wandering the wasteland.");
        assert_eq!(whimsical_message(7.0), "Moderate power—stay cautious.");
        assert_eq!(whimsical_message(3.0), "Low battery—find shelter soon.");
        assert_eq!(whimsical_message(1.0), "Critical! Power will die any moment.");
        assert_eq!(whimsical_message(f64::INFINITY), "Your battery is eternal, like the void.");
    }
}
