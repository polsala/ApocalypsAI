pub fn xor_cipher(data: &[u8], key: &[u8]) -> Vec<u8> {
    data.iter()
        .enumerate()
        .map(|(i, &b)| b ^ key[i % key.len()])
        .collect()
}

pub fn encrypt(passphrase: &str, text: &str) -> String {
    let cipher_bytes = xor_cipher(text.as_bytes(), passphrase.as_bytes());
    base64::engine::general_purpose::STANDARD.encode(&cipher_bytes)
}

pub fn decrypt(passphrase: &str, cipher: &str) -> Result<String, String> {
    let cipher_bytes = base64::engine::general_purpose::STANDARD
        .decode(cipher)
        .map_err(|e| format!("Base64 decode error: {}", e))?;
    let plain_bytes = xor_cipher(&cipher_bytes, passphrase.as_bytes());
    String::from_utf8(plain_bytes).map_err(|e| format!("UTF-8 error: {}", e))
}
