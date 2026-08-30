pub fn estimate_hours(capacity_mah: f64, consumption_ma: f64) -> f64 {
    if consumption_ma == 0.0 {
        return f64::INFINITY;
    }
    capacity_mah / consumption_ma
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_estimate() {
        let hrs = estimate_hours(5000.0, 250.0);
        assert!((hrs - 20.0).abs() < 1e-6);
    }
    #[test]
    fn test_zero_consumption() {
        let hrs = estimate_hours(1000.0, 0.0);
        assert!(hrs.is_infinite());
    }
}
