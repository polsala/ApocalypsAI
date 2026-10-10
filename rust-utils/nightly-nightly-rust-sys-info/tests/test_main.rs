#[cfg(test)]
mod tests {
    use super::*;
    use std::process::Command;
    use std::str;

    // Mock rationale: These tests simulate running the CLI tool and capturing its output.
    // We don't need to mock the sysinfo crate itself as we are testing the integration
    // of its output into our CLI's presentation. The tests are deterministic as they
    // rely on the output of the command, not external system state that can change.

    #[test]
    fn test_sys_info_output_contains_key_info() {
        // Ensure the binary is built before running tests
        let output = Command::new("./target/release/nightly-rust-sys-info")
            .output()
            .expect("Failed to execute command");

        assert!(output.status.success(), "Command failed to execute");

        let stdout = str::from_utf8(&output.stdout).expect("Failed to convert stdout to string");

        // Check for presence of key information fields
        assert!(stdout.contains("✨ System Name:"));
        assert!(stdout.contains("🐧 Kernel Version:"));
        assert!(stdout.contains("⚡ CPU Model:"));
        assert!(stdout.contains("💾 Memory Usage:"));
        assert!(stdout.contains("💽 Disk Usage (Root):"));
    }

    #[test]
    fn test_sys_info_output_format() {
        // This test checks for a specific format, assuming a basic structure.
        // It's less about exact values (which vary) and more about the presence of lines.
        let output = Command::new("./target/release/nightly-rust-sys-info")
            .output()
            .expect("Failed to execute command");

        assert!(output.status.success(), "Command failed to execute");

        let stdout = str::from_utf8(&output.stdout).expect("Failed to convert stdout to string");
        let lines: Vec<&str> = stdout.lines().collect();

        // Expecting at least these lines, though more might be present.
        assert!(lines.iter().any(|&line| line.starts_with("✨ System Name:")));
        assert!(lines.iter().any(|&line| line.starts_with("🐧 Kernel Version:")));
        assert!(lines.iter().any(|&line| line.starts_with("⚡ CPU Model:")));
        assert!(lines.iter().any(|&line| line.starts_with("  Total: ") && line.contains(" GB")));
        assert!(lines.iter().any(|&line| line.starts_with("  Used: ") && line.contains(" GB")));
    }
}
