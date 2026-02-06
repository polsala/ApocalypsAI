use nightly_quantum_entropy_seeder::*;
use std::process::Command;

#[tokio::test]
async fn test_generate_deterministic_seed_cli() {
    let output = Command::new("cargo")
        .args(["run", "--release", "--", "--deterministic", "--format", "hex", "--bits", "256"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert_eq!(stdout.trim(), "2a");
}

#[tokio::test]
async fn test_generate_seed_with_quantum_fallback() {
    let output = Command::new("cargo")
        .args(["run", "--release", "--", "--format", "hex", "--bits", "128", "--pool-size", "10", "--fallback", "atmospheric"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(!stdout.trim().is_empty());
    assert!(stdout.trim().chars().all(|c| c.is_ascii_hexdigit()));
}

#[tokio::test]
async fn test_generate_seed_with_atmospheric_fallback() {
    let output = Command::new("cargo")
        .args(["run", "--release", "--", "--format", "base64", "--bits", "64", "--pool-size", "5", "--fallback", "quantum"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(!stdout.trim().is_empty());
    // Base64 should only contain valid base64 characters
    assert!(stdout.trim().chars().all(|c| c.is_ascii_alphanumeric() || c == '+' || c == '/' || c == '='));
}

#[tokio::test]
async fn test_generate_decimal_seed() {
    let output = Command::new("cargo")
        .args(["run", "--release", "--", "--format", "decimal", "--bits", "32", "--pool-size", "20"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(!stdout.trim().is_empty());
    assert!(stdout.trim().chars().all(|c| c.is_ascii_digit()));
}

#[tokio::test]
async fn test_help_command() {
    let output = Command::new("cargo")
        .args(["run", "--release", "--", "--help"])
        .output()
        .expect("Failed to execute command");

    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout).unwrap();
    assert!(stdout.contains("A CLI tool that generates cryptographically strong random seeds using quantum noise"));
    assert!(stdout.contains("--format"));
    assert!(stdout.contains("--bits"));
    assert!(stdout.contains("--pool-size"));
}
