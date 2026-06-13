use battery_life::estimate_hours;

#[test]
fn integration_estimate() {
    let hrs = estimate_hours(3000.0, 150.0);
    assert!((hrs - 20.0).abs() < 1e-6);
}
