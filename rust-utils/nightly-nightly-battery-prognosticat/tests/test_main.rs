use nightly_battery_prognosticator::estimate_hours;

#[test]
fn test_basic_estimate() {
    // Mock rationale: simple linear estimate without radiation
    let hours = estimate_hours(80.0, 4.0, 1.0);
    assert!((hours - 20.0).abs() < 1e-6);
}

#[test]
fn test_with_radiation() {
    // Mock rationale: radiation factor scales the result
    let hours = estimate_hours(50.0, 5.0, 1.5);
    assert!((hours - 15.0).abs() < 1e-6);
}

#[test]
fn test_zero_consumption() {
    // Mock rationale: zero consumption yields infinite hours
    let hours = estimate_hours(30.0, 0.0, 1.0);
    assert!(hours.is_infinite());
}
