/// Calculates the remaining radiation dose after `elapsed` hours.
///
/// * `initial` – initial dose in millisieverts (mSv).
/// * `half_life` – half‑life of the material in hours. If `half_life` is
///   zero or negative the function returns `0.0` to avoid division by zero.
/// * `elapsed` – time elapsed since the initial measurement, in hours.
///
/// The formula used is:
/// `remaining = initial * 0.5^(elapsed / half_life)`
pub fn calculate_decay(initial: f64, half_life: f64, elapsed: f64) -> f64 {
    if half_life <= 0.0 {
        return 0.0;
    }
    initial * 0.5_f64.powf(elapsed / half_life)
}
