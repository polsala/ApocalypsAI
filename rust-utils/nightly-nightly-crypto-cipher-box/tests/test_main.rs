use nightly_crypto_cipher_box::{encrypt, decrypt};

#[test]
fn test_encrypt_basic() {
    let message = "hello";
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let key = 3;
    let encrypted = encrypt(message, alphabet, key);
    assert_eq!(encrypted, "khoor");
}

#[test]
fn test_decrypt_basic() {
    let message = "khoor";
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let key = 3;
    let decrypted = decrypt(message, alphabet, key);
    assert_eq!(decrypted, "hello");
}

#[test]
fn test_encrypt_with_uppercase() {
    let message = "Hello";
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let key = 3;
    let encrypted = encrypt(message, alphabet, key);
    assert_eq!(encrypted, "Khoor");
}

#[test]
fn test_decrypt_with_uppercase() {
    let message = "Khoor";
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let key = 3;
    let decrypted = decrypt(message, alphabet, key);
    assert_eq!(decrypted, "Hello");
}

#[test]
fn test_encrypt_with_punctuation() {
    let message = "hello, world!";
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let key = 3;
    let encrypted = encrypt(message, alphabet, key);
    assert_eq!(encrypted, "khoor, zruog!");
}

#[test]
fn test_decrypt_with_punctuation() {
    let message = "khoor, zruog!";
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let key = 3;
    let decrypted = decrypt(message, alphabet, key);
    assert_eq!(decrypted, "hello, world!");
}

#[test]
fn test_encrypt_custom_alphabet() {
    let message = "abc";
    let alphabet = "abc";
    let key = 1;
    let encrypted = encrypt(message, alphabet, key);
    assert_eq!(encrypted, "bca");
}

#[test]
fn test_decrypt_custom_alphabet() {
    let message = "bca";
    let alphabet = "abc";
    let key = 1;
    let decrypted = decrypt(message, alphabet, key);
    assert_eq!(decrypted, "abc");
}

#[test]
fn test_encrypt_empty_message() {
    let message = "";
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let key = 3;
    let encrypted = encrypt(message, alphabet, key);
    assert_eq!(encrypted, "");
}

#[test]
fn test_decrypt_empty_message() {
    let message = "";
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let key = 3;
    let decrypted = decrypt(message, alphabet, key);
    assert_eq!(decrypted, "");
}

#[test]
fn test_encrypt_key_larger_than_alphabet() {
    let message = "hello";
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let key = 30;
    let encrypted = encrypt(message, alphabet, key);
    assert_eq!(encrypted, "khoor");
}

#[test]
fn test_decrypt_key_larger_than_alphabet() {
    let message = "khoor";
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let key = 30;
    let decrypted = decrypt(message, alphabet, key);
    assert_eq!(decrypted, "hello");
}
