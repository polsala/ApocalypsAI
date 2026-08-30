use assert_cmd::Command; // For running CLI commands in tests
use predicates::prelude::*;

// Mock rationale: These tests run the actual compiled binary with simulated stdin input.
// They do not interact with the real file system or network, making them deterministic and offline.

#[test]
fn test_basic_calibration() {
    let input = "2023-10-27T10:00:00Z,15.0\n2023-10-27T11:00:00Z,16.0\n2023-10-27T12:00:00Z,14.5";
    let mut cmd = Command::cargo_bin("nightly-chrono-compass-calibrator").unwrap();
    cmd.write_stdin(input)
        .assert()
        .success()
        .stdout(predicate::str::contains("Total observations processed: 3"))
        .stdout(predicate::str::contains("Average observed clock offset: 15.17 seconds"))
        .stdout(predicate::str::contains("Advance local clock by 15.17 seconds."));
}

#[test]
fn test_no_observations() {
    let input = "";
    let mut cmd = Command::cargo_bin("nightly-chrono-compass-calibrator").unwrap();
    cmd.write_stdin(input)
        .assert()
        .success()
        .stdout(predicate::str::contains("No observations found. Cannot calibrate chrono-compass."));
}

#[test]
fn test_negative_offset() {
    let input = "2023-10-27T10:00:00Z,-5.0\n2023-10-27T11:00:00Z,-6.0";
    let mut cmd = Command::cargo_bin("nightly-chrono-compass-calibrator").unwrap();
    cmd.write_stdin(input)
        .assert()
        .success()
        .stdout(predicate::str::contains("Total observations processed: 2"))
        .stdout(predicate::str::contains("Average observed clock offset: -5.50 seconds"))
        .stdout(predicate::str::contains("Retard local clock by 5.50 seconds."));
}

#[test]
fn test_zero_offset() {
    let input = "2023-10-27T10:00:00Z,0.0\n2023-10-27T11:00:00Z,0.0";
    let mut cmd = Command::cargo_bin("nightly-chrono-compass-calibrator").unwrap();
    cmd.write_stdin(input)
        .assert()
        .success()
        .stdout(predicate::str::contains("Total observations processed: 2"))
        .stdout(predicate::str::contains("Average observed clock offset: 0.00 seconds"))
        .stdout(predicate::str::contains("No correction needed."));
}

#[test]
fn test_invalid_input_format() {
    let input = "not-a-date,10.0\n2023-10-27T11:00:00Z,invalid-offset";
    let mut cmd = Command::cargo_bin("nightly-chrono-compass-calibrator").unwrap();
    cmd.write_stdin(input)
        .assert()
        .failure() // Expecting a parse error, which should result in a non-zero exit code
        .stderr(predicate::str::contains("CSV deserialize error")); // Check for specific error message
}
