// Integration test that runs the compiled binary and checks exit status.
// This test does not depend on external services – it is fully deterministic.

use std::process::Command;

#[test]
fn cli_returns_success_and_non_empty_output() {
    // Build the binary first (cargo test builds it automatically).
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-qr-artefact"))
        .arg("hello world")
        .output()
        .expect("Failed to execute binary");
    assert!(output.status.success(), "Binary should exit with 0");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(!stdout.trim().is_empty(), "STDOUT should contain the ASCII QR code");
    // Ensure only allowed characters are present.
    for ch in stdout.chars() {
        assert!(ch == ' ' || ch == '\u{2588}' || ch == '\n', "Unexpected character in CLI output");
    }
}
