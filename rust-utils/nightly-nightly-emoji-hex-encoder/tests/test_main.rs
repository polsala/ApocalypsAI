#[cfg(test)]
mod tests {
    use nightly_emoji_hex_encoder::{encode, decode};

    #[test]
    fn test_encode_known() {
        // 'A' is 0x41 => high nibble 4, low nibble 1 => 😃😁
        let result = encode("A");
        assert_eq!(result, "😃😁");
    }

    #[test]
    fn test_decode_known() {
        let result = decode("😃😁").unwrap();
        assert_eq!(result, "A");
    }

    #[test]
    fn test_roundtrip() {
        let original = "Hello, Rust!";
        let encoded = encode(original);
        let decoded = decode(&encoded).unwrap();
        assert_eq!(decoded, original);
    }
}
