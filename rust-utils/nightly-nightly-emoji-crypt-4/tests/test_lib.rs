use emoji_crypt::{decode, encode};

#[test]
fn test_encode_decode_roundtrip() {
    let original = "Apocalypse!";
    let encoded = encode(original);
    let decoded = decode(&encoded).expect("Decoding failed");
    assert_eq!(decoded, original);
}
