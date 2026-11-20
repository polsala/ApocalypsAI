use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn cli_selects_optimal_items() {
    // Mock rationale: deterministic input, expecting known output.
    let mut cmd = Command::cargo_bin("nightly-scavenger-knapsack").unwrap();
    cmd.arg("5")
        .arg("water:3:10,food:2:7,medkit:5:12");
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("water"))
        .stdout(predicate::str::contains("food"))
        .stdout(predicate::str::contains("Total value: 17"));
}
