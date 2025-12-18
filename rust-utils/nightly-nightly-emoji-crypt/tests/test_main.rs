#[cfg(test)]
mod tests {
    use super::super::decode;

    #[test]
    fn test_basic_mapping() {
        // 🐱🐶🐭 should map to "abc"
        let input = "🐱🐶🐭";
        let expected = "abc";
        assert_eq!(decode(input), expected);
    }

    #[test]
    fn test_unknown_emoji_ignored() {
        // 🦄 is not in the table and should be skipped.
        let input = "🐱🦄🐶";
        let expected = "ab";
        assert_eq!(decode(input), expected);
    }

    #[test]
    fn test_empty_input() {
        let input = "";
        let expected = "";
        assert_eq!(decode(input), expected);
    }
}
