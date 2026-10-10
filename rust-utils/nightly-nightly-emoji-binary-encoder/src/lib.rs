/// Convert a non‑negative integer to an emoji‑based binary string.
///
/// * `0` → "⚫"
/// * `1` → "🔴"
///
/// The function returns a `String` where each bit of the binary representation
/// is replaced by the corresponding emoji. The most‑significant bit appears first.
pub fn encode_number(num: u64) -> String {
    if num == 0 {
        return "⚫".to_string();
    }
    let binary = format!("{:b}", num);
    binary
        .chars()
        .map(|c| if c == '1' { "🔴" } else { "⚫" })
        .collect()
}
