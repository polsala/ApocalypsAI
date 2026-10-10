use assert_cmd::Command;
use predicates::str::contains;

#[test]
fn test_qr_output_contains_blocks() {
    // Run the binary with a simple input
    let mut cmd = Command::cargo_bin("cryptic-qr").expect("binary not found");
    cmd.arg("test");
    cmd.assert()
        .success()
        .stdout(contains("██")); // ASCII QR contains block characters
}

#[test]
fn test_reverse_option() {
    let mut cmd = Command::cargo_bin("cryptic-qr").expect("binary not found");
    cmd.args(&["-r", "abc"]);
    cmd.assert()
        .success()
        .stdout(contains("██")); // Still produces a QR code
}
