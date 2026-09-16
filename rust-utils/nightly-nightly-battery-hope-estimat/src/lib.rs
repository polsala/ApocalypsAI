pub fn estimate_hours(capacity_mah: f64, draw_ma: f64, efficiency: f64) -> f64 {
    if draw_ma <= 0.0 || efficiency <= 0.0 {
        return 0.0;
    }
    (capacity_mah * efficiency) / draw_ma
}
