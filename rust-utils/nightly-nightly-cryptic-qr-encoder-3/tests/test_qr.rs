use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_qr_output_nonempty() {
    let mut cmd = Command::cargo_bin("nightly-cryptic-qr-encoder").unwrap();
    cmd.arg("A");
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("█"));
}
