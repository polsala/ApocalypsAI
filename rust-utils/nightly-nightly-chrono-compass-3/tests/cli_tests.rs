use assert_cmd::Command;
use chrono::{Utc, TimeZone};

// Mock rationale: The `get_current_time` function in `src/main.rs` is conditionally compiled.
// For tests, it returns a fixed `2024-07-15 12:00:00 UTC`. This ensures tests are deterministic.

#[test]
fn test_until_future() {
    let mut cmd = Command::cargo_bin("nightly-chrono-compass").unwrap();
    cmd.arg("until")
       .arg("2024-07-15T13:00:00Z") // 1 hour in the future from mock 'now'
       .assert()
       .success()
       .stdout(predicates::str::contains("Only 1 hour until the next temporal anomaly! Stay vigilant!"));
}

#[test]
fn test_until_past() {
    let mut cmd = Command::cargo_bin("nightly-chrono-compass").unwrap();
    cmd.arg("until")
       .arg("2024-07-15T11:00:00Z") // 1 hour in the past from mock 'now'
       .assert()
       .success()
       .stdout(predicates::str::contains("The target time has already passed, survivor! It was 1 hour ago."));
}

#[test]
fn test_since_past() {
    let mut cmd = Command::cargo_bin("nightly-chrono-compass").unwrap();
    cmd.arg("since")
       .arg("2024-07-15T11:00:00Z") // 1 hour in the past from mock 'now'
       .assert()
       .success()
       .stdout(predicates::str::contains("It has been 1 hour since that moment. Time flies, even in the apocalypse."));
}

#[test]
fn test_since_future() {
    let mut cmd = Command::cargo_bin("nightly-chrono-compass").unwrap();
    cmd.arg("since")
       .arg("2024-07-15T13:00:00Z") // 1 hour in the future from mock 'now'
       .assert()
       .success()
       .stdout(predicates::str::contains("That event is in the future, wanderer. It will be 1 hour from now."));
}

#[test]
fn test_between_ordered() {
    let mut cmd = Command::cargo_bin("nightly-chrono-compass").unwrap();
    cmd.arg("between")
       .arg("2024-07-15T10:00:00Z")
       .arg("2024-07-15T12:00:00Z")
       .assert()
       .success()
       .stdout(predicates::str::contains("The temporal span between those points is 2 hours. A blink in the void."));
}

#[test]
fn test_between_unordered() {
    let mut cmd = Command::cargo_bin("nightly-chrono-compass").unwrap();
    cmd.arg("between")
       .arg("2024-07-15T12:00:00Z")
       .arg("2024-07-15T10:00:00Z")
       .assert()
       .success()
       .stdout(predicates::str::contains("The temporal span between those points is 2 hours. A blink in the void."));
}

#[test]
fn test_countdown_known_future_event() {
    let mut cmd = Command::cargo_bin("nightly-chrono-compass").unwrap();
    cmd.arg("countdown")
       .arg("ResourceResupply") // 2024-07-20 08:00:00 UTC (from mock 'now' 2024-07-15 12:00:00 UTC)
       .assert()
       .success()
       .stdout(predicates::str::contains("Countdown to ResourceResupply: 4 days, 20 hours remaining! Prepare for the inevitable."));
}

#[test]
fn test_countdown_known_past_event() {
    let mut cmd = Command::cargo_bin("nightly-chrono-compass").unwrap();
    cmd.arg("countdown")
       .arg("FirstAnomaly") // 2024-07-10 00:00:00 UTC (past from mock 'now' 2024-07-15 12:00:00 UTC)
       .assert()
       .success()
       .stdout(predicates::str::contains("The 'FirstAnomaly' event has already transpired, traveler. It was 5 days, 12 hours ago."));
}

#[test]
fn test_countdown_unknown_event() {
    let mut cmd = Command::cargo_bin("nightly-chrono-compass").unwrap();
    cmd.arg("countdown")
       .arg("UnknownRift")
       .assert()
       .success()
       .stdout(predicates::str::contains("Unknown apocalyptic event: 'UnknownRift'. Perhaps it's a secret timeline?"));
}

#[test]
fn test_parse_datetime_local_format() {
    let mut cmd = Command::cargo_bin("nightly-chrono-compass").unwrap();
    // Mock 'now' is 2024-07-15 12:00:00 UTC. Target is 2024-07-15 13:00:00 UTC (1 hour in future).
    // Assuming local timezone is UTC for this test environment or that `Local.datetime_from_str` handles it.
    cmd.arg("until")
       .arg("2024-07-15 13:00:00")
       .assert()
       .success()
       .stdout(predicates::str::contains("Only 1 hour until the next temporal anomaly! Stay vigilant!"));
}

#[test]
fn test_parse_datetime_date_only() {
    let mut cmd = Command::cargo_bin("nightly-chrono-compass").unwrap();
    // Mock 'now' is 2024-07-15 12:00:00 UTC. Target is 2024-07-16 00:00:00 UTC (start of day).
    // This is 12 hours in the future.
    cmd.arg("until")
       .arg("2024-07-16")
       .assert()
       .success()
       .stdout(predicates::str::contains("Only 12 hours until the next temporal anomaly! Stay vigilant!"));
}
