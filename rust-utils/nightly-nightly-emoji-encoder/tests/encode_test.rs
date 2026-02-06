use nightly_emoji_encoder::encode;

#[test]
fn test_cli_encode() {
    let input = "Rust!";
    let expected = "🇷🇺🇸🇹!";
    assert_eq!(encode(input), expected);
}
