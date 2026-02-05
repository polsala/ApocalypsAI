use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn cli_under_limit() {
    let mut cmd = Command::cargo_bin("nightly-scavenger-inventory").unwrap();
    cmd.arg("10")
        .arg("water:2")
        .arg("food:3")
        .arg("ammo:1");
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Total weight: 6"));
}

#[test]
fn cli_over_limit() {
    let mut cmd = Command::cargo_bin("nightly-scavenger-inventory").unwrap();
    cmd.arg("5")
        .arg("water:2")
        .arg("food:3")
        .arg("toolkit:5");
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Total weight: 10"))
        .stdout(predicate::str::contains("Limit exceeded by 5"))
        .stdout(predicate::str::contains("Suggested items to drop: toolkit (5"));
}
