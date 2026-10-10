pub fn estimate_hours(capacity_mah: f64, percent: f64, consumption_rate_mah_per_h: f64) -> f64 {
    if consumption_rate_mah_per_h == 0.0 {
        return f64::INFINITY;
    }
    let remaining = capacity_mah * (percent / 100.0);
    remaining / consumption_rate_mah_per_h
}

pub fn warning_message(hours: f64) -> &'static str {
    if hours > 5.0 {
        "You have enough juice to outrun the raiders."
    } else if hours > 2.0 {
        "Battery low, seek shelter soon."
    } else {
        "Critical! Power will die before sunrise."
    }
}
