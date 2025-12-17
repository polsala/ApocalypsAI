use std::process::Command;
use std::fs;
use tempfile::NamedTempFile;

#[test]
fn test_caesar_cipher_cli() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-cipher-canvas"))
        .args(&["-t", "hello", "-c", "caesar", "-s", "3"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("khoor"));
    assert!(!stdout.contains("Error:"));
}

#[test]
fn test_atbash_cipher_cli() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-cipher-canvas"))
        .args(&["-t", "hello", "-c", "atbash"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Svool"));
    assert!(!stdout.contains("Error:"));
}

#[test]
fn test_vigenere_cipher_cli() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-cipher-canvas"))
        .args(&["-t", "attackatdawn", "-c", "vigenere", "-k", "lemon"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("lxfopvefrnhr"));
    assert!(!stdout.contains("Error:"));
}

#[test]
fn test_caesar_cipher_with_ascii_art() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-cipher-canvas"))
        .args(&["-t", "hello", "-c", "caesar", "-s", "3", "-a"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("khoor"));
    assert!(stdout.contains("*".repeat(9))); // ASCII art border
    assert!(!stdout.contains("Error:"));
}

#[test]
fn test_output_to_file() {
    let temp_file = NamedTempFile::new().expect("Failed to create temp file");
    let file_path = temp_file.path().to_str().unwrap();
    
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-cipher-canvas"))
        .args(&["-t", "hello", "-c", "caesar", "-s", "3", "-o", file_path])
        .output()
        .expect("Failed to execute command");
    
    assert!(output.status.success());
    
    let content = fs::read_to_string(file_path).expect("Failed to read file");
    assert_eq!(content.trim(), "khoor");
}

#[test]
fn test_invalid_cipher_type() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-cipher-canvas"))
        .args(&["-t", "hello", "-c", "invalid"])
        .output()
        .expect("Failed to execute command");
    
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Error:"));
    assert!(stderr.contains("Unknown cipher type"));
    assert!(!output.status.success());
}

#[test]
fn test_missing_vigenere_key() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-cipher-canvas"))
        .args(&["-t", "hello", "-c", "vigenere"])
        .output()
        .expect("Failed to execute command");
    
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Error:"));
    assert!(stderr.contains("Vigenère cipher requires a key"));
    assert!(!output.status.success());
}

#[test]
fn test_invalid_shift_value() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-cipher-canvas"))
        .args(&["-t", "hello", "-c", "caesar", "-s", "abc"])
        .output()
        .expect("Failed to execute command");
    
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Error:"));
    assert!(stderr.contains("Invalid shift value"));
    assert!(!output.status.success());
}

#[test]
fn test_empty_vigenere_key() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-cipher-canvas"))
        .args(&["-t", "hello", "-c", "vigenere", "-k", ""])
        .output()
        .expect("Failed to execute command");
    
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert!(stderr.contains("Error:"));
    assert!(stderr.contains("Vigenère cipher key cannot be empty"));
    assert!(!output.status.success());
}

#[test]
fn test_easter_egg_42() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-cipher-canvas"))
        .args(&["-t", "hello", "-c", "caesar", "-s", "42"])
        .output()
        .expect("Failed to execute command");
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("Beep boop"));
    assert!(stdout.contains("The Answer to the Ultimate Question"));
    assert!(stdout.contains("kzxxa")); // Caesar shift of 42
    assert!(!stdout.contains("Error:"));
}
