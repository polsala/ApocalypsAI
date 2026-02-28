// Mock rationale: We mock external commands like `pgrep` and `kill` to avoid side effects during testing.
// These tests verify logic flow without actually killing real processes.

use assert_cmd::prelude::*;
use predicates::prelude::*;
use std::process::Command;
use tempfile::NamedTempFile;
use std::io::Write;

#[test]
fn test_dry_run_mode() {
    let mut cmd = Command::cargo_bin("chaos-monkey").unwrap();
    cmd.arg("--target")
       .arg("fakeproc")
       .arg("--dry-run")
       .arg("--duration")
       .arg("1");

    cmd.assert()
       .success()
       .stdout(predicate::str::contains("Chaos session completed"));
}

#[test]
fn test_help_output() {
    let mut cmd = Command::cargo_bin("chaos-monkey").unwrap();
    cmd.arg("--help");

    cmd.assert()
       .success()
       .stdout(predicate::str::contains("USAGE"));
}
