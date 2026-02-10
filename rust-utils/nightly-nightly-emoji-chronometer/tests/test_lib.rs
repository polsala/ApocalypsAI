use emoji_chronometer::{hour_to_emoji, round_minute};

#[test]
fn test_cli_logic_hour() {
    // 00:00 UTC should be 🕛 00
    assert_eq!(hour_to_emoji(0), "🕛");
    assert_eq!(round_minute(0), 0);
}

#[test]
fn test_cli_logic_mixed() {
    // 14:23 UTC -> hour 14 => 2 PM => 🕑, minutes 23 -> round to 25
    assert_eq!(hour_to_emoji(14), "🕑");
    assert_eq!(round_minute(23), 25);
}
