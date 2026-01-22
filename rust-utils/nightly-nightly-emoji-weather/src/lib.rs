use std::collections::HashMap;

pub fn weather_code_to_emoji(code: &str) -> Option<&'static str> {
    let mapping: HashMap<&str, &str> = [
        ("clear", "☀️"),
        ("partly_cloudy", "⛅"),
        ("cloudy", "☁️"),
        ("rain", "🌧️"),
        ("thunderstorm", "⛈️"),
        ("snow", "❄️"),
        ("fog", "🌫️"),
    ].iter().cloned().collect();
    mapping.get(code).copied()
}
