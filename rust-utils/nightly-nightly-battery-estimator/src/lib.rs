pub fn compute_estimated_hours(current_percent: f64, consumption_per_hour: f64) -> f64 {
    if consumption_per_hour <= 0.0 {
        return f64::INFINITY;
    }
    current_percent / consumption_per_hour
}

pub fn whimsical_message(hours: f64) -> &'static str {
    if hours.is_infinite() {
        "Your battery is eternal, like the void."
    } else if hours > 10.0 {
        "Plenty of juice left—keep wandering the wasteland."
    } else if hours > 5.0 {
        "Moderate power—stay cautious."
    } else if hours > 2.0 {
        "Low battery—find shelter soon."
    } else {
        "Critical! Power will die any moment."
    }
}
