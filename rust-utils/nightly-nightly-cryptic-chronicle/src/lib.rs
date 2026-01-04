pub fn xor(data: &[u8], key: &[u8]) -> Vec<u8> {
    data.iter()
        .enumerate()
        .map(|(i, &b)| b ^ key[i % key.len()])
        .collect()
}

pub fn encrypt(message: &str, key: &str) -> String {
    use std::time::{SystemTime, UNIX_EPOCH};
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("Time went backwards")
        .as_secs();
    let mut bytes = now.to_be_bytes().to_vec();
    bytes.extend_from_slice(message.as_bytes());
    let xored = xor(&bytes, key.as_bytes());
    base64::engine::general_purpose::STANDARD.encode(&xored)
}

pub fn decrypt(ciphertext: &str, key: &str) -> Result<(String, u64), String> {
    let decoded = base64::engine::general_purpose::STANDARD
        .decode(ciphertext)
        .map_err(|e| format!("Base64 decode error: {}", e))?;
    let xored = xor(&decoded, key.as_bytes());
    if xored.len() < 8 {
        return Err("Decoded data too short".into());
    }
    let (ts_bytes, msg_bytes) = xored.split_at(8);
    let timestamp = u64::from_be_bytes(ts_bytes.try_into().unwrap());
    let message = String::from_utf8(msg_bytes.to_vec())
        .map_err(|e| format!("UTF-8 error: {}", e))?;
    Ok((message, timestamp))
}
