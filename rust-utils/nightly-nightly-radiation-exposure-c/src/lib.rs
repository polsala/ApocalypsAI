pub fn max_exposure_hours(radiation_uSv_per_h: f64, dose_limit_mSv: f64) -> f64 {
    if radiation_uSv_per_h <= 0.0 {
        return f64::INFINITY;
    }
    dose_limit_mSv * 1000.0 / radiation_uSv_per_h
}
