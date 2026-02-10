#[cfg(test)]
mod integration {
    use std::process::Command;

    #[test]
    fn cli_produces_output() {
        // Build the binary first (cargo test builds it automatically)
        let output = Command::new("cargo")
            .args(&["run", "--quiet", "--release", "--", "TEST"])
            .output()
            .expect("Failed to execute binary");
        assert!(output.status.success(), "Binary exited with non‑zero status");
        let stdout = String::from_utf8_lossy(&output.stdout);
        // The QR for "TEST" must contain at least one dark block.
        assert!(stdout.contains("██"), "CLI output does not contain QR block characters");
    }
}
