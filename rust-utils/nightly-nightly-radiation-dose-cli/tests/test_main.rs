use std::process::Command;

#[test]
fn test_cli_output() {
    // Mock rationale: we run the compiled binary with known inputs and check output.
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-radiation-dose-cli"))
        .arg("2.0")
        .arg("30")
        .arg("0.5")
        .output()
        .expect("failed to execute process");
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    // Expected dose 0.0625 Sv (printed with 6 decimal places)
    assert!(stdout.contains("Estimated dose: 0.062500 Sv"));
}
