use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn cli_runs_with_defaults() {
    let mut cmd = Command::cargo_bin("nightly-wasteland-compass").unwrap();
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Current bearing: 0°"));
}

#[test]
fn cli_accepts_custom_bearing_and_drift() {
    let mut cmd = Command::cargo_bin("nightly-wasteland-compass").unwrap();
    cmd.args(["--bearing", "90", "--max-drift", "45"])
        .assert()
        .success()
        .stdout(predicate::str::contains("Current bearing: 90°"))
        .stdout(predicate::str::contains("New deterministic bearing:"));
}
