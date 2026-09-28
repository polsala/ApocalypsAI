/// Parses a string argument into a `f64`.
/// Returns an error message if parsing fails.
pub fn parse_arg(arg: &str) -> Result<f64, String> {
    arg.parse::<f64>()
        .map_err(|_| format!("Invalid number: {}", arg))
}

/// Estimates battery runtime in hours.
///
/// * `capacity` – battery capacity in mAh.
/// * `draw` – device draw in mA.
///
/// Returns `f64::INFINITY` when `draw` is zero.
pub fn estimate_hours(capacity: f64, draw: f64) -> f64 {
    if draw == 0.0 {
        f64::INFINITY
    } else {
        capacity / draw
    }
}
