#[cfg(test)]
mod tests {
    use super::*;
    use std::process::Command;
    use std::str;

    // Mock rationale: These tests execute the compiled binary and capture its stdout.
    // This is a form of integration testing for the CLI tool itself, ensuring it runs
    // and produces output without relying on external services or complex mocking.
    // The output format is checked for presence of key sections.

    #[test]
    fn test_sysinfo_cli_output_structure() {
        // Ensure the binary is built before running
        let output = Command::new("cargo")
            .args(&["run", "--release"])
            .output()
            .expect("Failed to execute cargo run");

        assert!(output.status.success(), "Cargo run failed: {}", String::from_utf8_lossy(&output.stderr));

        let stdout = str::from_utf8(&output.stdout).expect("Failed to convert stdout to string");

        // Check for the presence of key sections in the output
        assert!(stdout.contains("--- System Information ---"));
        assert!(stdout.contains("CPU Usage:"));
        assert!(stdout.contains("Memory Usage:"));
        assert!(stdout.contains("Network Interfaces:"));
        assert!(stdout.contains("Disk Usage:"));
        assert!(stdout.contains("--- End of Report ---"));
    }

    #[test]
    fn test_sysinfo_cli_no_panic() {
        // This test primarily checks that the application runs to completion without panicking.
        // We don't need to assert specific output values as they are highly system-dependent.
        let output = Command::new("cargo")
            .args(&["run", "--release"])
            .output()
            .expect("Failed to execute cargo run");

        assert!(output.status.success(), "Cargo run panicked or failed: {}", String::from_utf8_lossy(&output.stderr));
    }
}
