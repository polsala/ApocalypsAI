use std::fs::File;
use std::io::{self, Read, Write};
use std::path::Path;

/// XOR‑cipher that repeats the key over the data.
pub fn xor_cipher(data: &[u8], key: &[u8]) -> Vec<u8> {
    data.iter()
        .enumerate()
        .map(|(i, &b)| b ^ key[i % key.len()])
        .collect()
}

/// Encrypt `plaintext` with `key` and write the raw cipher bytes to `out_path`.
pub fn encrypt_and_save(plaintext: &str, key: &str, out_path: &Path) -> io::Result<()> {
    let cipher_bytes = xor_cipher(plaintext.as_bytes(), key.as_bytes());
    let mut file = File::create(out_path)?;
    file.write_all(&cipher_bytes)?;
    Ok(())
}

/// Read cipher bytes from `in_path`, decrypt with `key`, and return the plaintext string.
pub fn decrypt_from_file(key: &str, in_path: &Path) -> io::Result<String> {
    let mut file = File::open(in_path)?;
    let mut cipher_bytes = Vec::new();
    file.read_to_end(&mut cipher_bytes)?;
    let plain_bytes = xor_cipher(&cipher_bytes, key.as_bytes());
    Ok(String::from_utf8_lossy(&plain_bytes).into_owned())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::env;
    use std::fs;

    #[test]
    fn test_xor_roundtrip() {
        let data = b"The quick brown fox";
        let key = b"key";
        let encrypted = xor_cipher(data, key);
        let decrypted = xor_cipher(&encrypted, key);
        assert_eq!(data.to_vec(), decrypted);
    }

    #[test]
    fn test_encrypt_decrypt_file() {
        // Mock rationale: use a temporary file in the OS temp directory.
        let tmp_dir = env::temp_dir();
        let test_path = tmp_dir.join("nightly_clipboard_crypt_test.bin");
        let plaintext = "Hello, world!";
        let key = "secret";

        // Ensure a clean state before the test.
        let _ = fs::remove_file(&test_path);

        encrypt_and_save(plaintext, key, &test_path).expect("encryption failed");
        let recovered = decrypt_from_file(key, &test_path).expect("decryption failed");
        assert_eq!(plaintext, recovered);

        // Clean up after the test.
        let _ = fs::remove_file(&test_path);
    }
}
