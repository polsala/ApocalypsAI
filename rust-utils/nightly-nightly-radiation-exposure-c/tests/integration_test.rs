use nightly_radiation_exposure_calculator::total_dose;

#[test]
fn test_total_dose_simple() {
    // 60 min at 2.0 mSv/h => 2.0 mSv
    // 30 min at 4.0 mSv/h => 2.0 mSv
    // Expected total: 4.0 mSv
    let events = vec![(60.0, 2.0), (30.0, 4.0)];
    let dose = total_dose(&events);
    assert!((dose - 4.0).abs() < 1e-6);
}

#[test]
fn test_total_dose_empty() {
    let events: Vec<(f64, f64)> = vec![];
    let dose = total_dose(&events);
    assert_eq!(dose, 0.0);
}
