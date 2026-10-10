use std::process::Command;
use std::io::{Write, BufReader, BufRead};

// Mock rationale: These tests simulate input and capture output from the CLI tool
// without relying on external processes or actual file I/O, ensuring deterministic and offline execution.

#[test]
fn test_plain_text_filter() {
    let input_log = "INFO: System started\nWARN: Disk space low\nERROR: Critical failure\nINFO: Process completed\n";
    let filter_term = "ERROR";

    let mut child = Command::new("cargo")
        .args(["run", "--bin", "nightly-rust-log-parser"])
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .spawn()
        .expect("Failed to start the CLI tool");

    // Mock rationale: Writing to stdin to simulate input.
    let mut stdin = child.stdin.take().expect("Failed to open stdin");
    stdin.write_all(input_log.as_bytes()).expect("Failed to write to stdin");
    drop(stdin); // Close stdin to signal end of input

    let output = child.wait_with_output().expect("Failed to wait for CLI tool");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let expected_output = "ERROR: Critical failure\n";

    assert_eq!(stdout, expected_output);
    assert!(output.status.success());
}

#[test]
fn test_json_filter_message_field() {
    let input_log = "{\"level\": \"INFO\", \"message\": \"System started\"}\n{\"level\": \"WARN\", \"message\": \"Disk space low\"}\n{\"level\": \"ERROR\", \"message\": \"Critical failure detected\"}\n";
    let filter_term = "failure";

    let mut child = Command::new("cargo")
        .args(["run", "--bin", "nightly-rust-log-parser", "--format", "json", "--filter", filter_term])
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .spawn()
        .expect("Failed to start the CLI tool");

    // Mock rationale: Writing to stdin to simulate input.
    let mut stdin = child.stdin.take().expect("Failed to open stdin");
    stdin.write_all(input_log.as_bytes()).expect("Failed to write to stdin");
    drop(stdin);

    let output = child.wait_with_output().expect("Failed to wait for CLI tool");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let expected_output = "{\"level\": \"ERROR\", \"message\": \"Critical failure detected\"}\n";

    assert_eq!(stdout, expected_output);
    assert!(output.status.success());
}

#[test]
fn test_json_filter_any_field() {
    let input_log = "{\"level\": \"INFO\", \"details\": \"System started\"}\n{\"level\": \"WARN\", \"details\": \"Disk space low\"}\n{\"level\": \"ERROR\", \"details\": \"System halted\"}\n";
    let filter_term = "halted";

    let mut child = Command::new("cargo")
        .args(["run", "--bin", "nightly-rust-log-parser", "--format", "json", "--filter", filter_term])
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .spawn()
        .expect("Failed to start the CLI tool");

    // Mock rationale: Writing to stdin to simulate input.
    let mut stdin = child.stdin.take().expect("Failed to open stdin");
    stdin.write_all(input_log.as_bytes()).expect("Failed to write to stdin");
    drop(stdin);

    let output = child.wait_with_output().expect("Failed to wait for CLI tool");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let expected_output = "{\"level\": \"ERROR\", \"details\": \"System halted\"}\n";

    assert_eq!(stdout, expected_output);
    assert!(output.status.success());
}

#[test]
fn test_no_filter_matches() {
    let input_log = "INFO: System started\nINFO: Process completed\n";
    let filter_term = "error";

    let mut child = Command::new("cargo")
        .args(["run", "--bin", "nightly-rust-log-parser", "--filter", filter_term])
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .spawn()
        .expect("Failed to start the CLI tool");

    // Mock rationale: Writing to stdin to simulate input.
    let mut stdin = child.stdin.take().expect("Failed to open stdin");
    stdin.write_all(input_log.as_bytes()).expect("Failed to write to stdin");
    drop(stdin);

    let output = child.wait_with_output().expect("Failed to wait for CLI tool");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let expected_output = ""; // No lines should match

    assert_eq!(stdout, expected_output);
    assert!(output.status.success());
}

#[test]
fn test_plain_text_no_filter() {
    let input_log = "INFO: System started\nWARN: Disk space low\n";

    let mut child = Command::new("cargo")
        .args(["run", "--bin", "nightly-rust-log-parser"])
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .spawn()
        .expect("Failed to start the CLI tool");

    // Mock rationale: Writing to stdin to simulate input.
    let mut stdin = child.stdin.take().expect("Failed to open stdin");
    stdin.write_all(input_log.as_bytes()).expect("Failed to write to stdin");
    drop(stdin);

    let output = child.wait_with_output().expect("Failed to wait for CLI tool");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let expected_output = input_log;

    assert_eq!(stdout, expected_output);
    assert!(output.status.success());
}

#[test]
fn test_json_invalid_line_fallback() {
    let input_log = "{\"level\": \"INFO\", \"message\": \"Valid JSON\"}\nThis is not JSON\n{\"level\": \"ERROR\", \"message\": \"Another valid line\"}\n";
    let filter_term = "not JSON";

    let mut child = Command::new("cargo")
        .args(["run", "--bin", "nightly-rust-log-parser", "--format", "json", "--filter", filter_term])
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .spawn()
        .expect("Failed to start the CLI tool");

    // Mock rationale: Writing to stdin to simulate input.
    let mut stdin = child.stdin.take().expect("Failed to open stdin");
    stdin.write_all(input_log.as_bytes()).expect("Failed to write to stdin");
    drop(stdin);

    let output = child.wait_with_output().expect("Failed to wait for CLI tool");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let expected_output = "This is not JSON\n";

    assert_eq!(stdout, expected_output);
    assert!(output.status.success());
}
