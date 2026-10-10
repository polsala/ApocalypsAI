use std::process::Command;

#[test]
fn cli_runs_without_args() {
    // The binary path is provided by Cargo during integration tests
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-apocalypse-quote-cli"))
        .output()
        .expect("failed to execute binary");
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(!stdout.trim().is_empty(), "Expected non‑empty quote output");
}
