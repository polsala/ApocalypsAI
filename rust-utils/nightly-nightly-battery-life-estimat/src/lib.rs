pub fn estimate_hours(capacity_mah: f64, consumption_ma: f64) -> f64 {
    if consumption_ma == 0.0 {
        return f64::INFINITY;
    }
    capacity_mah / consumption_ma
}
