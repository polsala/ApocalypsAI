#[cfg(test)]
mod tests {
    use clipboard_xor::{decrypt, encrypt};

    #[test]
    fn test_encrypt_known_vector() {
        // "hello" XOR with key "key" should produce 030015070a
        let text = "hello";
        let key = "key";
        let encrypted = encrypt(text, key);
        assert_eq!(encrypted, "030015070a");
    }

    #[test]
    fn test_roundtrip_encrypt_decrypt() {
        let original = "The quick brown fox jumps over the lazy dog";
        let key = "secretpass";
        let enc = encrypt(original, key);
        let dec = decrypt(&enc, key).expect("decryption failed");
        assert_eq!(dec, original);
    }
}

