#[test]
fn cli_works() {
    // Mock rationale: ensure the binary produces the expected name for a known colour
    let output = std::process::Command::new(env!("CARGO_BIN_EXE_hexapoc-namer"))
        .arg("#ff4500")
        .output()
        .expect("failed to execute binary");
    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert_eq!(stdout.trim(), "blazing ember");
}
