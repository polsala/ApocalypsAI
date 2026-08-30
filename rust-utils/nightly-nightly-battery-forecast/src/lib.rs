pub fn estimate_hours(current: f64, consumption_per_hour: f64) -> f64 {\n    if consumption_per_hour <= 0.0 {\n        f64::INFINITY\n    } else {\n        current / consumption_per_hour\n    }\n}\n
