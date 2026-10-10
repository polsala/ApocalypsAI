// Integration test for the entropy-analyzer CLI.
// This test builds the binary using `cargo build` and then executes it with a known input.
// It verifies that the output matches the expected entropy value.

use std::process::Command;
use std::io::Write;

#[test]
fn cli_entropy_known_string() {
    // Build the binary first (debug build is sufficient for tests)
    let build_status = Command::new("cargo")
        .args(&["build"])
        .status()
        .expect("Failed to invoke cargo build");
    assert!(build_status.success(), "cargo build failed");

    // Prepare the input data
    let input = b"aaaaabbbbcc";

    // Execute the binary, feeding the input via STDIN
    let output = Command::new("./target/debug/entropy-analyzer")
        .output()
        .expect("Failed to execute binary");

    // The binary reads from STDIN when no file argument is given.
    // We need to spawn it with piped stdin.
    let mut child = Command::new("./target/debug/entropy-analyzer")
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .spawn()
        .expect("Failed to spawn child process");
    {
        let stdin = child.stdin.as_mut().expect("Failed to open stdin");
        stdin.write_all(input).expect("Failed to write to stdin");
    }
    let output = child.wait_with_output().expect("Failed to read stdout");
    let stdout = String::from_utf8_lossy(&output.stdout);
    // Expected output format: "Entropy: 1.4930 bits/byte"
    assert!(stdout.contains("Entropy:"), "Unexpected stdout: {}", stdout);
    // Extract the numeric part
    let parts: Vec<&str> = stdout.split_whitespace().collect();
    // parts[1] should be the numeric value
    let reported: f64 = parts[1].parse().expect("Failed to parse entropy value");
    let expected = 1.4930_f64;
    let diff = (reported - expected).abs();
    assert!(diff < 0.001, "Reported entropy {} differs from expected {}", reported, expected);
}
