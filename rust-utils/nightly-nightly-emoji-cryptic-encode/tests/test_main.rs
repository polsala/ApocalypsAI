#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encode_known() {
        // "Hi" -> Base64 "SGk=" -> emojis 🤗😆😴🟰
        let result = encode_to_emoji("Hi");
        assert_eq!(result, "🤗😆😴🟰");
    }

    #[test]
    fn test_decode_known() {
        let emoji = "🤗😆😴🟰";
        let decoded = decode_from_emoji(emoji).expect("Decoding failed");
        assert_eq!(decoded, "Hi");
    }

    #[test]
    fn test_roundtrip_random() {
        let original = "The quick brown fox jumps over the lazy dog 123!";
        let encoded = encode_to_emoji(original);
        let decoded = decode_from_emoji(&encoded).expect("Roundtrip decode failed");
        assert_eq!(decoded, original);
    }
}
