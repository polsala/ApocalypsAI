// Integration test to verify the binary runs without panicking.
// No external resources are required; this test simply invokes the binary.

#[test]
fn run_binary() {
    // Mock rationale: we invoke the compiled binary with a deterministic seed.
    // The test passes if the process exits successfully.
    let output = std::process::Command::new("cargo")
        .args(&["run", "--quiet", "--", "123"])
        .output()
        .expect("failed to execute cargo run");
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("spotted near"));
}
