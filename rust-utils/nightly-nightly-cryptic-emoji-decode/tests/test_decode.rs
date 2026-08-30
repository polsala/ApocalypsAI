use cryptic_emoji_decoder::decode;

#[test]
fn test_decode_full() {
    let input = "🌞 🌙 🌟 🔥 💧";
    assert_eq!(decode(input), "ABCDE");
}
