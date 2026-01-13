use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_to_seconds() {
    let mut cmd = Command::cargo_bin("chrono-converter").unwrap();
    cmd.arg("to-seconds")
        .arg("1d2h3m4s")
        .assert()
        .success()
        .stdout(predicate::str::contains("93784"));
}

#[test]
fn test_from_seconds() {
    let mut cmd = Command::cargo_bin("chrono-converter").unwrap();
    cmd.arg("from-seconds")
        .arg("93784")
        .assert()
        .success()
        .stdout(predicate::str::contains("1d2h3m4s"));
}

#[test]
fn test_invalid_input() {
    let mut cmd = Command::cargo_bin("chrono-converter").unwrap();
    cmd.arg("to-seconds")
        .arg("10x")
        .assert()
        .failure()
        .stderr(predicate::str::contains("Unknown unit"));
}

