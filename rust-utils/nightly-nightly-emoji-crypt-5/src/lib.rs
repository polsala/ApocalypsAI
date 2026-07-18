use lazy_static::lazy_static;
use std::collections::HashMap;

lazy_static! {
    static ref ENCODE_MAP: HashMap<char, &'static str> = {
        let mut m = HashMap::new();
        // a‑z
        let emojis = [
            "🦊", "🐘", "🦁", "🐼", "🐨", "🐯", "🦓", "🐸", "🐵", "🐔",
            "🐧", "🐦", "🐤", "🐣", "🦆", "🦅", "🦉", "🦇", "🐺", "🐗",
            "🐴", "🦄", "🐝", "🐛", "🦋", "🐌",
        ];
        for (i, ch) in ('a'..='z').enumerate() {
            m.insert(ch, emojis[i]);
        }
        // digits 0‑9
        let digit_emojis = [
            "0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣",
        ];
        for (i, ch) in ('0'..='9').enumerate() {
            m.insert(ch, digit_emojis[i]);
        }
        // space
        m.insert(' ', " ");
        m
    };
    static ref DECODE_MAP: HashMap<&'static str, char> = {
        let mut m = HashMap::new();
        for (k, v) in ENCODE_MAP.iter() {
            m.insert(*v, *k);
        }
        m
    };
}

/// Encode a plain‑text string into an emoji sequence.
pub fn encode(input: &str) -> String {
    input
        .chars()
        .map(|c| {
            let lower = c.to_ascii_lowercase();
            ENCODE_MAP.get(&lower).copied().unwrap_or_else(|| c.to_string().as_str())
        })
        .collect::<Vec<&str>>()
        .join("")
}

/// Decode an emoji sequence back into plain text.
pub fn decode(input: &str) -> String {
    // Because some emojis are multi‑character (e.g., "0️⃣"), we need to iterate over the string
    // and greedily match the longest possible emoji from the map.
    let mut result = String::new();
    let mut i = 0;
    let chars: Vec<char> = input.chars().collect();
    while i < chars.len() {
        // Try to match two‑char emojis (most digit emojis are two codepoints)
        let mut matched = None;
        // Check up to 4 chars ahead (some animal emojis are single codepoint but safe to limit)
        for len in (1..=4).rev() {
            if i + len > chars.len() {
                continue;
            }
            let slice: String = chars[i..i + len].iter().collect();
            if let Some(&ch) = DECODE_MAP.get(slice.as_str()) {
                matched = Some((ch, len));
                break;
            }
        }
        if let Some((ch, len)) = matched {
            result.push(ch);
            i += len;
        } else {
            // No match – preserve the original character
            result.push(chars[i]);
            i += 1;
        }
    }
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_encode() {
        let plain = "abc xyz 123";
        let encoded = encode(plain);
        // Expected emojis based on the static tables
        let expected = "🦊🐘🦁 🐌🦊🦁 1️⃣2️⃣3️⃣";
        assert_eq!(encoded, expected);
    }

    #[test]
    fn test_basic_decode() {
        let encoded = "🦊🐘🦁 🐌🦊🦁 1️⃣2️⃣3️⃣";
        let decoded = decode(encoded);
        assert_eq!(decoded, "abc xyz 123");
    }

    #[test]
    fn test_roundtrip() {
        let original = "rust 2024";
        let enc = encode(original);
        let dec = decode(&enc);
        assert_eq!(dec, original);
    }
}
