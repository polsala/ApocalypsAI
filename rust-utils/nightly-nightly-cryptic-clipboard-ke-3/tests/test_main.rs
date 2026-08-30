use cryptic_clipboard::xor_cipher;

#[test]
fn test_encrypt_decrypt_roundtrip() {
    let plaintext = b"The quick brown fox jumps over the lazy dog.";
    let passphrase = b"secret";

    let encrypted = xor_cipher(plaintext, passphrase);
    let decrypted = xor_cipher(&encrypted, passphrase);
    assert_eq!(plaintext.to_vec(), decrypted);
}

#[test]
fn test_empty_input() {
    let plaintext: &[u8] = b"";
    let passphrase = b"anykey";
    let encrypted = xor_cipher(plaintext, passphrase);
    let decrypted = xor_cipher(&encrypted, passphrase);
    assert_eq!(plaintext.to_vec(), decrypted);
}
