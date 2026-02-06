/// Estimates remaining battery hours.
///
/// * `current` – current charge percentage (0‑100).
/// * `consumption` – average percent drained per hour.
/// * `radiation` – optional multiplier to simulate radiation effects.
///
/// Returns `f64::INFINITY` when `consumption` is zero.
pub fn estimate_hours(current: f64, consumption: f64, radiation: f64) -> f64 {
    if consumption == 0.0 {
        return f64::INFINITY;
    }
    (current / consumption) * radiation
}
