use assert_cmd::Command;
use predicates::prelude::*;
use std::fs;
use std::path::Path;

#[test]
fn encrypt_decrypt_roundtrip() {
    // Ensure a clean environment
    let out_file = "test_vault.bin";
    if Path::new(out_file).exists() {
        fs::remove_file(out_file).unwrap();
    }

    // Encrypt the secret
    Command::cargo_bin("nightly-cryptic-vault")
        .unwrap()
        .args(&["encrypt", "--passphrase", "s3cr3t", "--output", out_file])
        .write_stdin("my secret")
        .assert()
        .success()
        .stderr(predicate::str::contains("Encrypted data written to"));

    // Decrypt and capture output
    let assert = Command::cargo_bin("nightly-cryptic-vault")
        .unwrap()
        .args(&["decrypt", "--passphrase", "s3cr3t", "--input", out_file])
        .assert()
        .success()
        .stdout(predicate::eq("my secret"));

    // Clean up
    fs::remove_file(out_file).unwrap();
    assert;
}

