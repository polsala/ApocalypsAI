use std::collections::HashMap;

/// Returns a mapping from emoji characters to their corresponding letters.
fn emoji_map() -> HashMap<char, char> {
    let mut m = HashMap::new();
    m.insert('🌞', 'A');
    m.insert('🌙', 'B');
    m.insert('🌟', 'C');
    m.insert('🔥', 'D');
    m.insert('💧', 'E');
    // 🌪️ consists of a base character and a variation selector; we map the base.
    m.insert('🌪', 'F');
    m.insert('🌈', 'G');
    m.insert('🍎', 'H');
    m.insert('🍞', 'I');
    m.insert('🐍', 'J');
    m
}

/// Decodes a space‑separated emoji string into a plain text string.
/// Unknown emojis are ignored.
pub fn decode(input: &str) -> String {
    let map = emoji_map();
    input
        .split_whitespace()
        .filter_map(|e| e.chars().next())
        .filter_map(|c| map.get(&c).copied())
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_decode_basic() {
        let input = "🌞 🌙 🌟";
        assert_eq!(decode(input), "ABC");
    }

    #[test]
    fn test_decode_with_unknown() {
        let input = "🌞 🛸 🌙";
        // 🛸 is unknown and should be skipped
        assert_eq!(decode(input), "AB");
    }

    #[test]
    fn test_decode_empty() {
        assert_eq!(decode(""), "");
    }
}
