use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn cli_produces_output() {
    // Run the compiled binary with a sample string.
    let mut cmd = Command::cargo_bin("nightly-cryptic-qr-encoder").expect("binary exists");
    cmd.arg("Apocalypse");
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("█"))
        .stdout(predicate::str::contains("▇").or(predicate::str::contains("▆")));
}
