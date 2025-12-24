#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn roundtrip_encrypt_decrypt() {
        let plaintext = "The quick brown fox jumps over the lazy dog.";
        let passphrase = "s3cr3t";

        let encrypted = encrypt(plaintext, passphrase);
        // Ensure encrypted is not the same as plaintext
        assert_ne!(encrypted, plaintext);

        let decrypted = decrypt(&encrypted, passphrase).expect("Decryption failed");
        assert_eq!(decrypted, plaintext);
    }

    #[test]
    fn decrypt_invalid_base64() {
        let result = decrypt("!!!notbase64!!!", "any");
        assert!(result.is_err());
    }

    #[test]
    fn encrypt_decrypt_empty() {
        let encrypted = encrypt("", "key");
        let decrypted = decrypt(&encrypted, "key").unwrap();
        assert_eq!(decrypted, "");
    }
}
