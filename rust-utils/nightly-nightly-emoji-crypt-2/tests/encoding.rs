#[cfg(test)]
mod tests {
    use nightly_emoji_crypt::{encode, decode};

    #[test]
    fn test_encode_known() {
        let input = "abc xyz";
        let expected = "😀😁😂⬜😑😶🙄";
        assert_eq!(encode(input), expected);
    }

    #[test]
    fn test_decode_known() {
        let emoji = "😀😁😂⬜😑😶🙄";
        let expected = "abc xyz";
        assert_eq!(decode(emoji), expected);
    }

    #[test]
    fn test_roundtrip() {
        let original = "Rust is fun!";
        let encoded = encode(original);
        let decoded = decode(&encoded);
        // Unsupported characters become '?' after decode
        let expected = "rust is fun?";
        assert_eq!(decoded, expected);
    }
}
