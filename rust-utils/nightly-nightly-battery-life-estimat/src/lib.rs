pub fn estimate_hours(current: f64, consumption: f64) -> f64 {
    if consumption == 0.0 {
        f64::INFINITY
    } else {
        current / consumption
    }
}
