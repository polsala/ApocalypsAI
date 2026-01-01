use std::env;
use std::fs;
use std::path::Path;

use nightly_clipboard_crypt::{decrypt_from_file, encrypt_and_save};

#[test]
fn integration_encrypt_decrypt() {
    // Mock rationale: operate in a temporary directory to avoid side effects.
    let tmp_dir = env::temp_dir();
    let file_path = tmp_dir.join("nightly_clipboard_crypt_integ.bin");
    let secret = "integrity-key";
    let message = "Integration test payload";

    // Clean any previous artifact.
    let _ = fs::remove_file(&file_path);

    encrypt_and_save(message, secret, &file_path).expect("failed to encrypt");
    let result = decrypt_from_file(secret, &file_path).expect("failed to decrypt");
    assert_eq!(message, result);

    // Clean up.
    let _ = fs::remove_file(&file_path);
}
