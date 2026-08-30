pub fn compute_max_hours(level: f64, limit: f64) -> Result<f64, &'static str> {
    if level <= 0.0 {
        return Err("Radiation level must be positive");
    }
    if limit <= 0.0 {
        return Err("Dose limit must be positive");
    }
    Ok(limit / level)
}
