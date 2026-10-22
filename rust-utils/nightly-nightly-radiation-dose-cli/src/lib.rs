pub fn compute_dose(distance_m: f64, time_min: f64, source_sieverts_per_hr_at_1m: f64) -> f64 {
    if distance_m <= 0.0 {
        return 0.0;
    }
    let dose_rate = source_sieverts_per_hr_at_1m / (distance_m * distance_m);
    dose_rate * (time_min / 60.0)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_compute_dose_basic() {
        let dose = compute_dose(2.0, 30.0, 0.5);
        // dose_rate = 0.5 / 4 = 0.125 Sv/h, time = 0.5 h => dose = 0.0625 Sv
        assert!((dose - 0.0625).abs() < 1e-6);
    }
    #[test]
    fn test_zero_distance() {
        let dose = compute_dose(0.0, 10.0, 1.0);
        assert_eq!(dose, 0.0);
    }
}
