use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_colorization() {
    let input = "INFO Starting\nWARN Low disk\nERROR Crash\nNormal line\n";
    let mut cmd = Command::cargo_bin("nightly-log-colorizer").unwrap();
    cmd.write_stdin(input)
        .assert()
        .success()
        .stdout(predicate::str::contains("\x1b[32mINFO Starting\x1b[0m"))
        .stdout(predicate::str::contains("\x1b[33mWARN Low disk\x1b[0m"))
        .stdout(predicate::str::contains("\x1b[31mERROR Crash\x1b[0m"))
        .stdout(predicate::str::contains("Normal line"));
}
