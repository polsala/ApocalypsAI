use assert_cmd::Command;

#[test]
fn cli_without_radiation_produces_output() {
    let mut cmd = Command::cargo_bin("nightly-apocalypse-qr").unwrap();
    cmd.arg("hello");
    cmd.assert().success().stdout(predicates::str::contains("█"));
}

#[test]
fn cli_with_radiation_has_border() {
    let mut cmd = Command::cargo_bin("nightly-apocalypse-qr").unwrap();
    cmd.args(["world", "--radiation"]);
    let assert = cmd.assert().success();
    let out = String::from_utf8(assert.get_output().stdout.clone()).unwrap();
    let first_line = out.lines().next().unwrap();
    assert!(first_line.chars().all(|c| c == '☢'));
    let last_line = out.lines().last().unwrap();
    assert_eq!(first_line, last_line);
}
