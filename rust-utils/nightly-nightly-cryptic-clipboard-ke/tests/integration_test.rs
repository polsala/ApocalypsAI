use nightly_cryptic_clipboard_keeper::{encrypt, decrypt};

#[test]
fn round_trip() {
    let plaintext = "The quick brown fox jumps over the lazy dog.";
    let pass = "s3cr3t!";
    let enc = encrypt(plaintext, pass);
    let dec = decrypt(&enc, pass).expect("decryption failed");
    assert_eq!(dec, plaintext);
}

#[test]
fn wrong_passphrase_fails() {
    let plaintext = "HiddenMessage";
    let pass = "right";
    let wrong = "wrong";
    let enc = encrypt(plaintext, pass);
    let dec = decrypt(&enc, wrong).expect("decryption succeeded");
    assert_ne!(dec, plaintext);
}

#[test]
fn invalid_base64_returns_error() {
    let result = decrypt("!!!notbase64!!!", "any");
    assert!(result.is_err());
}
