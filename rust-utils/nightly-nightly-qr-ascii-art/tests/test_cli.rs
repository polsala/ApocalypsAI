use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_qr_output() {
    // Mock rationale: we test that the CLI produces a nonâempty ASCII QR code for a known input.
    let mut cmd = Command::cargo_bin(env!("CARGO_PKG_NAME")).unwrap();
    cmd.arg("test");
    let assert = cmd.assert().success();
    let output = String::from_utf8(assert.get_output().stdout.clone()).unwrap();
    // The QR code should contain at least one dark block character (U+2588)
    assert!(output.contains("â"));
}
