use radiation_estimator::compute_max_hours;

#[test]
fn test_normal_case() {
    let hours = compute_max_hours(250.0, 1000.0).unwrap();
    assert!((hours - 4.0).abs() < 1e-6);
}

#[test]
fn test_default_limit() {
    let hours = compute_max_hours(500.0, 1000.0).unwrap();
    assert!((hours - 2.0).abs() < 1e-6);
}

#[test]
fn test_invalid_level() {
    let err = compute_max_hours(0.0, 1000.0).unwrap_err();
    assert_eq!(err, "Radiation level must be positive");
}

#[test]
fn test_invalid_limit() {
    let err = compute_max_hours(100.0, -50.0).unwrap_err();
    assert_eq!(err, "Dose limit must be positive");
}
