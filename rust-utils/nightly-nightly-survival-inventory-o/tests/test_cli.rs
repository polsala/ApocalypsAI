use assert_cmd::Command;

#[test]
fn test_cli_output() {
    // Mock rationale: we invoke the binary with a deterministic set of items and capacity.
    let mut cmd = Command::cargo_bin("nightly-survival-inventory-optimizer").unwrap();
    cmd.arg("--items")
        .arg("water:3:10,food:5:8,first-aid:2:7,radio:1:4,knife:2:5")
        .arg("--capacity")
        .arg("10");
    cmd.assert()
        .success()
        .stdout(predicates::str::contains("Optimal items (total weight: 8kg, total utility: 26):"))
        .stdout(predicates::str::contains("- water (3kg, utility 10)"))
        .stdout(predicates::str::contains("- first-aid (2kg, utility 7)"))
        .stdout(predicates::str::contains("- radio (1kg, utility 4)"))
        .stdout(predicates::str::contains("- knife (2kg, utility 5)"));
}
