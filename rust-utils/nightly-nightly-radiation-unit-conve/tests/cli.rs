use assert_cmd::Command;
use predicates::str::contains;

#[test]
fn test_sv_to_msv() {
    let mut cmd = Command::cargo_bin("radiation-unit-converter").unwrap();
    cmd.arg("1").arg("Sv").arg("mSv");
    cmd.assert()
        .success()
        .stdout(contains("1000.000000 mSv"));
}

#[test]
fn test_rem_to_rad() {
    let mut cmd = Command::cargo_bin("radiation-unit-converter").unwrap();
    cmd.arg("5").arg("rem").arg("rad");
    cmd.assert()
        .success()
        .stdout(contains("5.000000 rad"));
}
