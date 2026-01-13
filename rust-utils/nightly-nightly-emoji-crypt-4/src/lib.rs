pub const EMOJI_ALPHABET: [&str; 64] = [
    "😀","😃","😄","😁","😆","😅","😂","🤣",
    "😊","😇","🙂","🙃","😉","😌","😍","🥰",
    "😘","😗","😙","😚","😋","😛","😝","😜",
    "🤪","🤨","🧐","🤓","😎","🥳","🤩","😏",
    "😒","😞","😔","😟","😕","🙁","☹️","😣",
    "😖","😫","😩","🥺","😢","😭","😤","😠",
    "😡","🤬","🤯","😳","🥵","🥶","😱","😨",
    "😰","😥","🤗","🤔","🤭","🤫","🤥","😶",
    "😐","😑","🫠","🤐"
];

/// Encode a UTF‑8 string into an emoji sequence.
pub fn encode(text: &str) -> String {
    // Encode to standard Base64 first.
    let b64 = base64::engine::general_purpose::STANDARD.encode(text);
    // Translate each Base64 character to its corresponding emoji.
    b64.chars()
        .map(|c| {
            let idx = match c {
                'A'..='Z' => (c as u8 - b'A') as usize,
                'a'..='z' => (c as u8 - b'a' + 26) as usize,
                '0'..='9' => (c as u8 - b'0' + 52) as usize,
                '+' => 62,
                '/' => 63,
                _ => 0, // padding or unexpected chars map to first emoji
            };
            EMOJI_ALPHABET[idx]
        })
        .collect()
}

/// Decode an emoji sequence back into the original UTF‑8 string.
pub fn decode(emojis: &str) -> Result<String, String> {
    let mut b64 = String::new();
    let mut chars = emojis.chars();
    while let Some(ch) = chars.next() {
        // Find the index of the emoji in the alphabet.
        let idx_opt = EMOJI_ALPHABET.iter().position(|&e| e == ch.to_string());
        let idx = match idx_opt {
            Some(i) => i,
            None => return Err(format!("Unknown emoji: {}", ch)),
        };
        let c = match idx {
            0..=25 => ((b'A' as u8) + idx as u8) as char,
            26..=51 => ((b'a' as u8) + (idx as u8 - 26)) as char,
            52..=61 => ((b'0' as u8) + (idx as u8 - 52)) as char,
            62 => '+',
            63 => '/',
            _ => '=',
        };
        b64.push(c);
    }
    // Decode Base64 back to bytes, then to UTF‑8 string.
    base64::engine::general_purpose::STANDARD
        .decode(&b64)
        .map_err(|e| e.to_string())
        .and_then(|bytes| String::from_utf8(bytes).map_err(|e| e.to_string()))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn roundtrip_simple() {
        let original = "Hello, world!";
        let encoded = encode(original);
        let decoded = decode(&encoded).expect("decode failed");
        assert_eq!(decoded, original);
    }

    #[test]
    fn roundtrip_unicode() {
        let original = "🚀✨🌟";
        let encoded = encode(original);
        let decoded = decode(&encoded).expect("decode failed");
        assert_eq!(decoded, original);
    }
}
