use radiation_decay::decay;

#[test]
fn test_decay_half_life() {
    let initial = 800.0;
    let half_life = 20.0;
    let time = 40.0;
    let remaining = decay(initial, half_life, time);
    // After two half‑lives, should be quarter of initial
    assert!((remaining - 200.0).abs() < 1e-6);
}

#[test]
fn test_decay_zero_half_life() {
    let remaining = decay(100.0, 0.0, 10.0);
    assert_eq!(remaining, 0.0);
}
