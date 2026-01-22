use nightly_emoji_weather::weather_code_to_emoji;

#[test]
fn test_known_codes() {
    assert_eq!(weather_code_to_emoji("clear"), Some("☀️"));
    assert_eq!(weather_code_to_emoji("rain"), Some("🌧️"));
}

#[test]
fn test_unknown_code() {
    assert_eq!(weather_code_to_emoji("unknown"), None);
}
