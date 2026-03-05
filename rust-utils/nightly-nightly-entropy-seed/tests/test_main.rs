use std::process::Command;
use std::env;

#[test]
fn test_deterministic_repeatability() {
    // Set a fixed seed for reproducibility
    env::set_var("ENTROPY_SEED", "12345");

    // First run
    let out1 = Command::new(env!("CARGO_BIN_EXE_entropy-seed"))
        .args(&["-l", "12"])
        .output()
        .expect("failed to execute first run");
    assert!(out1.status.success());

    // Second run with same seed
    let out2 = Command::new(env!("CARGO_BIN_EXE_entropy-seed"))
        .args(&["-l", "12"])
        .output()
        .expect("failed to execute second run");
    assert!(out2.status.success());

    // Outputs should be identical
    assert_eq!(out1.stdout, out2.stdout);

    // Verify length and character set (default alphanumeric)
    let result = String::from_utf8_lossy(&out1.stdout).trim().to_string();
    assert_eq!(result.len(), 12);
    assert!(result.chars().all(|c| c.is_ascii_alphanumeric()));
}
