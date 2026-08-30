/// Computes the total radiation dose (in mSv) from a slice of exposure events.
///
/// Each event is a tuple `(duration_minutes, intensity_mSv_per_h)`.
/// The dose contributed by an event is `duration_hours * intensity`.
pub fn total_dose(events: &[(f64, f64)]) -> f64 {
    events
        .iter()
        .map(|(duration_min, intensity)| duration_min / 60.0 * intensity)
        .sum()
}
