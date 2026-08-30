use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;
use std::fs;
use std::collections::HashMap;
use std::path::PathBuf;
use std::env;

// Mock rationale: Using `tempfile::tempdir()` to create an isolated, temporary directory
// for configuration files. This ensures tests are deterministic, don't interfere with
// actual user configurations, and are fully offline without external dependencies.

fn get_test_config_dir() -> PathBuf {
    let dir = tempdir().expect("Failed to create temp dir");
    dir.path().to_path_buf()
}

#[test]
fn test_store_and_list_profile() {
    let config_dir = get_test_config_dir();

    // Set some environment variables for the test
    env::set_var("TEST_VAR_1", "value1");
    env::set_var("TEST_VAR_2", "value2 with spaces");

    // Store a profile
    let mut cmd = Command::cargo_bin("nightly-env-scavenger").unwrap();
    cmd.env("XDG_CONFIG_HOME", &config_dir)
       .arg("store")
       .arg("test-profile-1")
       .assert()
       .success()
       .stdout(predicate::str::contains("Scavenged cache 'test-profile-1' stored successfully."));

    // List profiles and check if it's there
    let mut cmd = Command::cargo_bin("nightly-env-scavenger").unwrap();
    cmd.env("XDG_CONFIG_HOME", &config_dir)
       .arg("list")
       .assert()
       .success()
       .stdout(predicate::str::contains("- test-profile-1"));

    // Clean up env vars
    env::remove_var("TEST_VAR_1");
    env::remove_var("TEST_VAR_2");
}

#[test]
fn test_load_profile() {
    let config_dir = get_test_config_dir();

    // Manually create a profile file for loading
    let profile_content = r#"
[profiles."test-profile-to-load"]
name = "test-profile-to-load"

[profiles."test-profile-to-load".vars]
LOAD_VAR_A = "alpha"
LOAD_VAR_B = "beta value with spaces"
"#;
    let profiles_path = config_dir.join("nightly-env-scavenger").join("profiles.toml");
    fs::create_dir_all(profiles_path.parent().unwrap()).unwrap();
    fs::write(&profiles_path, profile_content).unwrap();

    // Load the profile and check its output
    let mut cmd = Command::cargo_bin("nightly-env-scavenger").unwrap();
    cmd.env("XDG_CONFIG_HOME", &config_dir)
       .arg("load")
       .arg("test-profile-to-load")
       .assert()
       .success()
       .stdout(predicate::str::contains("export LOAD_VAR_A=\"alpha\";"))
       .stdout(predicate::str::contains("export LOAD_VAR_B=\"beta value with spaces\";"));
}

#[test]
fn test_remove_profile() {
    let config_dir = get_test_config_dir();

    // Manually create a profile file for removal
    let profile_content = r#"
[profiles."profile-to-remove"]
name = "profile-to-remove"

[profiles."profile-to-remove".vars]
VAR_TO_REMOVE = "value"

[profiles."another-profile"]
name = "another-profile"

[profiles."another-profile".vars]
ANOTHER_VAR = "another_value"
"#;
    let profiles_path = config_dir.join("nightly-env-scavenger").join("profiles.toml");
    fs::create_dir_all(profiles_path.parent().unwrap()).unwrap();
    fs::write(&profiles_path, profile_content).unwrap();

    // Remove the profile
    let mut cmd = Command::cargo_bin("nightly-env-scavenger").unwrap();
    cmd.env("XDG_CONFIG_HOME", &config_dir)
       .arg("remove")
       .arg("profile-to-remove")
       .assert()
       .success()
       .stdout(predicate::str::contains("Scavenged cache 'profile-to-remove' removed successfully."));

    // List profiles and ensure it's gone
    let mut cmd = Command::cargo_bin("nightly-env-scavenger").unwrap();
    cmd.env("XDG_CONFIG_HOME", &config_dir)
       .arg("list")
       .assert()
       .success()
       .stdout(predicate::str::contains("- another-profile"))
       .stdout(predicate::str::not(predicate::str::contains("- profile-to-remove")));
}

#[test]
fn test_list_empty() {
    let config_dir = get_test_config_dir();

    // List profiles when no profiles exist
    let mut cmd = Command::cargo_bin("nightly-env-scavenger").unwrap();
    cmd.env("XDG_CONFIG_HOME", &config_dir)
       .arg("list")
       .assert()
       .success()
       .stdout(predicate::str::contains("No scavenged caches found."));
}

#[test]
fn test_load_non_existent_profile() {
    let config_dir = get_test_config_dir();

    // Try to load a non-existent profile
    let mut cmd = Command::cargo_bin("nightly-env-scavenger").unwrap();
    cmd.env("XDG_CONFIG_HOME", &config_dir)
       .arg("load")
       .arg("non-existent-profile")
       .assert()
       .failure()
       .stderr(predicate::str::contains("Error: Scavenged cache 'non-existent-profile' not found."));
}

#[test]
fn test_store_with_special_chars_in_value() {
    let config_dir = get_test_config_dir();

    env::set_var("SPECIAL_VAR", "value with \"quotes\" and spaces");

    let mut cmd = Command::cargo_bin("nightly-env-scavenger").unwrap();
    cmd.env("XDG_CONFIG_HOME", &config_dir)
       .arg("store")
       .arg("special-char-profile")
       .assert()
       .success();

    let mut cmd = Command::cargo_bin("nightly-env-scavenger").unwrap();
    cmd.env("XDG_CONFIG_HOME", &config_dir)
       .arg("load")
       .arg("special-char-profile")
       .assert()
       .success()
       .stdout(predicate::str::contains("export SPECIAL_VAR=\"value with \\\"quotes\\\" and spaces\";"));

    env::remove_var("SPECIAL_VAR");
}
