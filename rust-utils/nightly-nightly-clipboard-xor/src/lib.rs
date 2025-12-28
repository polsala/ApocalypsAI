pub fn xor(data: &[u8], key: &[u8]) -> Vec<u8> {
    data.iter()
        .zip(key.iter().cycle())
        .map(|(d, k)| d ^ k)
        .collect()
}
\npub fn to_hex(bytes: &[u8]) -> String {
    bytes.iter().map(|b| format!("{:02x}", b)).collect()
}
\npub fn from_hex(s: &str) -> Result<Vec<u8>, String> {
    if s.len() % 2 != 0 {
        return Err("Hex string has odd length".into());
    }
    (0..s.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&s[i..i + 2], 16).map_err(|e| e.to_string()))
        .collect()
}
\npub fn encrypt(text: &str, key: &str) -> String {
    let encrypted = xor(text.as_bytes(), key.as_bytes());
    to_hex(&encrypted)
}
\npub fn decrypt(hex: &str, key: &str) -> Result<String, String> {
    let bytes = from_hex(hex)?;
    let decrypted = xor(&bytes, key.as_bytes());
    String::from_utf8(decrypted).map_err(|e| e.to_string())
}
