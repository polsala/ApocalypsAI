pub const EMOJI_MAP: [&str; 16] = [
    "😀",
    "😁",
    "😂",
    "🤣",
    "😃",
    "😄",
    "😅",
    "😆",
    "😉",
    "😊",
    "😋",
    "😎",
    "😍",
    "😘",
    "🥰",
    "🤩",
];

/// Encode a UTF‑8 string into an emoji‑hex representation.
pub fn encode(input: &str) -> String {
    let mut out = String::new();
    for b in input.bytes() {
        let hi = (b >> 4) as usize;
        let lo = (b & 0x0F) as usize;
        out.push_str(EMOJI_MAP[hi]);
        out.push_str(EMOJI_MAP[lo]);
    }
    out
}

/// Decode an emoji‑hex string back into the original UTF‑8 text.
/// Returns an error string if the input is malformed or not valid UTF‑8.
pub fn decode(input: &str) -> Result<String, String> {
    let chars: Vec<char> = input.chars().collect();
    if chars.len() % 2 != 0 {
        return Err("Invalid emoji‑hex length".into());
    }
    let mut bytes = Vec::new();
    for i in (0..chars.len()).step_by(2) {
        let hi = EMOJI_MAP
            .iter()
            .position(|&e| e.chars().next().unwrap() == chars[i])
            .ok_or_else(|| format!("Invalid emoji: {}", chars[i]))?;
        let lo = EMOJI_MAP
            .iter()
            .position(|&e| e.chars().next().unwrap() == chars[i + 1])
            .ok_or_else(|| format!("Invalid emoji: {}", chars[i + 1]))?;
        bytes.push(((hi as u8) << 4) | (lo as u8));
    }
    String::from_utf8(bytes).map_err(|e| e.to_string())
}
