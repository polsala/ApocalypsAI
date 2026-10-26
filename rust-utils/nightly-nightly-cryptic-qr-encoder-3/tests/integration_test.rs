use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_cli_output_non_empty() {
    let mut cmd = Command::cargo_bin("nightly-cryptic-qr-encoder").unwrap();
    cmd.arg("test");
    cmd.assert()
        .success()
        .stdout(predicate::str::is_match(r"^[█ \n]+$").unwrap());
}
