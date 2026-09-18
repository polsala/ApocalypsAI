/// Decode a whimsical QR string.
///
/// The function expects the input to start with the literal prefix `QR:`.
/// The remainder of the string is interpreted as the original message written
/// backwards. If the format is correct, the original message is returned.
/// Otherwise, `None` is returned.
pub fn decode_qr(content: &str) -> Option<String> {
    if content.starts_with("QR:") {
        let reversed_part = &content[3..];
        Some(reversed_part.chars().rev().collect())
    } else {
        None
    }
}
