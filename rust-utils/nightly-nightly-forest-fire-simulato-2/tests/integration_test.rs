#[cfg(test)]
mod integration {
    use std::process::Command;

    #[test]
    fn runs_without_panic() {
        // Mock rationale: we invoke the compiled binary with deterministic arguments.
        // The test ensures the program exits successfully and produces the expected number of lines.
        let output = Command::new("cargo")
            .args(&["run", "--quiet", "--", "5", "5", "2", "12345"])
            .output()
            .expect("Failed to execute cargo run");
        assert!(output.status.success());
        let stdout = String::from_utf8_lossy(&output.stdout);
        // Initial state + 2 steps => 3 grids, each with 5 lines, plus headers.
        // Rough check: at least 15 newline characters.
        let newline_count = stdout.matches('\n').count();
        assert!(newline_count >= 15, "Expected many lines of output, got {}", newline_count);
    }
}
