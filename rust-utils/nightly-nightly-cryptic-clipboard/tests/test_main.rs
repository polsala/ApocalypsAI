use nightly_cryptic_clipboard::{encrypt, decrypt};

#[test]
fn roundtrip_encrypt_decrypt() {
    let pass = "s3cr3t";
    let plain = "The quick brown fox jumps over the lazy dog";
    let enc = encrypt(pass, plain);
    let dec = decrypt(pass, &enc).expect("decryption failed");
    assert_eq!(plain, dec);
}

#[test]
fn decrypt_invalid_base64() {
    let err = decrypt("key", "@@@invalid@@@").unwrap_err();
    assert!(err.contains("Base64"));
}
