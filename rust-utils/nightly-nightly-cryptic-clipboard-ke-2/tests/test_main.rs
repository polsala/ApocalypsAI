use nightly_cryptic_clipboard_keeper::xor;

#[test]
fn roundtrip_encrypt_decrypt() {
    let passphrase = b"s3cr3tP@ss";
    let original = b"The quick brown fox jumps over the lazy dog.";

    // Encrypt
    let encrypted = xor(original, passphrase);
    // Decrypt (XOR again with same key)
    let decrypted = xor(&encrypted, passphrase);

    assert_eq!(decrypted, original);
}
