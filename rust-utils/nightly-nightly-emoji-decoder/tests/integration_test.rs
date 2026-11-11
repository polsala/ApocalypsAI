use emoji_decoder::decode_emoji;

#[test]
fn test_decode_known() {
    let input = "🚀🔥";
    let out = decode_emoji(input);
    assert_eq!(out, vec![("🚀", "rocket"), ("🔥", "fire")]);
}

#[test]
fn test_decode_unknown() {
    let input = "ABC";
    let out = decode_emoji(input);
    assert!(out.is_empty());
}
