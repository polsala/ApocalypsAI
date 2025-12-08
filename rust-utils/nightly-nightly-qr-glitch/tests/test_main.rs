#[test]
fn test_qr_output_contains_dark_blocks() {
    // Invoke the compiled binary with a simple argument.
    let output = std::process::Command::new(env!("CARGO_BIN_EXE_nightly-qr-glitch"))
        .arg("test")
        .output()
        .expect("Failed to execute nightly-qr-glitch binary");
    let stdout = std::str::from_utf8(&output.stdout).expect("Output not valid UTF-8");
    // The ASCII QR should contain at least one dark block ("██" or "▓▓").
    assert!(stdout.contains("██") || stdout.contains("▓▓"), "QR output does not contain expected dark block characters");
}
