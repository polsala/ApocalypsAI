use assert_cmd::Command;
use predicates::str::contains;

#[test]
fn test_cli_output_fixed_seed() {
    let mut cmd = Command::cargo_bin("scavenger_inventory").unwrap();
    cmd.env("SCAV_SEED", "42");
    cmd.assert()
        .success()
        .stdout(contains("4 x Radiation Suit"))
        .stdout(contains("9 x Scrap Metal"))
        .stdout(contains("2 x Old Radio"))
        .stdout(contains("5 x Solar Charger"))
        .stdout(contains("3 x Canned Beans"));
}
