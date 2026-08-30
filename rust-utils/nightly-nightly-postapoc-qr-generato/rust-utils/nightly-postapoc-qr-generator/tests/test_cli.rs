use assert_cmd::Command;
use predicates::str::contains;

#[test]
fn test_help_output() {
    let mut cmd = Command::cargo_bin("postapoc-qr-generator").unwrap();
    cmd.arg("--help");
    cmd.assert()
        .success()
        .stdout(contains("Generate an ASCII QR code for the wasteland"));
}
