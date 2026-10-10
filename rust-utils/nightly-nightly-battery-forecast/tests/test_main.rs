use battery_forecast::estimate_hours;
use battery_forecast::warning_message;

#[test]
fn test_estimate_hours_normal() {
    let hours = estimate_hours(6000.0, 50.0, 1500.0);
    assert!((hours - 2.0).abs() < 1e-6);
}

#[test]
fn test_warning_high() {
    let msg = warning_message(6.0);
    assert_eq!(msg, "You have enough juice to outrun the raiders.");
}

#[test]
fn test_warning_medium() {
    let msg = warning_message(3.0);
    assert_eq!(msg, "Battery low, seek shelter soon.");
}

#[test]
fn test_warning_low() {
    let msg = warning_message(1.5);
    assert_eq!(msg, "Critical! Power will die before sunrise.");
}
