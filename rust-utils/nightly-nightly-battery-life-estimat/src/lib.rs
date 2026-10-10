/// Computes the estimated battery life in hours.
///
/// * `capacity` – current battery capacity in mAh.
/// * `draw` – average power draw in mA.
/// * `efficiency` – efficiency factor (0.0‑1.0). Typical default is 0.9.
///
/// Returns `f64::INFINITY` when `draw` is zero.
pub fn compute_estimated_hours(capacity: f64, draw: f64, efficiency: f64) -> f64 {
    if draw == 0.0 {
        return f64::INFINITY;
    }
    capacity * efficiency / draw
}
