use std::process::Command;
use std::str;

// Mock rationale: The sysinfo crate interacts with the OS directly. For deterministic
// offline tests, we will execute the compiled binary and capture its stdout.
// This assumes the binary is built and available at the specified path.
// In a real CI environment, this would be part of a build step.

#[test]
fn test_sys_info_output_format() {
    // Ensure the binary is built before running tests
    let output = Command::new("cargo")
        .args(&["build", "--release"])
        .output()
        .expect("Failed to build the project");

    assert!(output.status.success(), "Cargo build failed: {}", String::from_utf8_lossy(&output.stderr));

    let mut cmd = Command::new("./target/release/nightly-rust-sys-info");
    let output = cmd.output().expect("Failed to execute sys-info command");

    assert!(output.status.success(), "Command failed: {}", String::from_utf8_lossy(&output.stderr));

    let stdout = str::from_utf8(&output.stdout).expect("Output is not valid UTF-8");

    // Basic checks for expected sections and keywords
    assert!(stdout.contains("System Information:"));
    assert!(stdout.contains("CPU:"));
    assert!(stdout.contains("Memory:"));
    assert!(stdout.contains("Disk Usage:"));
    assert!(stdout.contains("Network Interfaces:"));

    // Check for specific patterns within sections (e.g., "Cores: ", "Total: ")
    assert!(stdout.contains("Cores:"));
    assert!(stdout.contains("Architecture:"));
    assert!(stdout.contains("Total:"));
    assert!(stdout.contains("Available:"));
    assert!(stdout.contains("Used:"));
    assert!(stdout.contains("GiB")); // Check for units
    assert!(stdout.contains("/")); // Check for disk usage format
    assert!(stdout.contains("%")); // Check for percentage
    assert!(stdout.contains("UP")); // Check for network status
}

#[test]
fn test_sys_info_no_panic() {
    // This test ensures the application runs without panicking, even if some
// OS-specific details are unavailable or malformed.
    let mut cmd = Command::new("./target/release/nightly-rust-sys-info");
    let output = cmd.output().expect("Failed to execute sys-info command");

    // We expect success, but the primary goal is to not panic.
    // If it panics, output.status.success() will be false and stderr will contain panic info.
    assert!(output.status.success(), "Command panicked or failed: {}", String::from_utf8_lossy(&output.stderr));
}
