#![allow(unused_imports)]

use std::process::Command;
use std::fs;
use std::path::PathBuf;
use tempfile::tempdir;

#[test]
fn test_key_generation() {
    // Create a temporary directory for key output
    let dir = tempdir().expect("failed to create temp dir");
    let out_dir = dir.path().to_str().expect("invalid temp dir path");
    let key_name = "test_key";

    // Run the binary via cargo
    let output = Command::new("cargo")
        .args(&["run", "--quiet", "--", out_dir, key_name])
        .output()
        .expect("failed to execute cargo run");

    assert!(output.status.success(), "binary exited with error");

    // Capture stdout and ensure it contains an OpenSSH public key
    let stdout = String::from_utf8(output.stdout).expect("stdout not UTF-8");
    assert!(stdout.contains("ssh-rsa"), "stdout does not contain public key");

    // Verify files were created
    let priv_path = PathBuf::from(out_dir).join(key_name);
    let pub_path = PathBuf::from(out_dir).join(format!("{}.pub", key_name));

    assert!(priv_path.exists(), "private key file missing");
    assert!(pub_path.exists(), "public key file missing");

    // Check private key format
    let priv_contents = fs::read_to_string(&priv_path).expect("failed to read private key");
    assert!(priv_contents.contains("-----BEGIN RSA PRIVATE KEY-----"), "private key not PEM formatted");

    // Check public key format
    let pub_contents = fs::read_to_string(&pub_path).expect("failed to read public key");
    assert!(pub_contents.starts_with("ssh-rsa"), "public key not OpenSSH format");
}
