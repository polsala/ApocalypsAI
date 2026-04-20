#[cfg(test)]
mod tests {
    use nightly_emoji_binary_encoder::encode_number;

    #[test]
    fn test_zero() {
        assert_eq!(encode_number(0), "⚫");
    }

    #[test]
    fn test_single_digit() {
        // 5 in binary is 101 → 🔴⚫🔴
        assert_eq!(encode_number(5), "🔴⚫🔴");
    }

    #[test]
    fn test_multiple_bits() {
        // 13 in binary is 1101 → 🔴⚫🔴🔴
        assert_eq!(encode_number(13), "🔴⚫🔴🔴");
    }
}
