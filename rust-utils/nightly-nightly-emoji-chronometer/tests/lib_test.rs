use emoji_chronometer::parse_and_format;

#[test]
fn integration_hour_only() {
    // 09:10 UTC -> 9:10 AM => 🕘
    let result = parse_and_format(Some("2023-01-01T09:10:00Z")).unwrap();
    assert_eq!(result, "🕘");
}

#[test]
fn integration_half_hour() {
    // 21:55 UTC -> 9:55 PM => 🕘🕜
    let result = parse_and_format(Some("2023-01-01T21:55:00Z")).unwrap();
    assert_eq!(result, "🕘🕜");
}
