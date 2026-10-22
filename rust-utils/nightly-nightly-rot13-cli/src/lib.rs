/// Apply ROT13 encoding to the given string.
///
/// This function works on ASCII alphabetic characters only. Non‑alphabetic
/// characters (digits, punctuation, whitespace, etc.) are left unchanged.
///
/// # Examples
///
/// ```
/// let encoded = nightly_rot13_cli::rot13("Hello, World!");
/// assert_eq!(encoded, "Uryyb, Jbeyq!");
/// ```
pub fn rot13(input: &str) -> String {
    input
        .chars()
        .map(|c| match c {
            'a'..='z' => (((c as u8 - b'a' + 13) % 26) + b'a') as char,
            'A'..='Z' => (((c as u8 - b'A' + 13) % 26) + b'A') as char,
            _ => c,
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic() {
        assert_eq!(rot13("Hello, World!"), "Uryyb, Jbeyq!");
    }

    #[test]
    fn test_round_trip() {
        let original = "Apocalypse 2026";
        let encoded = rot13(original);
        let decoded = rot13(&encoded);
        assert_eq!(decoded, original);
    }

    #[test]
    fn test_non_alpha_unchanged() {
        assert_eq!(rot13("1234!@#$"), "1234!@#$");
    }
}
