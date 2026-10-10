use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn cli_outputs_safe() {
    let mut cmd = Command::cargo_bin("radiation_calc").unwrap();
    cmd.arg("0.5").arg("48");
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Total dose: 24.00 mSv (safe)"));
}

#[test]
fn cli_outputs_exceeds() {
    let mut cmd = Command::cargo_bin("radiation_calc").unwrap();
    cmd.arg("5").arg("30");
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("EXCEEDS safe limit"));
}
