pub fn encode(input: &str) -> String {
    input.chars().map(|c| {
        if c.is_ascii_alphabetic() {
            let base = 0x1F1E6u32; // Regional Indicator Symbol Letter A
            let offset = c.to_ascii_uppercase() as u32 - 'A' as u32;
            std::char::from_u32(base + offset).unwrap_or(c)
        } else {
            c
        }
    }).collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_encode_basic() {
        let input = "ABC xyz!";
        let expected = "🇦🇧🇨 🇽🇾🇿!";
        assert_eq!(encode(input), expected);
    }
    #[test]
    fn test_encode_non_alpha() {
        let input = "123-!@#";
        let expected = "123-!@#";
        assert_eq!(encode(input), expected);
    }
}
