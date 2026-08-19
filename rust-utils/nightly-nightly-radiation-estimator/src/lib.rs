/// Computes the total radiation dose.
///
/// * `hours` – Time spent in the radiation zone (can be fractional).
/// * `level` – Radiation level per hour (in Sv/h).
///
/// Returns the dose in Sieverts. Negative hours are treated as zero.
pub fn compute_dose(hours: f64, level: u32) -> f64 {
    if hours < 0.0 {
        return 0.0;
    }
    hours * level as f64
}
