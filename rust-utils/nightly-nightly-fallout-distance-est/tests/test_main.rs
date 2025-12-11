#[cfg(test)]
mod tests {
    use approx::assert_relative_eq;
    use super::super::*;

    #[test]
    fn test_radiation_at_distance() {
        // Example values: initial 4 Sv/h at 1 km, half‑life 8 h, time 8 h, distance 2 km
        let rad = radiation_at_distance(4.0, 8.0, 8.0, 2.0);
        // Decay factor = 0.5^(8/8) = 0.5, so expected = 4 * 0.5 / (2^2) = 1.0 / 4 = 0.25 Sv/h
        assert_relative_eq!(rad, 0.25, epsilon = 1e-12);
    }

    #[test]
    fn test_safe_distance_basic() {
        // With same parameters as above and threshold 0.1 Sv/h
        let dist = safe_distance(4.0, 8.0, 8.0, 0.1);
        // Expected distance = sqrt( (4 * 0.5) / 0.1 ) = sqrt(2 / 0.1) = sqrt(20) ≈ 4.4721 km
        assert_relative_eq!(dist, 4.47213595499958, epsilon = 1e-12);
    }

    #[test]
    fn test_safe_distance_matches_radiation() {
        let initial = 5.0;
        let half_life = 12.0;
        let time = 24.0;
        let threshold = 0.001;
        let dist = safe_distance(initial, half_life, time, threshold);
        let rad = radiation_at_distance(initial, half_life, time, dist);
        // The radiation at the computed distance should be <= threshold (allow tiny epsilon)
        assert!(rad <= threshold + 1e-9);
    }
}
