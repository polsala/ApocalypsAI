/// Compute remaining radiation after `time` given an `initial` level and `half_life`.
///
/// Uses the formula: remaining = initial * 0.5^(time / half_life)
pub fn decay(initial: f64, half_life: f64, time: f64) -> f64 {
    if half_life == 0.0 {
        return 0.0; // avoid division by zero; treat as immediate decay
    }
    initial * 0.5_f64.powf(time / half_life)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_decay_basic() {
        let result = decay(1000.0, 30.0, 30.0);
        assert!((result - 500.0).abs() < 1e-6);
    }
}
