pub fn estimate_hours(charge: f64, rate: f64) -> Option<f64> {
    if rate <= 0.0 {
        None
    } else {
        Some(charge / rate)
    }
}

pub fn apply_survival(rate: f64) -> f64 {
    // Survival mode simulates a 25% increase in power drain due to harsh conditions.
    rate * 1.25
}
